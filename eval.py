import io
import re
import contextlib
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

@commands.command()
@checks.has_permissions(PermissionLevel.OWNER)
async def help(ctx):
    embed = discord.Embed(title="Help", color=0x3975AA)
    embed.add_field(name="help", value="Shows this message", inline=False)
    embed.add_field(name="evaluate | eval | e", value="Evaluates the python code in the code block", inline=False)
    return await ctx.send(embed=embed)

@commands.command(aliases=["eval", "e"])
@checks.has_permissions(PermissionLevel.OWNER)
async def evaluate(ctx, *, command):
    """Evaluate the given python code"""
    if match := re.fullmatch(r"(?:\n*)?`(?:``(?:py(?:thon)?\n)?((?:.|\n)*)``|(.*))`", command, re.DOTALL):
        code = match.group(1) if match.group(1) else match.group(2)
        str_obj = io.StringIO()  # Retrieves a stream of data
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as e:
            return await ctx.send(f"""❌ Your code completed with execution code 1
```
{e.__class__.__name__}: {e}
```""")
        return await ctx.send(f"""✅ Your code completed with execution code 0
```
{str_obj.getvalue()}
```""")
    embed = discord.Embed(description="Error: Invalid format", color=0xED2525)
    return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(eval(bot))