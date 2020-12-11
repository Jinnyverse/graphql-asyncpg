import time


async def insert(info, *args):
    async with info.context["db"].acquire() as database:
        await database.execute("INSERT INTO users(id, email, company) VALUES ($1, $2, $3);", str(args[0]), "james@doe.com", False)
        return


async def insertMany(info, *args):
    async with info.context["db"].acquire() as database:
        async with database.transaction():
            await database.executemany("INSERT INTO dummy(id, email, company) VALUES ($1, $2, $3);", args[0])


async def select_all(info, *args):
    async with info.context["db"].acquire() as database:
        rows = await database.fetch("SELECT * FROM dummy")
        return [dict(row) for row in rows]


async def insert_thousand(root, info, id):
    numbers = []
    temp = []
    for x in range(100000):
        temp.append(x)
        if len(temp) == 3:
            numbers.append(temp.copy())
            temp.clear()
    tic = time.perf_counter()
    await insertMany(info, numbers)
    tock = time.perf_counter()
    return f"Took {tock-tic} seconds"


async def get_all(root, info):
    tic = time.perf_counter()
    rows = await select_all(info)
    tock = time.perf_counter()
    print(tock-tic)
    return rows


async def hello(info, query, *args):
    return "Hello"
