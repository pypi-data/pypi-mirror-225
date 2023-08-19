import pandas as pd
import pkg_resources


def load(filename):

    if not filename.endswith(".zip"):
        zipped_filename = filename + ".zip"
    else:
        zipped_filename = filename

    available_data = list_pkg_data()
    assert zipped_filename in available_data, (
        f"Could not find '{filename}' dataset. "
        + f"Available datasets are: {[data.strip('.zip') for data in available_data]}."
    )

    # Path to data relative to package
    data_path = f"data/{zipped_filename}"

    # Absolute path to data
    abs_path = pkg_resources.resource_filename(__name__, data_path)

    return pd.read_csv(abs_path)


def list_pkg_data():
    # Get path to files relative to package
    pkg_data = pkg_resources.resource_listdir(__name__, "data")
    return pkg_data
