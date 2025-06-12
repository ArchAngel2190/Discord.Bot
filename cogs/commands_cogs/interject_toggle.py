import discord
from discord import app_commands
from discord.ext import commands

# In-memory set of guild IDs with interjections disabled
_interject_disabled = set()

def interjections_enabled(guild_id: int) -> bool:
    return guild_id not in _interject_disabled

class InterjectToggle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="disable_interjections",
        description="Turn OFF random AI interjections in this server"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def disable_interjections(self, interaction: discord.Interaction):
        _interject_disabled.add(interaction.guild_id)
        await interaction.response.send_message(
            "🚫 Random interjections are now **disabled** in this server.", ephemeral=True
        )

    @app_commands.command(
        name="enable_interjections",
        description="Turn ON random AI interjections in this server"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def enable_interjections(self, interaction: discord.Interaction):
        _interject_disabled.discard(interaction.guild_id)
        await interaction.response.send_message(
            "✅ Random interjections are now **enabled** in this server.",
            ephemeral=True
        )

    @app_commands.command(
        name="interjection_status",
        description="Check if random interjections are on or off"
    )
    async def interjection_status(self, interaction: discord.Interaction):
        status = "enabled" if interjections_enabled(interaction.guild_id) else "disabled"
        await interaction.response.send_message(
            f"Random interjections are currently **{status}** in this server.",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(InterjectToggle(bot))
