import asyncio, json

import bnet, settings


async def main():
    roster = []

    async with bnet.BNet(settings.BNET_CLIENT_ID, settings.BNET_SECRET) as client:
        data = await client.guild_roster('chaos-bolt', 'clam-lords')

        for m in data['members']:
            await asyncio.sleep(0.5)
            if m['character']['level'] != 25:
                continue

            summary = await client.character_summary('chaos-bolt', m['character']['name'].lower())
            e = await client.character_equipment('chaos-bolt', m['character']['name'].lower())
            s = await client.character_specializations('chaos-bolt', m['character']['name'].lower())

            if summary.get('code', False):
                print(f"{m['character']['name']}: {summary['code']}")
                continue

            runes = []

            for item in e['equipped_items']:
                for enchant in item.get('enchantments', []):
                    if enchant['enchantment_slot'].get('type', None) == 'TEMPORARY':
                        runes.append(enchant['display_string'])

            spec = {}
            active_spec = s['specialization_groups'][0]['specializations']

            for tree in active_spec:
                spec[tree['specialization_name']] = tree['spent_points']

            roster.append({
                'name': m['character']['name'],
                'class': m['character']['playable_class']['id'],
                'avg_ilvl': summary['average_item_level'],
                'runes': runes,
                'spec': spec
            })

    with open('clam_lords_roster.json', 'w') as outfile:
        json.dump(roster, outfile, indent=2)


if __name__ == '__main__':
    asyncio.run(main())
