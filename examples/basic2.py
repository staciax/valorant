import asyncio

import valorant


async def main() -> None:
    client = valorant.Client()
    async with client:
        # agent
        agents = await client.fetch_agents()
        for agent in agents:
            print(agent.display_name)
            # role = agent.role
            # print(role.display_name)
            # print(role.display_icon)

            print(agent.display_icon)
            print(agent.display_icon_small)
            print(agent.full_portrait_v2)

            # grenade = agent.get_ability(valorant.AbilitySlot.grenade)
            # if grenade is not None:
            #     print(grenade.display_name)

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

        # skin child of weapon

        skins = await client.fetch_weapon_skins()
        for skin in skins:
            # weapon = skin.parent
            print(weapon.display_name, skin.display_name)

        # skin level child of skin

        skin_levels = await client.fetch_weapon_skin_levels()
        for level in skin_levels:
            # skin = level.parent
            # weapon = skin.parent
            # print(skin.display_name, str(level.display_name).strip())
            print(level.display_icon)

        # skin chroma child of skin
        skin_chromas = await client.fetch_weapon_skin_chromas()
        for chroma in skin_chromas:
            # skin = chroma.parent
            # weapon = skin.parent
            # print(weapon.display_name, skin.display_name, str(chroma.display_name).strip())
            print(chroma.display_icon)


asyncio.run(main())
