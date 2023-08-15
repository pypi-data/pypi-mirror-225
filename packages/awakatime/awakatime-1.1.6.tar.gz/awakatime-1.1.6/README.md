<div align="center">
    <h1>🔃 Awakatime</h1>
    <p>An asynchronous API wrapper for Wakatime</p>
    <a href="https://wakatime.com/badge/github/controlado/awakatime">
        <img src="https://wakatime.com/badge/github/controlado/awakatime.svg" alt="wakatime">
    </a>
    <a href="https://discordapp.com/users/854886148455399436">
        <img src="https://dcbadge.vercel.app/api/shield/854886148455399436?style=flat" alt="discord">
    </a>
    <br>
    <a href="https://github.com/controlado/awakatime/issues/new">
        <img src="https://img.shields.io/badge/Report%20a%20bug-gray" alt="report">
    </a>
    <a href="https://awakatime.readthedocs.io/en/latest/?badge=latest">
        <img src="https://readthedocs.org/projects/awakatime/badge/?version=latest" alt="documentation">
    </a>
    <a href="README.md">
        <img src="https://img.shields.io/badge/English-bright" alt="english">
    </a>
    <a href="README.br.md">
        <img src="https://img.shields.io/badge/Português-bright" alt="português">
    </a>
    <br>
    <a href="https://codecov.io/gh/controlado/awakatime">
        <img src="https://codecov.io/gh/controlado/awakatime/branch/main/graph/badge.svg?token=86DTBWW41H">
    </a>
    <a href="https://pypi.org/project/awakatime/">
        <img src="https://img.shields.io/pypi/v/awakatime?color=red" alt="pypi">
    </a>
    <img src="https://img.shields.io/github/license/controlado/awakatime?color=red" alt="license">
</div>

## Installation

```bash
pip install awakatime
```

## Usage

It"s recommended to use a context manager to create an instance of the client.

```python
import asyncio

from awakatime import Awakatime


async def main():
    async with Awakatime("your_api_key") as awakatime:
        tasks = [awakatime.get_all_time(), awakatime.get_projects()]
        all_time, projects = await asyncio.gather(*tasks)
        print(all_time)
        print(projects)


if __name__ == "__main__":
    coro = main()
    asyncio.run(coro)
```

## Development

Make sure you have [Poetry](https://python-poetry.org/) installed.

```bash
git clone https://github.com/controlado/awakatime.git
cd awakatime
poetry install --with dev
```