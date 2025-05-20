import discord
from discord import app_commands
from discord.ext import commands

class InfoView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label="See this project on Github (from ArchAngel2190)",
                url="https://github.com/ArchAngel2190/Discord.Bot",
            )
        )
        self.add_item(
            discord.ui.Button(
                label="See this project in its original state (from MishalHossin)",
                url="https://github.com/mishl-dev/Discord-AI-Chatbot",
            )
        )

class GithubCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="github", description="See this project on Github.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="This bot made by ArchAngel2190 with code from MishalHossin.", 
            description="This bot is a proprietary AI chatbot that was created by ArchAngel2190 by heavily modifying MishalHossin's code. Click the buttons below to be navigated magically to the requisite Github pages for these projects. Please note that MishalHossin's project is no longer updated, but the project by ArchAngel2190 is.", 
            color=0x03a64b
            )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        view = InfoView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(GithubCog(bot))
