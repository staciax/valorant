import asyncio

from valorant.http import HTTPClient


async def main() -> None:
    http = HTTPClient()
    await http.start()

    # agents

    agents_response = await http.get_agents(language='ja-JP')
    agents = agents_response['data']
    for agent in agents:
        print(agent['displayName'])

        role = agent['role']
        print(role['displayName'])
        print(role['displayIcon'])

        print(agent['displayIcon'])
        print(agent['displayIconSmall'])
        print(agent['fullPortrait'])

        abilities = agent['abilities']
        for ability in abilities:
            print(ability['displayName'])

    await http.close()


if __name__ == '__main__':
    asyncio.run(main())
