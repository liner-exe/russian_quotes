import aiohttp
import requests
from . import exceptions
from .languages import Languages
from .formats import Formats
from typing import Union, Dict, Tuple
                
async def get_quote_async(lang: Languages = Languages.ENGLISH, as_dict: bool = False) -> Union[Dict, Tuple]:
    """
    Get random quote on russian from forismatic API.

    Parameters:
        - lang `Languages`\n
            If Languages.ENGLISH returns quote in English\n
            If Languages.RUSSIAN returns quote in Russian
        - as_dict `bool`\n
            If True returns dict\n
            If False returns tuple

    Returns: `Union[Dict, Tuple]`

    Raises:
        `ServerError`
            Returns when server status isn\`t 200.

        `LanguageIsNotSupported`
            Returns when lang isn`t Languages.ENGLISH or Languages.RUSSIAN'
    """
    if lang not in Languages:
        raise exceptions.LanguageIsNotSupported('This language is not supported (Russian or English only).')

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={lang.value}') as response:
            if response.status == 200:
                data = await response.json()

                if as_dict:
                    return data

                return data['quoteText'], data['quoteAuthor']
            else:
                raise exceptions.ServerError(f'Server isn`t responding. Status code: {response.status}')
    
def get_quote(
    lang: Languages = Languages.ENGLISH,
    as_dict: bool = False,
    format: str = Formats.JSON,
    key: int = None
) -> Union[Dict, Tuple]:
    """
    Get random quote on russian from forismatic API.

    Parameters:
        - lang `Languages`\n
            If Languages.ENGLISH returns quote in English\n
            If Languages.RUSSIAN returns quote in Russian
        - as_dict `bool`\n
            If True returns dict\n
            If False returns tuple

    Returns: `Union[Dict, Tuple]`

    Raises:
        `ServerError`
            Returns when server status isn\`t 200.

        `LanguageIsNotSupported`
            Returns when lang isn`t Languages.ENGLISH or Languages.RUSSIAN'
    """
    if lang not in Languages:
        raise exceptions.LanguageIsNotSupported('This language is not supported (Russian or English only).')
    
    if 1 > key > 999999:
        raise exceptions.QuoteKeyError('Improper key passed.')
    
    params = {
        "method": "getQuote",
        "format": format,
        "lang": lang.value,
    }

    if key:
        params['key'] = key
    
    response = requests.get('https://api.forismatic.com/api/1.0/', params=params)

    if response.status_code == 200:
        if format == Formats.JSON:
            data = response.json()
        elif format in (Formats.XML, Formats.TEXT, Formats.HTML):
            data = response.text
        
        if format == Formats.JSON and "quoteText" in data and "quoteAuthor" in data:
            if as_dict:
                return data
            return data['quoteText'], data['quoteAuthor']
        
        return data
    else:
        raise exceptions.ServerError(f'Server isn`t responding. Status code: {response.status}')
