from discord.ext import commands
import discord
from dispie import EmbedCreator 
import config

class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('>'), intents=intents, **kwargs)

    async def setup_hook(self):
        for cog in config.cogs:
            try:
                await self.load_extension(cog)
            except Exception as exc:
                print(f'Could not load extension {cog} due to {exc.__class__.__name__}: {exc}')

    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')

intents = discord.Intents.default()
intents.message_content = True
bot = Bot(intents=intents)


@bot.command(name="notify")
@commands.has_role("Admin")
async def notify(ctx: commands.Context):
    view = EmbedCreator(bot=bot)
    await ctx.send(embed=view.get_default_embed, view=view)

@bot.command(name="announce")
@commands.has_role("Admin")
async def message(ctx, channel: discord.TextChannel, *, content):
    await channel.send(content)

bot.run(config.token)
