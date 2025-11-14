import asyncio
import time

from aiohttp_client_cache import CachedSession

from valorant import Client


async def main() -> None:

    async with Client(enable_cache=True, cache_ttl=3600) as client:
        start_time = time.time()
        for _ in range(100):
            version = await client.fetch_version()
            # print('version:', version)

        end_time = time.time()
        print(f'Total time for 100 requests: {end_time - start_time:.2f} seconds')

        # version = await client.fetch_agents()
        # version = await client.fetch_agents()
        # version = await client.fetch_agents()
        # version = await client.fetch_agents()

        # session: CachedSession = client.http._session

        # print(session.cache.get_urls())
        # print(session.cache.responses.values())
        # async for value in session.cache.responses.values():
        #     print('value:', value)
        # async for url in session.cache.get_urls():
        #     print('url:', url)


if __name__ == '__main__':
    asyncio.run(main())

# Client(enable_cache=False, cache_path='./cache', cache_ttl=3600)
# from pathlib import Path

# print('Path.home()', Path.home())

# # import os
# # import platform
# # import sys

# # # from parsley import makeGrammar

# # grammar = """
# #     wsp ...
# #     """
# # tests = [
# #     'A',
# #     'A.B-C_D',
# #     'aa',
# #     'name',
# #     'name<=1',
# #     'name>=3',
# #     'name>=3,<2',
# #     'name@http://foo.com',
# #     "name [fred,bar] @ http://foo.com ; python_version=='2.7'",
# #     "name[quux, strange];python_version<'2.7' and platform_version=='2'",
# #     "name; os_name=='a' or os_name=='b'",
# #     # Should parse as (a and b) or c
# #     "name; os_name=='a' and os_name=='b' or os_name=='c'",
# #     # Overriding precedence -> a and (b or c)
# #     "name; os_name=='a' and (os_name=='b' or os_name=='c')",
# #     # should parse as a or (b and c)
# #     "name; os_name=='a' or os_name=='b' and os_name=='c'",
# #     # Overriding precedence -> (a or b) and c
# #     "name; (os_name=='a' or os_name=='b') and os_name=='c'",
# # ]


# # def format_full_version(info):
# #     version = f'{info.major}.{info.minor}.{info.micro}'
# #     kind = info.releaselevel
# #     if kind != 'final':
# #         version += kind[0] + str(info.serial)
# #     return version


# # if hasattr(sys, 'implementation'):
# #     implementation_version = format_full_version(sys.implementation.version)
# #     implementation_name = sys.implementation.name
# # else:
# #     implementation_version = '0'
# #     implementation_name = ''

# # bindings = {
# #     'implementation_name': implementation_name,
# #     'implementation_version': implementation_version,
# #     'os_name': os.name,
# #     'platform_machine': platform.machine(),
# #     'platform_python_implementation': platform.python_implementation(),
# #     'platform_release': platform.release(),
# #     'platform_system': platform.system(),
# #     'platform_version': platform.version(),
# #     'python_full_version': platform.python_version(),
# #     'python_version': '.'.join(platform.python_version_tuple()[:2]),
# #     'sys_platform': sys.platform,
# #     'sys.abi_features': sys.abiflags,
# # }
# # print(bindings)
