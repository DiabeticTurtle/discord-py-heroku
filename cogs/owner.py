import discord
from discord.ext import commands
import subprocess as sp
import os
from jishaku import  codeblocks

class OwnerCog(commands.Cog, name="Owner"):
    """Owner Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load')
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        # Command which Loads a Module.
        # Remember to use dot path. e.g: cogs.owner

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload')
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        # Command which Unloads a Module.
        # Remember to use dot path. e.g: cogs.owner

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload')
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        # Command which Reloads a Module.
        # Remember to use dot path. e.g: owner

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
            await ctx.send(f"Reloaded cog {cog}")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(aliases=["reloadall", "ra"])
    @commands.is_owner()
    async def reload_all(self, ctx):
        s = []
        e = []
        l = []

        for cog in os.listdir("cogs/"):
            if ".py" in cog:
                l.append(f"cogs.{cog[:-3]}")

        for cog in l:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
                s.append(cog)
            except Exception as p:
                e.append(cog)

        embed = discord.Embed(title="Reloaded all cogs", color = self.bot.embed_color)
        embed.add_field(name="Succesful Cogs", value=str.join("   ", s))
        p = str.join("   ", e)
        if p == "": p = "None"
        embed.add_field(name="Unsuccesful Cogs", value=p)
        await ctx.send(embed=embed)

    @commands.command(name='cogs')
    @commands.is_owner()
    async def active_cogs(self, ctx):
        s = str.join('\n', self.bot.cogs.keys())
        await ctx.send(embed=discord.Embed(title="Active Cogs:", description=f"```{s}```", color = self.bot.embed_color))

    @commands.command(aliases=['pull'])
    @commands.is_owner()
    async def sync(self, ctx):
        """Get the most recent changes from the GitHub repository
        Uses: p,sync"""
        embedvar = discord.Embed(title="Syncing...", description="Syncing with the GitHub repository, this should take up to 15 seconds", color=0xff0000, timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=embedvar)
        async with ctx.channel.typing():
            output = sp.getoutput('git pull origin master')
            await ctx.send(f""" ```sh
            {output} ```""")
            msg1 = await ctx.send("Success!")
            await msg1.delete()
        embedvar = discord.Embed(title="Synced", description="Sync with the GitHub repository has completed, check the logs to make sure it worked", color=0x00ff00, timestamp=ctx.message.created_at)
        await msg.edit(embed=embedvar)

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restarts the bot, actually just closes the bot"""
        await ctx.send("Bye!")
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def journalctl(self, ctx):
        await ctx.invoke(self.bot.get_command('jsk sh'),
                         argument=codeblocks.codeblock_converter("journalctl -u diaranks"))

def setup(bot):
    bot.add_cog(OwnerCog(bot))