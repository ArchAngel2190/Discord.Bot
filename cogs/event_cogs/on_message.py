import discord
import asyncio
from discord.ext import commands

from bot_utilities.response_utils import split_response
from bot_utilities.ai_utils import generate_response
from bot_utilities.config_loader import config, load_active_channels
from ..common import allow_dm, trigger_words, replied_messages, smart_mention, message_history, MAX_HISTORY, instructions

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = load_active_channels
        self.instructions = instructions

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
            await asyncio.sleep(10)
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

    async def send_response(self, message, response):
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

        await self.process_message(message)

async def setup(bot):
    await bot.add_cog(OnMessage(bot))
