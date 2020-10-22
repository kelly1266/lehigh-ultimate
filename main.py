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
        i += 1
    return in_list


@client.command(
    name='ping',
    description='Tests that a bot is active.',
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
    if len(args) > 0:
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
            # create the role
            created_role = await guild.create_role(name=role_name)
            await context.message.author.add_roles(created_role)
    return


@client.command(
    name='team',
    description='creates a new channel that is only visible to people with the team role',
    pass_context=True
)
async def team(context, *args):
    if len(args) > 0:
        # get guild object
        guild = context.guild
        # parse team name
        team_name = ''
        for x in args:
            team_name = team_name + x + ' '
        team_name = team_name[:-1].lower()
        channel_name = team_name.replace(' ', '-')

        if get(guild.text_channels, name=channel_name) is not None:
            # channel exists
            await context.message.author.add_roles(get(guild.roles, name=team_name))
        else:
            # channel does not exist
            category_id = config.TEAM_CATEGORY
            category = get(guild.categories, id=category_id)
            await guild.create_text_channel(channel_name, category=category)
            created_role = await guild.create_role(name=team_name)
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
