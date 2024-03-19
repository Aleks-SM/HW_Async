import datetime
import asyncio
import aiohttp
from more_itertools import chunked
from models import init_db, SwapiPeople, Session, engine


MAX_CHUNK = 10


async def get_person(client, person_id):
    http_response = await client.get(f"https://swapi.py4e.com/api/people/{person_id}")
    json_result = await http_response.json()
    return json_result


async def get_homeworld(client, url):
    http_response = await client.get(url)
    json_result = await http_response.json()
    result = json_result.get('name')
    return result


async def insert_to_db(list_of_json):
    models = [SwapiPeople(json=json_item) for json_item in list_of_json]
    async with Session() as session:
        session.add_all(models)
        await session.commit()


async def main():
    await init_db()
    client = aiohttp.ClientSession()
    for chunk in chunked(range(1, 100), MAX_CHUNK):
        coros = [get_person(client, person_id) for person_id in chunk]
        result = await asyncio.gather(*coros)
        # asyncio.create_task(insert_to_db(result))
        for i in range(len(result)):
            name_person = result[i].get('name')

            url_homeworld = result[i].get('homeworld')
            cor = get_homeworld(client, url_homeworld)
            homeworld = await asyncio.gather(cor)

            url_species = result[i].get('species')[0]
            cor1 = get_homeworld(client, url_species)
            species = await asyncio.gather(cor1)


            print('name_person', name_person)
            print('homeworld', homeworld)
            print('species', species)

    tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks_set)

    await client.close()
    await engine.dispose()


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
