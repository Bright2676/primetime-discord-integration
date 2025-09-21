import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="kick", description="Kick a user from the server.")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        dm_embed = discord.Embed(title="Moderation Notice", description=f"You have been kicked from Primetime.\n Reason: {reason}")
        general_embed = discord.Embed(title="User Kicked", description=f"**{member}** has been kicked from the server.\nReason: {reason}")

        try:
            await member.kick(reason=reason)
            if not member.dm_channel:
                await member.create_dm()
            await member.dm_channel.send(embed=dm_embed)
            await interaction.response.send_message(embed=general_embed)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"An error occurred while kicking {member}.\nError: {e}")
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Kick(bot))