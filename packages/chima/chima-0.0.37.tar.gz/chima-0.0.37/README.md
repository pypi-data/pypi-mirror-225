# Chima Python Library

[![pypi](https://img.shields.io/pypi/v/chima.svg)](https://pypi.python.org/pypi/chima)
[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)

## Documentation

API reference documentation is available [here](https://chima.docs.buildwithfern.com/api-reference/search).

## Installation

Add this dependency to your project's build file:

```bash
pip install chima
# or
poetry add chima
```

## Usage

```python
from chima.client import Chima

chima_client = Chima()

response = chima_client.search(group_id="group_id", query="Your query")

print(response)
```

## Async client

This SDK also includes an async client, which supports the `await` syntax:

```python
import asyncio
from chima.client import AsyncChima

chima_client = AsyncChima()

async def get_response() -> None:
    response = await chima_client.search(group_id="group_id")
    print(response)

asyncio.run(get_response())
```

## Streaming

Chima's streaming endpoint will return a Python generator that you can iterate over. 

```python
from chima.client import Chima

chima_client = Chima()

response = chima_client.stream(level_context="Some context.")

for chunk in response: 
    print(chunk)
```

## Beta status

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning the package version to a specific version in your lock file. This way, you can install the same version each time without breaking changes unless you are intentionally looking for the latest version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest [opening an issue](https://github.com/chima-org/chima-python/issues) first to discuss with us!

On the other hand, contributions to the README are always very welcome!

