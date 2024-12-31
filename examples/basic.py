import asyncio

import valorant
from valorant.models.localization import LocalizedField


async def main() -> None:
    client = valorant.Client()
    async with client:
        weapon = await client.fetch_weapon(
            '9c82e19d-4575-0200-1a81-3eacf00cf872',  # Vandal
            language='all',  # all languages (LocalizedField)
        )  # Vandal
        assert weapon is not None

        for skin in weapon.skins[:5]:
            print(skin.display_name)
            print(skin.display_icon)

            # display_name locale
            assert skin.display_name is not None
            assert isinstance(skin.display_name, LocalizedField)
            print(skin.display_name.ja_JP)
            print(skin.display_name.japanese)

            skin_theme = await skin.fetch_theme(client=client)
            if skin_theme is not None:
                print(skin_theme.display_name)
                print(skin_theme.display_icon)

            skin_content_tier = await skin.fetch_content_tier(client=client)
            if skin_content_tier is not None:
                print(skin_content_tier.display_name)
                print(skin_content_tier.display_icon)

            for level in skin.levels:
                print(level.display_name)
            for chroma in skin.chromas:
                print(chroma.display_name)

            print('-' * 40)


asyncio.run(main())
