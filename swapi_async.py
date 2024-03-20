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


async def get_data(client, url, key):
    http_response = await client.get(url)
    json_result = await http_response.json()
    result = json_result.get(key)
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

            films = []
            if 'films' in result[i]:
                url_films = result[i].get('films')
                for j in url_films:
                    cor = get_data(client, j, 'title')
                    res = await asyncio.gather(cor)
                    films.append(*res)

            species = []
            if 'species' in result[i]:
                url_species = result[i].get('species')
                for j in url_species:
                    cor = get_data(client, j, 'name')
                    res = await asyncio.gather(cor)
                    species.append(*res)

            homeworld = []
            if 'homeworld' in result[i]:
                # url_homeworld = result[i].get('homeworld')
                cor = get_data(client, result[i].get('homeworld'), 'name')
                res = await asyncio.gather(cor)
                homeworld.append(*res)

            print('name_person: ', name_person)
            print('homeworld: ', *homeworld)
            print('films: ', ', '.join(films))
            print('species: ', ', '.join(species))

    tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks_set)

    await client.close()
    await engine.dispose()


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
