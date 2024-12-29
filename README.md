# valorant
A modern, easy to use, feature-rich, and async ready API wrapper for [Valorant API](https://valorant-api.com) written in Python.

## Key Features
- Modern Pythonic API using `async` and  `await`.

## Installing
Python 3.10 or higher is required

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


async def main() -> None:
    client = valorant.Client()

    async with client:
        weapons = await client.fetch_weapons()
        for weapon in weapons:
            print(weapon.display_name)
            print(weapon.display_name.ja_JP)
            print(weapon.display_name.japanese)
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