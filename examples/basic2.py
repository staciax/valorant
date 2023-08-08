import asyncio

import valorant


async def main():
    client = valorant.Client(valorant.Locale.american_english)  # set default locale to thai
    async with client:
        # agent
        for agent in client.agents:
            print(agent.display_name)  # default locale
            role = agent.role
            print(role.display_name)
            print(role.display_icon)

            print(agent.display_icon)
            print(agent.display_icon_small)
            print(agent.full_portrait_v2)

            grenade = agent.get_ability(valorant.AbilityType.grenade)
            if grenade is not None:
                print(grenade.display_name)

        # buddy
        for buddy in client.buddies:
            print(buddy.display_name)
            print(buddy.display_icon)
            print(buddy.levels)

        # player card
        for player_card in client.player_cards:
            print(player_card.display_name)
            print(player_card.display_icon)
            print(player_card.large_art)
            print(player_card.wide_art)
            print(player_card.small_art)

        # weapon

        for weapon in client.weapons:
            print(weapon.display_name)
            for skin in weapon.skins:
                print(skin.display_name)
                for level in skin.levels:
                    print(level.display_name)
                for chroma in skin.chromas:
                    print(chroma.display_name)

        # skin child of weapon

        for skin in client.skins:
            weapon = skin.parent
            print(weapon.display_name, skin.display_name)

        # skin level child of skin

        for level in client.skin_levels:
            skin = level.parent
            weapon = skin.parent
            print(skin.display_name, str(level.display_name).strip())
            print(level.display_icon)

        # skin chroma child of skin

        for chroma in client.skin_chromas:
            skin = chroma.parent
            weapon = skin.parent
            print(weapon.display_name, skin.display_name, str(chroma.display_name).strip())
            print(chroma.display_icon)


asyncio.run(main())
