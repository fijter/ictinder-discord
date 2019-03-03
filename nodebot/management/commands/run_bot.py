import discord
import asyncio
import socket
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from nodebot.external_api import IctApi
from nodebot.models import Message

class Command(BaseCommand):
    help = 'Runs the Discord Bot'

    def handle(self, *args, **options):
        client = discord.Client()

        @client.event
        async def on_ready():
            print('Ictinder bot logged in as')
            print(client.user.name)
            print(client.user.id)
            print('------')

        @client.event
        async def on_message(message):
            if message.channel.is_private and not message.author.bot:

                if message.content.startswith('!help'):
                    text = '''
This bot allows you to easily manage and connect to your node(s) neighbors.

**Public commands:**

`!ictinder`
Start a DM session with this bot

**DM Only commands:**

`!register`
Register your Discord account once to retreive a password for Ictinder, this password is only sent once!

`!listnodes`
Show all your nodes connected

`!delnode <address>:<port>`
Remove the node listed under the given address/port combination, this will inform this nodes neighbors as well!

                    '''
                    await client.send_message(message.author, text)

                if message.content.startswith('!delnode'):
                    api = IctApi()
                    address = message.content.split(' ')[1]
                    result = api.remove_node(str(message.author.id), address)

                    if not result.get('success'):
                        text = 'Something went wrong while removing this node: {}'.format(result.get('error', 'Please contact @Dave#3333'))
                    else:
                        text = 'The node with the address `{}` has been removed!'.format(address)

                    await client.send_message(message.author, text)

                if message.content.startswith('!listnodes'):
                    api = IctApi()
                    result = api.list_nodes(str(message.author.id))

                    if not result.get('success'):
                        text = 'Something went wrong while listing your nodes: {}'.format(result.get('error', 'Please contact @Dave#3333'))
                    else:
                        if not result.get('nodes'):
                            text = 'No nodes found yet, register your node using the auto peering IXI!'
                        else:
                            text = 'Your registered nodes:\n\n'
                            for node in result.get('nodes'):
                                text += ' - `{}`\n'.format(node)

                    await client.send_message(message.author, text)

                if message.content.startswith('!register'):
                    api = IctApi()
                    result = api.signup(str(message.author.id))

                    if not result.get('success'):
                        text = 'Something went wrong while registering: {}'.format(result.get('error', 'Please contact @Dave#3333'))
                        await client.send_message(message.author, text)
                    else:
                        text = 'Thank you for registering, you will need the following details to set up Ictinder:\n\n**Discord ID:** {}\n**Password:** {}'.format(message.author.id, result.get('password'))
                        await client.send_message(message.author, text)

            if not message.channel.is_private:
                if message.content.startswith('!ictinder'):
                    await client.delete_message(message)
                    await client.send_message(message.author, 'Hey {}, Type !help in this DM for the available commands, you need to use `!register` here first if you have not done so to retreive the password you need for Ictinder.'.format(message.author.name))


        async def interval():
            await asyncio.sleep(3)
            
            server = client.get_server('397872799483428865')
            while True:
                for message in Message.objects.all():
                    user = server.get_member('{}'.format(message.discord_id))
                    await client.send_message(user, message.message)
                    message.delete()

                await asyncio.sleep(3)

        try:
            client.loop.run_until_complete(asyncio.gather(client.start(settings.DISCORD_TOKEN), interval()))
        except KeyboardInterrupt:
            client.loop.run_until_complete(client.logout())
        finally:
            client.loop.close()
