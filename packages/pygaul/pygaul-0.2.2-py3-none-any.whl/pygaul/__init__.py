"""
Easy access to administrative boundary defined by FAO GAUL 2015 from Python scripts.

This lib provides access to FAO GAUL 2015 datasets from a Python script. it is the best boundary dataset available for GEE at this point. We provide access to The current version (2015) administrative areas till level 2.
"""
import json
import warnings
from difflib import get_close_matches
from itertools import product
from pathlib import Path
from typing import List, Union

import ee
import numpy as np
import pandas as pd

__version__ = "0.2.2"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"

__gaul_data__ = Path(__file__).parent / "data" / "gaul_database.parquet"
__gaul_continent__ = Path(__file__).parent / "data" / "gaul_continent.json"
__gaul_asset__ = "FAO/GAUL/2015/level{}"


def get_names(
    name: str = "", admin: str = "", content_level: int = -1, complete: bool = False
) -> pd.DataFrame:
    """
    Return the list of names available in a administrative layer using the name or the administrative code.

    Return a pandas DataFrame of the names as FAO GAUL codes of and administrative region. The region can be requested either by its "name" or its "admin", the lib will identify the corresponding level on the fly. The user can also request for a specific level for its content e.g. get all admin level 1 of a country. If nothing is set we will infer the level of the item and if the level is higher than the found item, it will be ignored. If Nothing is found the method will raise an error.

    Args:
        name: The name of a administrative area. Cannot be set along with :code:`admin`.
        admin: The id of an administrative area in the FAO GAUL nomenclature. Cannot be set along with :code:`name`.
        content_level: The level to use in the final dataset. Default to -1 (use level of the selected area).
        complete: If True, the method will return all the names of the higher administrative areas. Default to False.

    Returns:
        The list of all the available names.
    """
    # sanitary check on parameters
    if name and admin:
        raise ValueError('"name" and "id" cannot be set at the same time.')
    elif not name and not admin:
        raise ValueError('at least "name" or "admin" need to be set.')

    # set the id we look for and tell the function if its a name or an admin
    is_name = True if name else False
    id = name if name else admin

    # read the data and find if the element exist
    df = pd.read_parquet(__gaul_data__)
    column = "ADM{}_NAME" if is_name else "ADM{}_CODE"
    is_in = (
        df.filter([column.format(i) for i in range(3)])
        .apply(lambda col: col.str.lower())
        .isin([id.lower()])
    )

    if not is_in.any().any():
        # find the 5 closest names/id
        columns = [df[column.format(i)].dropna().str.lower().values for i in range(3)]
        ids = np.unique(np.concatenate(columns))
        close_ids = get_close_matches(id.lower(), ids, n=5)
        if is_name is True:
            close_ids = [i.capitalize() for i in close_ids]
        else:
            close_ids = [i.upper() for i in close_ids]
        raise ValueError(
            f'The requested "{id}" is not part of FAO GAUL 2015. The closest matches are: {", ".join(close_ids)}.'
        )

    # Get the code of the associated country of the identifed area and the associated level
    line = is_in[~((~is_in).all(axis=1))].idxmax(1)
    level = line.iloc[0][3]

    # load the max_level available in the requested area
    sub_df = df[df[column.format(level)].str.fullmatch(id, case=False)]
    max_level = next(
        i for i in reversed(range(3)) if (sub_df[f"ADM{i}_NAME"] != "").any()
    )

    # get the request level from user
    if content_level == -1:
        content_level = level
    elif content_level < int(level):
        warnings.warn(
            f"The requested level ({content_level}) is higher than the area ({level}). Fallback to {level}."
        )
        content_level = level

    if int(content_level) > max_level:
        warnings.warn(
            f"The requested level ({content_level}) is higher than the max level in this country ({max_level}). Fallback to {max_level}."
        )
        content_level = max_level

    # get the columns name corresponding to the requested level
    columns = [f"ADM{content_level}_NAME", f"ADM{content_level}_CODE"]

    # the list will contain duplicate as all the smaller admin level will be included
    sub_df = sub_df.drop_duplicates(subset=columns, ignore_index=True)

    # the list will contain NA as all the bigger admin level will be selected as well
    # the database is read as pure string so dropna cannot be used
    # .astype is also a vectorized operation so it goes very fast
    sub_df = sub_df[sub_df[columns[0]].astype(bool)]

    # filter the df if complete is set to False, the only displayed columns will be the one requested
    final_df = sub_df if complete is True else sub_df[columns]

    return final_df


def _items(
    name: str = "", admin: str = "", content_level: int = -1
) -> ee.FeatureCollection:
    """
    Return the requested administrative boundaries using the name or the administrative code.

    Same method as get_items but only accept single requests in str format.

    Args:
        name: The name of an administrative area. Cannot be set along with :code:`admin`.
        admin: The id of an administrative area in the FAO GAUL nomenclature. Cannot be set along with :code:`name`.
        content_level: The level to use in the final dataset. Default to -1 (use level from the area).

    Returns:
        The FeatureCollection of the requested area with all the GADM attributes.
    """
    # call to get_names without level to raise an error if the requested level won't work
    df = get_names(name, admin)
    if len(df) > 1:
        raise ValueError(
            f'The requested name ("{name}") is not unique ({len(df)} results). To retrieve it, please use the `admin` parameter instead. If you don\'t know the GAUL code, use the following code, it will return the GAUL codes as well:\n`get_names(name="{name}")`'
        )
    df.columns[0][3]

    # now load the useful one to get content_level
    df = get_names(name, admin, content_level)
    content_level = df.columns[1][3]

    # checks have already been performed in get_names and there should
    # be one single result
    ids = [int(v) for v in df[f"ADM{content_level}_CODE"].to_list()]

    # read the accurate dataset
    feature_collection = ee.FeatureCollection(
        __gaul_asset__.format(content_level)
    ).filter(ee.Filter.inList(f"ADM{content_level}_CODE", ids))

    return feature_collection


def get_items(
    name: Union[str, List[str]] = "",
    admin: Union[str, List[str]] = "",
    content_level: int = -1,
) -> ee.FeatureCollection:
    """
    Return the requested administrative boundaries using the name or the administrative code.

    Return an ee.FeatureCollection representing an administrative region. The region can be requested either by its "name" or its "admin", the lib will identify the area level on the fly. The user can also request for a specific level for the GeoDataFrame features e.g. get all admin level 1 of a country. If nothing is set we will infer the level of the item and if the level is higher than the found item, it will be ignored. If Nothing is found the method will return an error.

    Args:
        name: The name of an administrative area. Cannot be set along with :code:`admin`. it can be a list or a single name.
        admin: The id of an administrative area in the GADM nomenclature. Cannot be set along with :code:`name`. It can be a list or a single admin code.
        content_level: The level to use in the final dataset. Default to -1 (use level from the area).

    Returns:
        The FeatureCollection of the requested area with all the GADM attributes.
    """
    # set up the loop
    names = [name] if isinstance(name, str) else name
    admins = [admin] if isinstance(admin, str) else admin

    # check that they are not all empty
    if names == [""] == admins:
        raise ValueError('at least "name" or "admin" need to be set.')

    # special parsing for continents. They are saved as admins to avoid any duplication
    continents = json.loads(__gaul_continent__.read_text())
    if len(names) == 1 and names[0].lower() in continents:
        admins = [c for c in continents[names[0].lower()]]
        names = [""]

    # use itertools, normally one of them is empty so it will raise an error
    # if not the case as admin and name will be set together
    fc_list = [_items(n, a, content_level) for n, a in product(names, admins)]

    # avoid concat if not needed for speed boost
    feature_collection = fc_list[0]
    if len(fc_list) > 1:
        for fc in fc_list[1:]:
            feature_collection = feature_collection.merge(fc)

    return feature_collection
