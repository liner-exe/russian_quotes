import aiohttp
import requests
from . import exceptions
from .languages import Language
from .formats import Format
from typing import Union, Dict, Tuple
                
async def get_quote_async(lang: Language = Language.ENGLISH, as_dict: bool = False) -> Union[Dict, Tuple]:
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
    if lang not in Language:
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
    lang: Language = Language.ENGLISH,
    as_dict: bool = False,
    format: str = Format.JSON,
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
    if not isinstance(lang, Language):
        raise TypeError(f'You must pass lang with enum Languages. Not with {type(lang)}')
    
    if not isinstance(format, Format):
        raise TypeError(f'You must pass format with enum Formats. Not with {type(format)}')
    
    if key and not (1 <= key <= 999999):
        raise exceptions.QuoteKeyError('Improper key passed.')
    
    params = {
        "method": "getQuote",
        "format": format.value,
        "lang": lang.value,
    }

    if key:
        params['key'] = key
    
    response = requests.get('https://api.forismatic.com/api/1.0/', params=params)

    if response.status_code == 200:
        if format == Format.JSON:
            data = response.json()

            if as_dict:
                return data
            return data['quoteText'], data['quoteAuthor']
        
        elif format in (Format.XML, Format.TEXT, Format.HTML):
            data = response.text
        
        return data
    else:
        raise exceptions.ServerError(f'Server isn`t responding. Status code: {response.status}')
