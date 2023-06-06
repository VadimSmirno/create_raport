import asyncio
from pprint import pprint
from dadata import DadataAsync
from bot import token_dadata
from bot import secret


async def get_address(city:str) -> list:
    async with DadataAsync(token_dadata, secret) as dadata:
        response = await dadata.suggest('address', city, count=3)
        locality_information = [[value['value']] for value in response]
        return locality_information
        # pprint(response)
        # for i in response:
        #     print(
        #           i['data']['city_with_type'],
        #           i['data']['region_with_type'],
        #           i['data']['settlement_with_type'],
        #           i['data']['area_with_type']
        #     )

#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(get_address(''))



