import discord
from discord import app_commands
from discord.ext import commands

from ..common import current_language

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description=current_language["help"])
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Need help?", description="The following commands are available on this bot:", color=0x03a64b)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        for cmd in self.bot.tree.get_commands():
            # skip hidden or non-Cog commands
            if getattr(cmd, "hidden", False):
                continue
            desc = cmd.description or "No description available"
            embed.add_field(name=f"/{cmd.name}", value=desc, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))
