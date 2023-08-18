import requests
from pprint import pprint
from requests.auth import HTTPBasicAuth
from loguru import logger

from ocpy import OcPyRequestException
from ocpy.model.mediapackage import MediaPackage
from ocpy.api.api_client import OpenCastBaseApiClient


class SearchApi(OpenCastBaseApiClient):
    """Search API class.
    PLEASE NOTE: The search API is (usually) only available on the presentation node.
    (Which might or might not be the same as the admin node)!
    Args:
        OpenCastBaseApiClient (_type_): _description_
    """

    def __init__(self, user=None, password=None, server_url=None, **kwargs):
        super().__init__(user, password, server_url)
        self.base_url = server_url + "/search"
        if self.base_url and "admin" in self.base_url.lower():
            logger.warning(
                "Search API is usually only available on the presentation node! Requsets might fail!"
            )

    def get_episode(
        self,
        id: str = "",
        q: str = "",
        series_id: str = "",
        series_name: str = "",
        sort: str = "",
        limit: int = 20,
        offset: int = 0,
        admin: bool = False,
        sign: bool = True,
        format: str = "json",
        **kwargs,
    ):
        params = {
            "id": id,
            "q": q,
            "sid": series_id,
            "sname": series_name,
            "sort": sort,
            "limit": limit,
            "offset": offset,
            "admin": admin,
            "sign": sign,
        }
        res = requests.get(
            self.base_url + f"/episode.{format}",
            params=params,
            auth=HTTPBasicAuth(self.user, self.password),
            timeout=10,
            **kwargs,
        )
        if res.ok:
            if format == "json":
                return res.json()
            return res.text
        raise OcPyRequestException("could not get episode(s)!", response=res)

    def get_lucene(
        self,
        q: str = "",
        series: bool = False,
        sort: str = "",
        limit: int = 20,
        offset: int = 0,
        admin: bool = False,
        sign: bool = True,
        format="json",
        **kwargs,
    ):
        params = {
            "q": q,
            "series": series,
            "sort": sort,
            "limit": limit,
            "offset": offset,
            "admin": admin,
            "sign": sign,
        }

        res = requests.get(
            self.base_url + f"/lucene.{format}",
            auth=HTTPBasicAuth(self.user, self.password),
            params=params,
            timeout=10,
            **kwargs,
        )

        if res.ok:
            if format == "json":
                return res.json()
            return res.text
        raise OcPyRequestException("could not get response!", response=res)

    def get_series(
        self,
        id: str = "",
        q: str = "",
        episodes: bool = False,
        sort: str = "",
        limit: int = 20,
        offset: int = 0,
        admin: bool = False,
        sign: bool = True,
        format: str = "json",
        **kwargs,
    ):
        params = {
            "id": id,
            "q": q,
            "episodes": episodes,
            "sort": sort,
            "limit": limit,
            "offset": offset,
            "admin": admin,
            "sign": sign,
        }

        res = requests.get(
            self.base_url + f"/lucene.{format}",
            auth=HTTPBasicAuth(self.user, self.password),
            params=params,
            timeout=10,
            **kwargs,
        )

        if res.ok:
            if format == "json":
                return res.json()
            return res.text
        raise OcPyRequestException("could not get series!", response=res)

    def add_mediapackage(self, media_package_xml: str):
        url = self.base_url + "/add"
        data = {"mediapackage": media_package_xml}
       
        res = requests.post(
            url,
            data=data,
            auth=HTTPBasicAuth(self.user, self.password),
            timeout=10,
        )
        if res.ok:
            return MediaPackage(res.text)
        raise OcPyRequestException("could not get event!", response=res)

    def delete_mediapackage(self, mp_id: str):
        url = self.base_url + f"/{mp_id}"
        res = requests.delete(
            url,
            auth=HTTPBasicAuth(self.user, self.password),
            timeout=10,
        )
        if res.ok:
            return res.text
        raise OcPyRequestException("could not delete mediapackage!", response=res)


def main():
    api = SearchApi()
    pprint(api.get_episode())
    pprint(api.get_lucene("mh_default_org"))


if __name__ == "__main__":
    main()
