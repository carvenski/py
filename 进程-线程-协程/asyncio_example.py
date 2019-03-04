import asyncio

async def co1():
    print('Hello ...1')
    await asyncio.sleep(1)
    print('...1 World!')


async def co2():
    print('Hello ...2')
    await asyncio.sleep(1)
    print('...2 World!')


async def co3():
    print('Hello ...3')
    await asyncio.sleep(1)
    print('...3 World!')

futures = [co1(), co2(), co3()]

print("all coroutines ready, loop started...")
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))  # wait until all coroutines finished.
loop.close()
print("all coroutines finished, loop stopped...")



