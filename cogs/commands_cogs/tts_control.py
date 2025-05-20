import discord
from discord import app_commands
from discord.ext import commands

class TTSCtrl(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="stoptts",
        description="Immediately stop any currently playing TTS and disconnect."
    )
    async def stoptts(self, interaction: discord.Interaction):
        vc: discord.VoiceClient = interaction.guild.voice_client
        if vc is None:
            await interaction.response.send_message(
                "I’m not in a voice channel right now.", ephemeral=True
            )
            return

        if vc.is_playing():
            vc.stop()
            await interaction.response.send_message(
                "🔇 TTS playback stopped.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "There was no TTS playing.", ephemeral=True
            )

        # optionally disconnect
        await vc.disconnect()

async def setup(bot: commands.Bot):
    await bot.add_cog(TTSCtrl(bot))