import datetime
import asyncio
import aiohttp
from more_itertools import chunked
from models import init_db, SwapiPeople, Session, engine


MAX_CHUNK = 10


async def get_person(client, person_id):
    http_response = await client.get(f"https://swapi.py4e.com/api/people/{person_id}")
    if http_response.status == 404:
        return
    else:
        # print(http_response.status)
        json_result = await http_response.json()
    return json_result


async def get_data(client, url_list, key):
    list_data = []
    if type(url_list) is str:
        url_list = [url_list]
    for url in url_list:
        http_response = await client.get(url)
        json_result = await http_response.json()
        list_data.append(json_result.get(key))
    result = ', '.join(list_data)
    return result


async def insert_to_db(list_of_json):
    models = [SwapiPeople(**data) for data in list_of_json]
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
        if None in result:
            result.remove(None)
        for i in range(len(result)):
            try:
                result[i].pop('edited', 'Key not found')
                result[i].pop('created', 'Key not found')
                result[i].pop('url', 'Key not found')
                # del result[i]['url']

                person_name = result[i].get('name')
                if 'vehicles' in result[i]:
                    result[i]['vehicles'] = await get_data(client, result[i].get('vehicles'), 'name')
                if 'starships' in result[i]:
                    result[i]['starships'] = await get_data(client, result[i].get('starships'), 'name')
                if 'films' in result[i]:
                    result[i]['films'] = await get_data(client, result[i].get('films'), 'title')
                if 'species' in result[i]:
                    result[i]['species'] = await get_data(client, result[i].get('species'), 'name')
                if 'homeworld' in result[i]:
                    result[i]['homeworld'] = await get_data(client, result[i].get('homeworld'), 'name')
            except Exception:
                pass

            print('i = ', i, result[i])
        asyncio.create_task(insert_to_db(result))

        tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
        await asyncio.gather(*tasks_set)

    await client.close()
    await engine.dispose()


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
