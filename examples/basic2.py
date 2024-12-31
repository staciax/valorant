import asyncio

import valorant
from valorant.enums import Language


async def main() -> None:
    client = valorant.Client()
    async with client:
        # agent
        agents = await client.fetch_agents(language=Language.japanese)
        for agent in agents[:1]:
            if agent.role is not None:
                print(agent.role.display_name)
                print(agent.role.display_icon)

        # buddy
        buddies = await client.fetch_buddies()
        for buddy in buddies:
            print(buddy.display_name)
            print(buddy.display_icon)
            print(buddy.levels)

        # player card
        player_cards = await client.fetch_player_cards()
        for player_card in player_cards:
            print(player_card.display_name)
            print(player_card.display_icon)
            print(player_card.large_art)
            print(player_card.wide_art)
            print(player_card.small_art)

        # weapon
        weapons = await client.fetch_weapons()
        for weapon in weapons:
            print(weapon.display_name)
            for skin in weapon.skins:
                print(skin.display_name)
                for level in skin.levels:
                    print(level.display_name)
                for chroma in skin.chromas:
                    print(chroma.display_name)

        # skin

        skins = await client.fetch_skins()
        for skin in skins:
            print(skin.display_name)

        # skin level

        skin_levels = await client.fetch_skin_levels()
        for level in skin_levels:
            print(level.display_name)

        # skin chroma
        skin_chromas = await client.fetch_skin_chromas()
        for chroma in skin_chromas:
            print(chroma.display_name)


asyncio.run(main())
