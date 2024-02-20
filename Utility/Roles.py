import discord
from discord.ext import commands


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def addrole(self, ctx, role: discord.Role, member: discord.Member):
        await member.add_roles(role)
        await ctx.send(f"{member.mention} has been given the {role.name} role.")

    @commands.command()
    @commands.is_owner()
    async def delrole(self, ctx, role: discord.Role, member: discord.Member):
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} has had the {role.name} role removed.")

    @commands.command()
    @commands.is_owner()
    async def createrole(self, ctx, *, role_name: str):
        if role_name is None:
            await ctx.send("Please provide a name for the role.")
            return
        role = await ctx.guild.create_role(name=role_name)
        await ctx.send(f"The {role.name} role has been created.")


async def setup(bot):
    await bot.add_cog(Roles(bot))
