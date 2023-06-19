import asyncio
from dadata import DadataAsync
from bot import token_dadata
from bot import secret



async def get_address(city:str) -> list:
    async with DadataAsync(token_dadata, secret) as dadata:
        response = await dadata.suggest('address', city, count=3)
        locality_information = [[value['value']] for value in response]
        return locality_information



async def get_itinerary(city: str)->list:
    async with DadataAsync(token_dadata,secret) as dadata:
        response = await dadata.suggest('address', city, count=1)
        list_settlements = [
            value['data']['settlement_with_type']
             if value['data']['settlement_with_type'] != None
             else value['data']['city_with_type']
            for value in response]
        if list_settlements == [None]:
            return ['Не нашел']
        return list_settlements

# async def main():
#     result = await get_itinerary('')
#     print(result)
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())