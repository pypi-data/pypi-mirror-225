"""ITSPerfect integration"""
import requests


class Itsperfect:
    """Integration class to represent ITSPerfect API responses.

    :param str url: base_url for the ITSP API
    :param str token: Authorization token for the ITSP API.
    :param str version: Version of the ITSP API to be used.
    :param str timeout: Timeout time for the requests made to ITSP.
    """
    endpoints = [
        {
            'path': 'stock',
            'key': 'stock',
            'endpoint_id': 'stock'
        },
        {
            'path': 'purchaseOrders',
            'key': 'purchaseorders',
            'endpoint_id': 'purchaseorders'
        },
        {
            'path': 'barcodes',
            'key': 'barcodes',
            'endpoint_id': 'barcodes'
        },
        {
            'path': 'items',
            'key': 'items',
            'endpoint_id': 'items'
        },
        {
            'path': 'customers',
            'key': 'brands',
            'endpoint_id': 'customer_brands',
            "path_extension": "brands"
        },
        {
            'path': 'customers',
            'key': 'addresses',
            'endpoint_id': 'customer_addresses',
            "path_extension": "addresses"
        }
    ]

    def __init__(self, url: str, token: str, version: str = "v2", timeout: int = 5):
        self.url = url
        self.token = token
        self.version = version
        self.timeout = timeout

    def __get_endpoint(self, endpoint_id: str):
        """Private Func to find the requested endpoint"""
        endpoint = next(
            (item for item in self.endpoints if item["endpoint_id"] == endpoint_id),
            None,
        )
        return [] if endpoint is None else endpoint

    def __get_endpoint_url(self, endpoint_id: str, item_id: str = ""):
        """Private Func to parse and return the URL for the endpoint"""
        endpoint = self.__get_endpoint(endpoint_id)
        base_url = f"https://{self.url}/api/{self.version}/{endpoint['path']}"

        if item_id != "":
            base_url = f"{base_url}/{item_id}"

        if "path_extension" in endpoint:
            base_url = f"{base_url}/{endpoint['path_extension']}"

        return base_url

    def __get_endpoint_key(self, endpoint_id: str):
        """Private Func to parse and return the key for the endpoint"""
        endpoint = self.__get_endpoint(endpoint_id)
        return endpoint["key"]

    def __fetch_data(
        self,
        base_url: str,
        endpoint_key: str,
        batch_size: int = 100,
        page_limit: int = 0,
    ):
        """General data function to get data from itsp"""
        data = []
        page_finished = False
        page_number = 1
        current_page = 1
        last_page = 1

        while not page_finished:
            parameters = f"&token={self.token}&page={page_number}&limit={batch_size}"
            url = f"{base_url}/{parameters}"
            print(url)
            response = requests.get(url, timeout=self.timeout)

            if response.status_code == 200:
                headers = response.headers

                if (
                    "X-Pagination-Current-Page" in headers
                    and "X-Pagination-Page-Count" in headers
                ):
                    data.extend(response.json()[endpoint_key])
                    current_page = int(headers["X-Pagination-Current-Page"])
                    last_page = int(headers["X-Pagination-Page-Count"])
                else:
                    error = f"Unable to retrieve API data for {base_url}"
                    return f"{error} on page: {page_number}, with bSize {batch_size}."
                # Use last page as indictor for the end of requests
                # Unless page_limit is set, in that case use page_limit
                if (page_limit == 0 and current_page < last_page) or (
                    page_limit != 0 and current_page < page_limit
                ):
                    page_number += 1
                else:
                    page_finished = True
        return data

    def fetch_all(self, endpoint_id: str, batch_size: int = 100, page_limit: int = 0):
        """Get all data from a single endpoint, batch_size optional (default 100)"""
        print("fetch_all", endpoint_id)
        base_url = self.__get_endpoint_url(endpoint_id)
        endpoint_key = self.__get_endpoint_key(endpoint_id)
        return self.__fetch_data(base_url, endpoint_key, batch_size, page_limit)

    def fetch_one(self, endpoint_id: str, item_id: str):
        """Get one record from a single endpoint"""
        print("fetch_one", endpoint_id, item_id)
        base_url = self.__get_endpoint_url(endpoint_id, item_id)
        endpoint_key = self.__get_endpoint_key(endpoint_id)
        return self.__fetch_data(base_url, endpoint_key)
