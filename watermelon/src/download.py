import httpx


class Downloader(httpx.Client):
    def __init__(
        self,
        url: str = None,
        api_key: str = None,
    ) -> None:
        super(Downloader, self).__init__(
            base_url=url,
            headers={
                "Content-Type": "application/json",
            },
            timeout=30,
        )

        self.query_params = {"apiKey": api_key}

    def get_all_audio_files(self):
        response: httpx.Response = self.get(f"/api/getMp3s", params=self.query_params)

        if response.status_code != 200:
            raise Exception(response.json())

        return response.json()

    def download_file(self, link: str = None):
        body = {
            "url": link,
            "type": "audio",
            "cropFileSettings": {"cropFileStart": 0, "cropFileEnd": 0},
        }

        response: httpx.Response = self.post(
            f"/api/downloadFile", json=body, params=self.query_params
        )

        if response.status_code != 200:
            raise Exception(response.json())

        return True
