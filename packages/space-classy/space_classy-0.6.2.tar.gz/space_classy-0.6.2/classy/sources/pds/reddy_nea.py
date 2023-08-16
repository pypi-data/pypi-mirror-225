import pandas as pd
import rocks

from classy import index
from classy import config
from classy.sources import pds

SHORTBIB, BIBCODE = "Reddy 2009", "2009PhDT.......233R"


def _load_data(idx):
    """Load data and metadata of a cached Gaia spectrum.

    Parameters
    ----------
    idx : pd.Series
        A row from the classy spectra index.

    Returns
    -------
    pd.DataFrame, dict
        The data and metadata. List-like attributes are in the dataframe,
        single-value attributes in the dictionary.
    """

    # Load spectrum data file
    PATH_DATA = config.PATH_CACHE / idx.filename
    data = pd.read_csv(PATH_DATA, names=["wave", "refl", "refl_err"], delimiter=r"\s+")
    return data, {}


def _create_index(PATH_REPO):
    """Create index of spectra collection."""

    entries = []

    # Iterate over data directory
    for dir in PATH_REPO.iterdir():
        if dir.name != "data":
            continue

        # Extract meta from LBL file
        for xml_file in dir.glob("**/*lbl"):
            if xml_file.name.startswith("collection_gbo"):
                continue

            id_, _, date_obs = pds.parse_lbl(xml_file)

            if id_ == "4954 ERIC":
                id_ = 4954
            if id_ == "1980 TEZCATLIPOCA":
                id_ = 1980
            if id_ == "1620 GEOGRAPHOS":
                id_ = 1620
            if id_ == "4179 TOUTATIS":
                id_ = 4179
            if id_ == "6456 GOLOMBEK":
                id_ = 6456
            if id_ == "4015 WILSON-HARRINGTON":
                id_ = 4015

            file_ = xml_file.with_suffix(".tab")

            # Identify asteroid
            name, number = rocks.id(id_)

            # Create index entry
            entry = pd.DataFrame(
                data={
                    "name": name,
                    "number": number,
                    "date_obs": date_obs,
                    "shortbib": SHORTBIB,
                    "bibcode": BIBCODE,
                    "filename": str(file_).split("/classy/")[1],
                    "source": "Misc",
                    "host": "PDS",
                    "module": "reddy_nea",
                },
                index=[0],
            )

            # Add spectrum metadata
            data, _ = _load_data(entry.squeeze())
            entry["wave_min"] = min(data["wave"])
            entry["wave_max"] = max(data["wave"])
            entry["N"] = len(data["wave"])

            entries.append(entry)
    entries = pd.concat(entries)
    index.add(entries)
