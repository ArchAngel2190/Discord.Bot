import discord
from discord import app_commands
from discord.ext import commands

# In-memory store of guilds who have voice *disabled*
_disabled_voice = set()

def voice_is_enabled(guild_id: int) -> bool:
    return guild_id not in _disabled_voice

class VoiceToggle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="disable_voice",
        description="Turn OFF TTS/voice output in this server."
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def disable_voice(self, interaction: discord.Interaction):
        _disabled_voice.add(interaction.guild_id)
        await interaction.response.send_message(
            "🔇 Voice/TTS **disabled** for this server.", ephemeral=True
        )

    @app_commands.command(
        name="enable_voice",
        description="Turn ON TTS/voice output in this server."
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def enable_voice(self, interaction: discord.Interaction):
        _disabled_voice.discard(interaction.guild_id)
        await interaction.response.send_message(
            "🔊 Voice/TTS **enabled** for this server.", ephemeral=True
        )

    @app_commands.command(
        name="voice_status",
        description="Show whether voice/TTS is enabled in this server."
    )
    async def voice_status(self, interaction: discord.Interaction):
        status = "enabled" if voice_is_enabled(interaction.guild_id) else "disabled"
        await interaction.response.send_message(
            f"Voice/TTS is currently **{status}** in this server.", ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceToggle(bot))
