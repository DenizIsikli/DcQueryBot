import discord
from discord.ext import commands


class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['del'])
    @commands.is_owner()
    async def delete(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            command_owner = ctx.bot.get_user(ctx.bot.owner_id)
            await ctx.send(f"Missing permission! - Permission assigned to {command_owner}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "No reason provided"
        await ctx.guild.kick(member)
        await ctx.send(f"User {member.mention} has been kicked\nReason: {reason}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            command_owner = ctx.bot.get_user(ctx.bot.owner_id)
            await ctx.send(f"Missing permission! - Permission assigned to {command_owner}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


class Mute(commands.Cog):
    @commands.command()
    @commands.is_owner()
    async def mute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(muted_role, send_messages=False)

        await member.add_roles(muted_role)

    @commands.command()
    @commands.is_owner()
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role)
        else:
            await ctx.send("User is not muted")


async def setup(bot):
    await bot.add_cog(Delete(bot))
    await bot.add_cog(Kick(bot))
    await bot.add_cog(Mute(bot))
