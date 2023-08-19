from datetime import datetime
import math
from typing import Any, Dict, List, Union

import numpy as np
import pandas as pd

from nordea_analytics.nalib.data_retrieval_client import (
    DataRetrievalServiceClient,
)
from nordea_analytics.nalib.util import (
    get_config,
    pascal_case,
)
from nordea_analytics.nalib.value_retriever import ValueRetriever

config = get_config()


class BondStaticData(ValueRetriever):
    """Retrieves and reformats latest static data for given bonds.

    Inherits from ValueRetriever class.
    """

    def __init__(
        self,
        client: DataRetrievalServiceClient,
        symbols: Union[List[str], str],
    ) -> None:
        """Initialize the BondStaticData class.

        Args:
            client: The client used to retrieve data.
            symbols: ISIN or name of bonds for requests.
                List of bond symbols or a single bond symbol.
        """
        super(BondStaticData, self).__init__(client)

        # Convert symbols to a list if it's not already a list
        self.symbols: List = [symbols] if not isinstance(symbols, list) else symbols
        self._data = self.get_bond_static_data()

    def get_bond_static_data(self) -> List:
        """Calls the client and retrieves response with static data from the service.

        Returns:
            The list of static data for the given bonds.
        """
        json_response: List[Any] = []
        for request_dict in self.request:
            _json_response = self.get_response(request_dict)
            json_map = _json_response[config["results"]["bond_static_data"]]
            json_response = list(json_map) + json_response

        return json_response

    @property
    def url_suffix(self) -> str:
        """Url suffix for a given method.

        Returns:
            The url suffix for the method.
        """
        return config["url_suffix"]["bond_static_data"]

    @property
    def request(self) -> List[Dict]:
        """Request dictionary for a given set of symbols.

        Returns:
            The list of request dictionaries for the given symbols.
        """
        if len(self.symbols) > config["max_bonds"]:
            split_symbols = np.array_split(
                self.symbols, math.ceil(len(self.symbols) / config["max_bonds"])
            )
            request_dict = [
                {
                    "symbols": list(symbols),
                }
                for symbols in split_symbols
            ]
        else:
            request_dict = [
                {
                    "symbols": self.symbols,
                }
            ]

        return request_dict

    def to_dict(self) -> Dict:
        """Reformat the json response to a dictionary.

        Returns:
            A dictionary with bond symbol as key and bond static data as value.
        """
        bond_data_dict = {}
        for bond_data in self._data:
            bond_symbol = bond_data["symbol"]
            bond_static_data = {}
            bond_static_data["Name"] = bond_data["name"]

            for static_data_key in bond_data["static_data"]:
                key_value_pair = bond_data["static_data"][static_data_key]

                if key_value_pair["key"] in [
                    "closing_date",
                    "issue_date",
                    "maturity",
                    "retrieval_date",
                ]:
                    # Convert datetime strings to datetime objects for specific keys
                    bond_static_data[
                        pascal_case(key_value_pair["key"])
                    ] = datetime.strptime(
                        key_value_pair["value"], "%Y-%m-%dT%H:%M:%S.0000000"
                    )
                else:
                    bond_static_data[
                        pascal_case(key_value_pair["key"])
                    ] = key_value_pair["value"]

            bond_data_dict[bond_symbol] = bond_static_data

        return bond_data_dict

    def to_df(self) -> pd.DataFrame:
        """Reformat the json response to a pandas DataFrame.

        Returns:
            A pandas DataFrame with bond symbols as index and bond static data as columns.
        """
        bond_data_dict = self.to_dict()
        bond_df = pd.DataFrame.from_dict(bond_data_dict, orient="index")
        return bond_df
