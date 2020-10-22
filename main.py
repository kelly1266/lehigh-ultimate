import discord
from discord.ext.commands import Bot
import config

TOKEN = config.TOKEN
client = Bot(command_prefix=config.BOT_PREFIX)


@client.command(
    name='ping',
    description = 'Tests that a bot is active.',
    pass_context=True,
)
async def ping(context):
    await context.message.channel.send('pong')


@client.command(
    name='role',
    description='Creates a new role',
    pass_context=True
)
async def role(contextt, *args):
    return


@client.event
async def on_ready():
    """
    Displays a short message in the console when the bot is initially run
    :return:
    """
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)