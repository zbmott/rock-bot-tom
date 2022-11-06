import datetime, os

import discord

import messages


class Client(discord.Client):
    def __init__(self, *pos, **kw):
        super().__init__(*pos, **kw)

        self.awaiting_nickname = {}

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print('-----')

        self.audit_channel = discord.utils.get(client.get_all_channels(), guild__name='Rock Bottom', name='audit-log')

    async def update_nickname(self, member, nickname):
        if member.id not in self.awaiting_nickname:
            return

        if datetime.timedelta(minutes=30) < datetime.datetime.now() - self.awaiting_nickname[member.id]['timestamp']:
            return

        member = self.awaiting_nickname[member.id]['member']

        try:
            await member.edit(nick=nickname)
            await member.send(f"Thanks! I updated your nickname to `{nickname}` for you.")
            await self.audit_channel.send(f"I updated `{str(member)}'s` nickname to `{nickname}`.")
        except discord.errors.Forbidden:
            pass

        del self.awaiting_nickname[member.id]

    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            await self.update_nickname(message.author, message.content)

    async def on_member_update(self, before, after):
        new_roles = list(map(lambda r: r.name, set(after.roles) - set(before.roles)))

        for role in new_roles:
            if role == 'Guest':
                self.awaiting_nickname[before.id] = {
                    'timestamp': datetime.datetime.now(),
                    'member': before
                }
            try:
                await before.send(messages.MESSAGES[role].strip())
            except KeyError:
                pass


intents = discord.Intents.default()
intents.members = True

client = Client(intents=intents)
client.run(os.environ['DISCORD_TOKEN'])
