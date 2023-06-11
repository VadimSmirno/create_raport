import asyncio
from dadata import DadataAsync
from bot import token_dadata
from bot import secret
from logging_dir.log import logger


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
        return list_settlements


