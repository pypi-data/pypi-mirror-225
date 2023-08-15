from aiohttp import ClientResponse, ClientSession

from awakatime.utils import encode_base64


class Awakatime:
    """Wakatime API client.

    Class that contains the ways to integrate with the Wakatime API.

    Attributes:
        base_url (str): Base URL for the API.
        api_key (str): Encoded API key.
        session (aiohttp.ClientSession): HTTP session.
    """

    base_url = "https://wakatime.com"

    def __init__(self, api_key: str):
        """Initialize a new Wakatime client.

        Transform the API key into a base64 encoded string.

        Args:
            api_key (str): API key to use.
        """
        self.api_key = encode_base64(api_key)
        self.session = ClientSession(self.base_url)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()

    async def request(self, method: str, endpoint: str, **kwargs) -> ClientResponse:
        """Make a request to the WakaTime API.

        This method is a coroutine.

        Args:
            method (str): HTTP method to use.
            endpoint (str): API endpoint to use.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            The response from the API.

        Raises:
            aiohttp.ClientResponseError: If the response status code is not 2xx.
        """
        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json",
        }
        return await self.session.request(
            method,
            endpoint,
            headers=headers,
            raise_for_status=True,
            **kwargs,
        )

    async def get_all_time(self, user: str = "current", **kwargs) -> dict:
        """Get total time logged for the user.

        This method is a coroutine.

        See https://wakatime.com/developers#all_time_since_today for more information.

        Args:
            user (str, optional): Wakatime user to get the data from.

        Keyword Args:
            project (str, optional): Project name to filter by.

        Returns:
            All time logged for the user.

        Raises:
            KeyError: If the response JSON is missing the "data" key.
            aiohttp.ClientResponseError: If the response status code is not 2xx.
        """
        endpoint = f"/api/v1/users/{user}/all_time_since_today"

        response = await self.request("GET", endpoint, params=kwargs)
        response_data = await response.json()
        return response_data["data"]

    async def get_commits(self, project: str, user: str = "current", **kwargs) -> list[dict]:
        """Get commits for a WakaTime project.

        This method is a coroutine.

        See https://wakatime.com/developers#commits for more information.

        Args:
            project (str): Project name to get the data from.
            user (str, optional): Wakatime user to get the data from.

        Keyword Args:
            author (str, optional): Author name to filter by.
            branch (str, optional): Branch name to filter by.
            page (int, optional): Page number to get.

        Returns:
            List of project commits.

        Raises:
            aiohttp.ClientResponseError: If the response status code is not 2xx.
        """
        endpoint = f"/api/v1/users/{user}/projects/{project}/commits"

        response = await self.request("GET", endpoint, params=kwargs)
        return await response.json()  # a resposta é direta

    async def get_projects(self, user: str = "current", **kwargs) -> list[dict]:
        """Get all projects logged for the user.

        This method is a coroutine.

        See https://wakatime.com/developers#projects for more information.

        Args:
            user (str, optional): Wakatime user to get the data from.

        Keyword Args:
            q (str, optional): Filter projects by name.

        Returns:
            List of projects.

        Raises:
            KeyError: If the response JSON is missing the "data" key.
            aiohttp.ClientResponseError: If the response status code is not 2xx.
        """
        endpoint = f"/api/v1/users/{user}/projects"

        response = await self.request("GET", endpoint, params=kwargs)
        response_data = await response.json()
        return response_data["data"]

    async def get_machines(self, user: str = "current") -> list[dict]:
        """Get all machines data logged for the user.

        This method is a coroutine.

        See https://wakatime.com/developers#machine_names for more information.

        Args:
            user (str, optional): Wakatime user to get the data from.

        Returns:
            List of user machines data.

        Raises:
            KeyError: If the response JSON is missing the "data" key.
            aiohttp.ClientResponseError: If the response status code is not 2xx.
        """
        endpoint = f"/api/v1/users/{user}/machine_names"

        response = await self.request("GET", endpoint)
        response_data = await response.json()
        return response_data["data"]

    async def close(self):
        await self.session.close()
