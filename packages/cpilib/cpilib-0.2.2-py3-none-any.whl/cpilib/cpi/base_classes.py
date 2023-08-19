import pandas as pd


class GraphDataFrame(pd.DataFrame):
    """DataFrame subclass for CPI indexes."""

    def node(self, node):
        """
        Retrieve a node's series from the DataFrame.

        Parameters
        ----------
        node : str
            The node to retrieve.

        Returns
        -------
        pd.Series
            The series corresponding to the node.
        """
        return self[node]

    def children(self, node, max_depth=False, strict=True):
        """
        Retrieve the children of a node.

        Parameters
        ----------
        node : str
            The parent node.
        max_depth : bool, optional
            If True, return all levels of children. If False, return only the next level (default is True).
        strict : bool, optional
            If True, the parent node itself will not be included (default is False).

        Returns
        -------
        pd.DataFrame
            DataFrame containing the children of the node.
        """
        if node == "CP00":
            # If the parent node is CP00, children should be CP01 to CP12
            if max_depth:
                if strict:
                    mask = self.columns.isin(
                        [code for code in self.columns if code.startswith("CP") and code != "CP00"]
                    )
                else:
                    return self
            else:
                if strict:
                    mask = self.columns.isin(["CP" + str(i).zfill(2) for i in range(1, 13)])
                else:
                    mask = self.columns.isin(["CP" + str(i).zfill(2) for i in range(0, 13)])
        else:
            if max_depth:
                mask = self.columns.str.startswith(node)
            else:
                mask = self.columns.str.startswith(node) & (self.columns.str.len() <= len(node) + 1)
            if strict:
                mask = mask & (self.columns != node)

        return self.loc[:, mask]


class CountryGraphDataFrame(pd.DataFrame):
    """DataFrame subclass for multi-country CPI indexes."""

    def country(self, country):
        """Retrieve data for a specific country."""
        return self[country]

    def node(self, node, country=None):
        """
        Retrieve a node's series for a specific country.

        Parameters
        ----------
        node : str
            The node to retrieve.
        country : str, optional
            The country for which to retrieve the node. If None, retrieves the node for all countries.

        Returns
        -------
        pd.Series or pd.DataFrame
            The series corresponding to the node for a specific country,
            or a DataFrame containing the series for the node for all countries.
        """
        if country is None:
            return self.xs(node, level=1, axis=1)
        return self[country, node]

    def children(self, node, country, max_depth=False, strict=True):
        """
        Retrieve the children of a node for a specific country.

        Parameters
        ----------
        node : str
            The parent node.
        country : str
            The country for which to retrieve the children.
        max_depth : bool, optional
            If True, return all levels of children. If False, return only the next level (default is True).
        strict : bool, optional
            If True, the parent node itself will not be included (default is False).

        Returns
        -------
        pd.DataFrame
            DataFrame containing the children of the node for the specified country.
        """
        return GraphDataFrame(self[country]).children(node, max_depth, strict)


class CPI:
    """CPI system."""

    def __init__(self, prices, weights, country, base_year):
        """Initialize the CPI object for a single country."""
        self.prices = GraphDataFrame(prices)
        self.weights = GraphDataFrame(weights)
        self.country = country
        self.base_year = base_year


class CPICountries:
    """Multi-county CPI system."""

    def __init__(self, prices, weights, country_weights, base_year):
        """Initialize the CPI object for multiple countries."""
        self.prices = CountryGraphDataFrame(prices)
        self.weights = CountryGraphDataFrame(weights)
        self.country_weights = country_weights
        self.base_year = base_year
