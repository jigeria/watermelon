import httpx


class Player(httpx.Client):
    def __init__(
        self,
        url: str = None,
        username: str = "admin",
        password: str = "admin",
    ) -> None:
        body: dict = {"username": username, "password": password}

        response: httpx.Response = httpx.post(
            f"{url}/login",
            json=body,
        )

        # retry login
        if response.status_code != 200:
            raise ValueError("Bad credentials")

        print(response.json()["user"]["token"])
        super(Player, self).__init__(
            base_url=url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"""Token {response.json()['user']['token']}""",
            },
            timeout=30,
        )

    def get_all_libraries(self):
        response: httpx.Response = self.get(f"/api/libraries")

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_item_in_libraries(self, lib_id: str = None):
        response: httpx.Response = self.get(f"/api/items/{lib_id}?expanded=1")

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def match_all_library_items(self, lib_id: str = None):
        response: httpx.Response = self.get(f"/api/libraries/{lib_id}/matchall")

        if response.status_code != 200:
            raise Exception(response.content)

        print(response.content)

    def scan_library(self, lib_id: str = None):
        response: httpx.Response = self.post(f"/api/libraries/{lib_id}/scan")

        if response.status_code != 200:
            raise Exception(response.content)

        print(response.content)
