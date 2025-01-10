# valorant
An API wrapper for [Valorant API](https://valorant-api.com) written in Python.

## Features
- Supports all endpoints. (includes undocumented endpoints)
- Fully type annotated.
- [Pydantic V2](https://docs.pydantic.dev/latest/) models.
- Supports Python 3.10+.
- Supports all languages.
<!-- TODO: supports caching -->
<!-- - Modern Pythonic API using `async` and  `await`. -->

## Installing
To install the library, you can just run the following command:
```
# uv
uv add valorant.py

# pip
pip install valorant.py
```
 
## Quick Example
```py
import asyncio
import valorant


async def main() -> None:
    async with valorant.Client() as client:
        weapons = await client.fetch_weapons()
        for weapon in weapons:
            print(weapon.display_name)
            print(weapon.display_icon)


asyncio.run(main())
```


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<!-- ## Project inspired by
- [discord.py](https://github.com/Rapptz/discord.py) the Discord API wrapper for Python.  -->

<!-- ## Support
- [Discord Server](https://discord.com/invite/) -->

## Links
- [Valorant API](https://valorant-api.com)
- [Official Discord Server](https://discord.com/invite/9V5MWgD)