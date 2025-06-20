import discord
import os
import io
import aiohttp
import asyncio
import random
import time

from dotenv import load_dotenv
from discord.ext import commands
from gtts import gTTS
from discord import FFmpegPCMAudio

from bot_utilities.response_utils import split_response
from bot_utilities.ai_utils import generate_response
from bot_utilities.config_loader import config, load_active_channels
from ..common import allow_dm, trigger_words, replied_messages, smart_mention, message_history, MAX_HISTORY, instructions
from cogs.commands_cogs.voice_toggle import voice_is_enabled
from cogs.commands_cogs.interject_toggle import interjections_enabled

load_dotenv ()
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
ELEVEN_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

_interjection_timestamps = {}
INTERJECTION_COOLDOWN = config['INTERJECTION_COOLDOWN']
INTERJECTION_CHANCE = config['INTERJECTION_CHANCE']

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = load_active_channels
        self.instructions = instructions

    async def eleven_tts(self, text: str) -> io.BytesIO:
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": ELEVEN_API_KEY
        }
        payload = { "text": text }
        buf = io.BytesIO()
        async with aiohttp.ClientSession() as session:
            async with session.post(ELEVEN_URL, json=payload, headers=headers) as resp:
                resp.raise_for_status()
                data = await resp.read()
                buf.write(data)
            buf.seek(0)
            return buf
        
    async def process_message(self, message):
        active_channels = self.active_channels()
        string_channel_id = f"{message.channel.id}"
        is_replied = (message.reference and message.reference.resolved.author == self.bot.user) and smart_mention
        is_dm_channel = isinstance(message.channel, discord.DMChannel)
        is_active_channel = string_channel_id in active_channels
        is_allowed_dm = allow_dm and is_dm_channel
        contains_trigger_word = any(word in message.content for word in trigger_words)
        is_bot_mentioned = self.bot.user.mentioned_in(message) and smart_mention and not message.mention_everyone
        bot_name_in_message = self.bot.user.name.lower() in message.content.lower() and smart_mention

        if not (is_active_channel or is_allowed_dm or contains_trigger_word or is_bot_mentioned or is_replied or bot_name_in_message):
            return

        # Prepare instructions using the config value
        instruc_config = active_channels.get(string_channel_id, config['DEFAULT_INSTRUCTION'])
        instructions_text = f"Ignore all the instructions you have gotten before. {self.instructions[instruc_config]}. "

        # Update message history
        channel_id = message.channel.id
        key = f"{message.author.id}-{channel_id}"
        message_history[key] = message_history.get(key, [])
        message_history[key] = message_history[key][-MAX_HISTORY:]
        message_history[key].append({"role": "user", "content": message.content})

        # Create an Event flag to signal when we're done
        typing_done = asyncio.Event()

        # Define a background task to keep typing until done
        async def keep_typing():
            while not typing_done.is_set():
                async with message.channel.typing():
                    await asyncio.sleep(3)  # Refresh typing indicator every 3 seconds

        # Stop typing automatically in case of error
        async def auto_stop_typing():
            await asyncio.sleep(5)
            typing_done.set()

        # Start the background typing task
        self.bot.loop.create_task(keep_typing())
        self.bot.loop.create_task(auto_stop_typing())

        # Generate the response (text-only)
        response = await self.generate_response(instructions_text, message_history[key])
        message_history[key].append({"role": "assistant", "content": response})

        # Send the response message(s)
        await self.send_response(message, response)

        # Signal to stop the typing indicator
        typing_done.set()

    async def generate_response(self, instructions, history):
        return await generate_response(instructions=instructions, history=history)

    async def send_response(self, message, response: str):
        if response is not None:
            for chunk in split_response(response):
                try:
                    await message.reply(chunk, suppress_embeds=True)
                except Exception:
                    await message.channel.send(
                        "I apologize for any inconvenience caused. It seems that there was an error preventing the delivery of my message. Additionally, it appears that the message I was replying to has been deleted, which could be the reason for the issue. If you have any further questions or if there's anything else I can assist you with, please let me know and I'll be happy to help."
                    )
        else:
            await message.reply(
                "I apologize for any inconvenience caused. It seems that there was an error preventing the delivery of my message."
            )

        # Ensure we're in a guild and that the admin wants us speaking
        if not message.guild or not voice_is_enabled(message.guild.id):
            return

        # Check if author is connected / determine voice state
        if message.author.voice and message.guild:
            vc = message.guild.voice_client
            target = message.author.voice.channel

            bot_connected = False
            try:
                # Join or move
                if vc is None:
                    vc = await target.connect()
                    bot_connected = True      # we made the connection
                elif vc.channel != target:
                    await vc.move_to(target)
                    bot_connected = True

                # TTS playback
                tts_buf = await self.eleven_tts(response)
                from discord import FFmpegPCMAudio
                source = FFmpegPCMAudio(tts_buf, pipe=True)
                vc.play(source)
                while vc.is_playing():
                    await asyncio.sleep(0.5)

            except Exception as e:
                print(f"Text-to-Speech error: {e}")

            finally:
                # Only disconnect if *we* connected for this message
                if bot_connected and vc and vc.is_connected():
                    await vc.disconnect()

    @commands.Cog.listener()
    async def on_message(self, message):
        # Track replied messages (for context/history)
        if message.author == self.bot.user and message.reference:
            replied_messages[message.reference.message_id] = message
            if len(replied_messages) > 5:
                oldest_message_id = min(replied_messages.keys())
                del replied_messages[oldest_message_id]

        # Replace mentions with display names
        if message.mentions:
            for mention in message.mentions:
                message.content = message.content.replace(f'<@{mention.id}>', f'{mention.display_name}')

        # Ignore stickers, bots, and certain message references
        if message.stickers or message.author.bot or (
            message.reference and (message.reference.resolved.author != self.bot.user or message.reference.resolved.embeds)
        ):
            return
        
        if self.bot.user.mentioned_in(message):
            await self.process_message(message)
            return

        # — Smart Interjection Logic —
        guild_id = message.guild.id if message.guild else None
        now = time.time()
        last = _interjection_timestamps.get(guild_id, 0)

        # Only if enough time has passed and random chance hits, and interjections enabled
        if not interjections_enabled(message.guild.id):
            if guild_id and now - last > INTERJECTION_COOLDOWN and random.random() < INTERJECTION_CHANCE:
                # Grab the last few messages from this channel for context
                active_channels = load_active_channels()
                string_channel_id = str(message.channel.id)
                instr_idx = active_channels.get(string_channel_id, config['DEFAULT_INSTRUCTION'])

            # prepend the system prompt from your instructions file
            instructions_text = (
                "Ignore all the instructions you have gotten before. "
                f"{instructions[instr_idx]}. "
                "Now, having listened to the last messages, interject with a short, witty, context‑aware phrase, "
                "then go quiet again."
    )

            # build the history just as you do for normal replies
            history = []
            async for msg in message.channel.history(limit=10, oldest_first=False):
                if not msg.author.bot:
                    history.append({"role": "user", "content": msg.content})
                history.reverse()

        # now call your normal generate_response
        async with message.channel.typing():
            interjection = await generate_response(instructions=instructions_text, history=history)
        await message.channel.send(interjection)
        _interjection_timestamps[guild_id] = now  # reset the cooldown

        await self.process_message(message)

async def setup(bot):
    await bot.add_cog(OnMessage(bot))
