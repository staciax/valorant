# valorant
A modern, easy to use, feature-rich, and async ready API wrapper for Valorant API written in Python.

## Key Features
- Modern Pythonic API using `async` and  `await`.

## Installing
Python 3.8 or higher is required

Windows: <br>
```
$ pip install -U valorant.py
```
Linux/MacOS:
```
$ python3 -m pip install -U valorant.py
```
 
## Quick Example
```py
import asyncio
import valorant

async def main():
    client = valorant.Client(valorant.Locale.thai)  # set default locale to thai
    async with client:
        weapon = client.get_weapon('9c82e19d-4575-0200-1a81-3eacf00cf872')  # Vandal
        assert weapon is not None

        for skin in weapon.skins:
            print(skin.display_name)  # default locale
            print(skin.display_icon)

            # specify locale
            print(skin.display_name.ja_JP)
            print(skin.display_name.japanese)
            print(skin.display_name.from_locale(valorant.Locale.japanese))

            if skin.theme is not None:
                print(skin.theme.display_name)
                print(skin.theme.display_icon)

            if skin.content_tier is not None:
                print(skin.content_tier.display_name)
                print(skin.content_tier.display_icon)

            for level in skin.levels:
                print(level.display_name)
            for chroma in skin.chromas:
                print(chroma.display_name)


asyncio.run(main())
```


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project inspired by
- [discord.py](https://github.com/Rapptz/discord.py) the Discord API wrapper for Python. 

<!-- ## Support
- [Discord Server](https://discord.com/invite/) -->

## Links
- [Valorant API](https://valorant-api.com)
- [Official Discord Server](https://discord.com/invite/9V5MWgD)