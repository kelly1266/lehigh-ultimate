import discord
from discord.ext.commands import Bot
from discord.utils import get
import config

TOKEN = config.TOKEN
client = Bot(command_prefix=config.BOT_PREFIX)


async def role_in_list(role_name, role_list):
    in_list = False
    i = 0
    while i < len(role_list) and not in_list:
        in_list = role_name == role_list[i].name.lower()
        i+=1
    return in_list


@client.command(
    name='ping',
    description = 'Tests that a bot is active.',
    pass_context=True,
)
async def ping(context):
    await context.message.channel.send('pong')


@client.command(
    name='role',
    description='Creates a new role or assigns a user the role if it exists',
    pass_context=True
)
async def role(context, *args):
    if len(args)>0:
        # get guild object
        guild = context.guild
        # parse role name
        role_name = ''
        for x in args:
            role_name = role_name + x + ' '
        role_name = role_name[:-1].lower()
        # get a list of existing guid roles and check if the role already exists or not
        roles_list = await guild.fetch_roles()
        if await role_in_list(role_name, roles_list):
            # assign user the role
            await context.message.author.add_roles(get(guild.roles, name=role_name))
        else:
            #create the role
            created_role = await guild.create_role(name=role_name)
            await context.message.author.add_roles(created_role)
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