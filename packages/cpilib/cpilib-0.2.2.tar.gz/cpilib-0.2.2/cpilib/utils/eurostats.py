import gzip
import os
import time
import urllib.request

import pandas as pd

# pylint: disable = broad-exception-caught, invalid-name, unspecified-encoding


def file_age(filename):
    """
    Calculate the age of a given file in hours.

    Parameters
    ----------
    filename : str
        The name of the file.

    Returns
    -------
    int
        The age of the file in hours (rounded to whole hours), -1 if file does not exist.
    """
    if os.path.exists(filename):
        return int((time.time() - os.path.getmtime(filename)) / 3600)
    return -1


def download_url(url, filename, binary=False, unzip=False):
    """
    Download the given URL and save it under filename.
    If the filename contains a directory, it is assumed the directory exists.

    Parameters
    ----------
    url : str
        The URL to download.
    filename : str
        The filename to save the file under.
    binary : bool, optional
        If True, download file as binary.
    unzip : bool, optional
        If True, unzip the downloaded file.
    """
    # if os.path.exists(filename) and file_age(filename) < 24:
    #    # Cached version exists and is less than a day old
    #    return
    try:
        with urllib.request.urlopen(url) as resp:
            if unzip:
                with gzip.GzipFile(fileobj=resp) as data:
                    file_content = data.read()
            else:
                file_content = resp.read()
            if not binary:
                file_content = file_content.decode("utf-8")

        dir_name = os.path.dirname(filename)
        os.makedirs(dir_name, exist_ok=True)

        with open(filename, "wb" if binary else "w") as f:
            f.write(file_content)
    except Exception:
        pass


def get_eurostat_dictionary(dictionary, inverse=False):
    """
    Fetch a dictionary from Eurostat.

    Parameters
    ----------
    dictionary : str
        The name of the dictionary to download.
    inverse : bool, optional
        If True, return value -> key mapping, defaults to False.

    Returns
    -------
    dict
        A Python dictionary with the key -> value pair.
    """
    dictionary = dictionary.lower()
    url = (
        "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/"
        "BulkDownloadListing?sort=1&downfile=dic%2Fen%2F{dictionary}.dic"
    )
    filename = os.path.join("cache", f"{dictionary}.dic")
    download_url(url, filename)

    try:
        with open(filename) as f:
            d = {}
            for line in f:
                if len(line.strip()) > 1:
                    row = line.split("\t")
                    d[row[0]] = row[1].strip()
        return {v: k for k, v in d.items()} if inverse else d
    except Exception:
        return {}


def get_eurostat_dataset(dataset, replace_codes=True, transpose=True, keep_codes=None):
    """
    Fetch a dataset from Eurostat.

    Downloads the dataset, replaces the code columns with their associated meanings (optional) and
    transposes the column for improved usability (optional).

    Parameters
    ----------
    dataset : str
        The name of the dataset to download.
    replace_codes : bool, optional
        If True, replaces codes with their associated values. Defaults to True.
    transpose : bool, optional
        If True, transpose the    dataset for ease of analysis. Defaults to True.
    keep_codes : list, optional
        List of codes not to replace. Defaults to None.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the downloaded dataset.
    """
    dataset = dataset.lower()
    filename = os.path.join("cache", f"{dataset}.tsv")
    url = f"https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/{dataset}.tsv.gz"
    download_url(url, filename, unzip=True)

    df = pd.read_csv(filename, sep=",|\t| [^ ]?\t", na_values=":", engine="python", dtype_backend="pyarrow")
    df.columns = [x.split("\\")[0].strip() for x in df.columns]

    # Get dictionary columns
    with open(os.path.join("cache", f"{dataset}.tsv")) as f:
        first_line = f.readline()
    codes = first_line.split("\t")[0].split("\\")[0].split(",")

    # Replace codes with value
    if replace_codes:
        for c in codes:
            if keep_codes is None or c not in keep_codes:
                code_list = get_eurostat_dictionary(c)
                df[c] = df[c].replace(code_list)

    # Transpose the table
    if transpose:
        df = df.set_index(codes).transpose()

    return df


def get_eurostat_geodata(level=0):
    """
    Fetch the geodata of the European countries.

    The features are filtered on the NUTS level code. Level 0 contains the countries,
    level 1 the regions within countries, etc.

    Parameters
    ----------
    level : int, optional
        The NUTS level to download. Defaults to 0.

    Returns
    -------
    GeoDataFrame
        A GeoDataFrame with the geodata.
    """
    import geopandas as gpd  # pylint: disable = import-outside-toplevel

    url = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/shp/NUTS_RG_20M_2021_3035.shp.zip"
    filename = os.path.join("cache", "NUTS_RG_20M_2021_3035.shp.zip")
    download_url(url, filename, binary=True)

    borders = gpd.read_file(filename)
    return borders[borders["LEVL_CODE"] == level]
