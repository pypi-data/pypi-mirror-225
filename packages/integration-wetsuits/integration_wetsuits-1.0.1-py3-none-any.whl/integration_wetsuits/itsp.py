"""ITSPerfect integration"""
import logging

import requests


class Itsperfect:
    """Integration class to represent ITSPerfect API responses."""

    endpoints = [
        {
            "path":"stock",
            "key":"stock",
            "endpoint_id":"stock"
        },
        {
            "path":"purchaseOrders",
            "key":"purchaseorders",
            "endpoint_id":"purchaseorders"
        },
        {
            "path":"barcodes",
            "key":"barcodes",
            "endpoint_id":"barcodes"
        },
        {
            "path":"items",
            "key":"items",
            "endpoint_id":"items"
        },
        {
            "path":"customers",
            "key":"brands",
            "endpoint_id":"customer_brands",
            "path_extension":"brands"
        },
        {
            "path":"customers",
            "key":"addresses",
            "endpoint_id":"customer_addresses",
            "path_extension":"addresses"
        },
        {
            "path":"agents",
            "key":"agents",
            "endpoint_id":"agents"
        }
    ]

    def __init__(self, url: str, token: str, version: str = "v2", timeout: int = 5):
        """Initialize basic ITSP settings

        Args:
            url (str): base_url for the ITSP API
            token (str): Authorization token for the ITSP API.
            version (str, optional): Version of the ITSP API to be used.
                                     Defaults to "v2".
            timeout (int, optional): Timeout time for the requests made to ITSP.
                                     Defaults to 5.
        """

        self.token = token
        self.timeout = timeout
        self.base_url = f"https://{url}/api/{version}"

    def __get_endpoint(self, endpoint_id: str) -> dict:
        """Private Func to find the requested endpoint

        Args:
            endpoint_id (str): Categorical identifier for the itsp endpoint

        Returns:
            dict: Key-value pair containing all basic information on an endpoint
        """
        endpoint = next(
            (item for item in self.endpoints if item["endpoint_id"] == endpoint_id),
            None,
        )
        return [] if endpoint is None else endpoint

    def __add_item_id(self, base_url: str, item_id: str):
        return f"{base_url}/{item_id}" if item_id != "" else base_url

    def __add_path_extension(self, base_url: str, endpoint: dict):
        return (
            f"{base_url}/{endpoint['path_extension']}"
            if "path_extension" in endpoint
            else base_url
        )

    def __add_token(self, base_url: str):
        return f"{base_url}?token={self.token}"

    def __add_filter(self, base_url: str, filters: str):
        return f"{base_url}&filter={filters}" if filters != "" else base_url

    def __get_endpoint_url(
        self, endpoint_id: str, item_id: str = "", filters: str = ""
    ) -> str:
        """Private Func to parse and return the URL for the endpoint

        Args:
            endpoint_id (str): Categorical identifier for the itsp endpoint
            item_id (str, optional): Identifier for the optional ID to be sent to ITSP.
                                     Defaults to "".
            filters (str, optional): String filters to pass to ITSP. Defaults to "".

        Returns:
            str: Partial URL containing version, token and path
                 used for a specific route call
        """

        endpoint = self.__get_endpoint(endpoint_id)

        partial_url = f"{self.base_url}/{endpoint['path']}"
        partial_url = self.__add_item_id(partial_url, item_id)
        partial_url = self.__add_path_extension(partial_url, endpoint)
        partial_url = self.__add_token(partial_url)
        partial_url = self.__add_filter(partial_url, filters)

        logging.error("Generated URL: %s", partial_url)
        return partial_url

    def __get_endpoint_key(self, endpoint_id: str) -> str:
        """Private Func to parse and return the key for the endpoint

        Args:
            endpoint_id (str): _description_

        Returns:
            str: _description_
        """
        endpoint = self.__get_endpoint(endpoint_id)
        return endpoint["key"]

    def __fetch_data(
        self,
        base_url: str,
        endpoint_key: str,
        batch_size: int = 100,
        page_limit: int = 0,
    ) -> list:
        """General data function to get data from itsp

        Args:
            base_url (str): _description_
            endpoint_key (str): _description_
            batch_size (int, optional): _description_. Defaults to 100.
            page_limit (int, optional): _description_. Defaults to 0.

        Returns:
            list: _description_
        """

        data = []
        page_number = 1

        def walk_pagination(page_number: int = 1):
            current_page = 1
            last_page = 1
            # while not page_finished:
            parameters = f"&page={page_number}&limit={batch_size}"
            url = f"{base_url}{parameters}"
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
                    logging.error(
                        "Error calling %s. Call returned: %s",
                        url,
                        response
                    )
                # Use last page as indictor for the end of requests
                # Unless page_limit is set, in that case use page_limit
                if (page_limit == 0 and current_page < last_page) or (
                    page_limit != 0 and current_page < page_limit
                ):
                    page_number += 1
                    walk_pagination(page_number)
            else:
                logging.error(
                    "Unable to retrieve ITSP data, returned with message: %s",
                    response.text
                )

        walk_pagination(page_number)
        return data

    def fetch_all(
        self,
        endpoint_id: str,
        batch_size: int = 100,
        page_limit: int = 0,
        filters: str = "",
    ) -> list:
        """Get all data from a single endpoint.

        Args:
            endpoint_id (str): Textual identifier for which ITSP route is requested
            batch_size (int, optional): Specify the amount of records to
                                        be sent per request. Defaults to 100.
            page_limit (int, optional): Specify the number of iteration
                                        for the requests. Defaults to 0.
            filters (str, optional): Specify filters using ITSP format. Defaults to "".

        Returns:
            list: List containing all requested data
        """

        request_url = self.__get_endpoint_url(endpoint_id=endpoint_id, filters=filters)
        endpoint_key = self.__get_endpoint_key(endpoint_id)
        return self.__fetch_data(request_url, endpoint_key, batch_size, page_limit)

    def fetch_one(self, endpoint_id: str, item_id: str, filters: str = "") -> list:
        """Returns a single record from ITSP as list with a single object

        Args:
            endpoint_id (str): _description_
            item_id (str): _description_
            filters (str, optional): _description_. Defaults to "".

        Returns:
            list: List containing a single record of the requested data
        """
        request_url = self.__get_endpoint_url(
            endpoint_id=endpoint_id, item_id=item_id, filters=filters
        )
        endpoint_key = self.__get_endpoint_key(endpoint_id)
        return self.__fetch_data(request_url, endpoint_key)
