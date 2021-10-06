import asyncio
async def main():
    print ("Waiting 5 seconds. ")
    for _ in range(20):
        await asyncio.sleep(1)
        print (".")
    print ("Finished waiting.")
asyncio.run(main())