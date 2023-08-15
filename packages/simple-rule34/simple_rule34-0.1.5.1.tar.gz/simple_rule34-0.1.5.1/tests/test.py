from SimpleRule34.src.SimpleRule34.aio.ARule34 import Rule34Api
import asyncio


async def main():

    r = Rule34Api()

    lis = await r.get_post_list(tags='1girl', limit=5, forbidden_tags=['male'])

    print(lis)

    for x in lis:
        print(x)

    return


if __name__ == '__main__':
    asyncio.run(main())