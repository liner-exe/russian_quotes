[![Downloads](https://static.pepy.tech/badge/russian-quotes)](https://pepy.tech/project/russian-quotes)
[![Downloads](https://static.pepy.tech/badge/russian-quotes/month)](https://pepy.tech/project/russian-quotes)
[![Downloads](https://static.pepy.tech/badge/russian-quotes/week)](https://pepy.tech/project/russian-quotes)

# russian_quotes

## Установка
```shell
pip install russian-quotes
```

## Примеры использования
* синхронный
```py
from russian_quotes import get_quote

text, author = get_quote()

print(f'Text: {text} Author: {author}')
```
* асинхронный
```py
import asyncio
from russian_quotes import get_quote_coro


async def main():
    return await get_quote_coro()

text, author = asyncio.run(main())

print(f'Text: {text} Author: {author}')
```
* ловля ошибки
```py
import russian_quotes

try:
    text, author = russian_quotes.get_quote()

    print(text, author)

except russian_quotes.ServerError:
    print('not works')
```

## Зависимости

[Python >=3.10](https://www.python.org/downloads/release/python-310)

## Лицензия

[MIT](http://en.wikipedia.org/wiki/MIT_License)
