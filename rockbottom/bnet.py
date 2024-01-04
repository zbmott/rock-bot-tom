import aiohttp, datetime


class BNet:
    def __init__(self, client_id, client_secret, locale='en_US'):
        self.session = aiohttp.ClientSession()
        self.client_id = client_id
        self.locale = locale
        self.base_url = 'https://us.api.blizzard.com'
        self.client_secret = client_secret
        self.expires_at = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def authenticate(self):
        url = 'https://oauth.battle.net/token'
        auth = aiohttp.BasicAuth(self.client_id, self.client_secret)
        async with self.session.post(url, data={'grant_type': 'client_credentials'}, auth=auth) as resp:
            data = await resp.json()

            self.session._default_headers['Authorization'] = f"Bearer {data['access_token']}"
            self.expires_at = datetime.datetime.now() + datetime.timedelta(seconds=data['expires_in'])

    async def _do_request(self, path, method='GET', params=None):
        params = params or {}
        params['locale'] = self.locale

        if self.expires_at is None or self.expires_at <= datetime.datetime.now():
            await self.authenticate()

        async with self.session.request(method, self.base_url + path, params=params) as response:
            return await response.json()

    async def auction_house_index(self, realm_id):
        return await self._do_request(f"/data/wow/connected-realm/{realm_id}/auctions/index", params={'namespace': 'dynamic-classic1x-us'})

    async def auctions(self, realm_id, auction_house_id):
        return await self._do_request(f"/data/wow/connected-realm/{realm_id}/auctions/{auction_house_id}", params={'namespace': 'dynamic-classic1x-us'})

    async def class_index(self):
        return await self._do_request('/data/wow/playable-class/index', params={'namespace': 'static-classic1x-us'})

    async def class_detail(self, class_id):
        return await self._do_request(f"/data/wow/playable-class/{class_id}", params={'namespace': 'static-classic1x-us'})

    async def connected_realms_index(self):
        return await self._do_request('/data/wow/connected-realm/index', params={'namespace': 'dynamic-classic1x-us'})

    async def item_detail(self, item_id):
        return await self._do_request(f"/data/wow/item/{item_id}", params={'namespace': 'static-classic1x-us'})

    async def guild_roster(self, realm_slug, guild_slug):
        return await self._do_request(f"/data/wow/guild/{realm_slug}/{guild_slug}/roster", params={'namespace': 'profile-classic1x-us'})

    async def character_summary(self, realm_slug, character_name):
        return await self._do_request(f"/profile/wow/character/{realm_slug}/{character_name}", params={'namespace': 'profile-classic1x-us'})

    async def character_equipment(self, realm_slug, character_name):
        return await self._do_request(f"/profile/wow/character/{realm_slug}/{character_name}/equipment", params={'namespace': 'profile-classic1x-us'})

    async def character_specializations(self, realm_slug, character_name):
        return await self._do_request(f"/profile/wow/character/{realm_slug}/{character_name}/specializations", params={'namespace': 'profile-classic1x-us'})