import pandas as pd
from typing import List, Dict
import numpy as np
import scipy.linalg
import importlib.resources


def transform_l1000_ids(
    from_id,
    to_id,
    gene_ids,
    dataset_path="l1000_mapped.csv",
    ignore_missing=False,
) -> Dict:
    """
    Transforms L1000 gene IDs from one format to another.

    Args:
        from_id (str): The source probe type ("affyID", "entrezID", "ensemblID").
        to_id (str): The target probe type ("affyID", "entrezID", "ensemblID").
        gene_ids (list): List of L1000 gene IDs to transform.
        dataset_path (str): Path to the DataFrame containing L1000 gene IDs for each probe type.
        ignore_missing (bool): If set to True, it will not raise an error on missing or invalid probe IDs.

    Returns:
        dict: Original and transformed L1000 gene IDs as keys and values respectively.

    Raises:
        ValueError: If either from_id or to_id is not one of the allowed values.
        ValueError: If any of the gene IDs in the dataset is not within the scope of L1000.

    """
    # Initialize dataset pd.DataFrame
    with importlib.resources.path('tka.data', dataset_path) as file_path:
        l1000 = pd.read_csv(file_path)

    # Define the allowed probe types
    allowed_probes = ["affyID", "entrezID", "ensemblID"]

    # Check if the probe types are valid
    if from_id not in allowed_probes or to_id not in allowed_probes:
        raise ValueError(
            "Invalid probe type. Allowed values: 'affyID', 'entrezID', 'ensemblID'."
        )

    # Initialize the output dict
    transformed_ids = {}

    # Perform the transformation
    for gene_id in gene_ids:
        # Safety check for missing IDs
        if gene_id not in l1000[from_id].values:
            if ignore_missing:
                continue
            raise ValueError(
                f"Gene ID '{gene_id}' is not within the scope of L1000 {from_id} values."
            )

        # Find the mapping from L1000 and save it to transformed_ids
        transformed_ids[gene_id] = l1000[l1000[from_id] == gene_id][to_id].values[0]

    return transformed_ids


def transform_moshkov_outputs(
    identifier_col_vals: List[str],
    output: List[List],
    use_full_assay_names: bool = False,
) -> pd.DataFrame:
    """
    Transform Moshkov outputs into a Pandas DataFrame.

    Args:
        identifier_col_vals (List[str]): List of SMILES strings corresponding to input data points (or any other identifiers).
        output (List[List[]]): List of lists containing output data (shape: X, 270).
        use_full_assay_names (bool, optional): Whether to use full assay names from the CSV. Defaults to False.

    Returns:
        DataFrame: Pandas DataFrame with SMILES as the first column and assay data columns.
    """

    # Load the PUMA_ASSAY_ID values from the CSV file
    with importlib.resources.path('tka.data', 'assay_metadata.csv') as file_path:
        assay_metadata = pd.read_csv(file_path)

    puma_assay_ids = assay_metadata["PUMA_ASSAY_ID"].tolist()

    # Create a dictionary to store the data for DataFrame creation
    data_dict = {"smiles": identifier_col_vals}

    # Loop through each PUMA_ASSAY_ID and add its values to the dictionary
    for idx, puma_assay_id in enumerate(puma_assay_ids):
        if use_full_assay_names:
            puma_assay_id = (
                assay_metadata[assay_metadata["PUMA_ASSAY_ID"] == puma_assay_id][
                    "ASSAY_NAME"
                ].values[0]
                + "_"
                + puma_assay_id
            )
        column_values = [row[idx] for row in output]
        data_dict[puma_assay_id] = column_values

    # Create a Pandas DataFrame from the data dictionary
    df = pd.DataFrame(data_dict)
    df.set_index("smiles", inplace=True)

    return df


class SpheringNormalizer(object):
    def __init__(self, controls):
        REG_PARAM = 10 ** np.log(1 / controls.shape[0])
        # Sphering transform on population level data
        self.mu = controls.mean()
        self.sphering_transform(controls - self.mu, REG_PARAM, rotate=True)
        # print(self.mu.shape, self.W.shape)

    def sphering_transform(self, X, lambda_, rotate=True):
        C = (1 / X.shape[0]) * np.dot(X.T, X)
        s, V = scipy.linalg.eigh(C)
        D = np.diag(1.0 / np.sqrt(s + lambda_))
        W = np.dot(V, D)
        if rotate:
            W = np.dot(W, V.T)
        self.W = W

    def normalize(self, X):
        return np.dot(X - self.mu, self.W)


def load_mobc_ordered_feature_columns():
    with importlib.resources.path('tka.data', "mobc_feature_columns_ordered.txt") as file_path:
        with file_path.open() as file:
            return [x.split("\n")[0] for x in file.readlines()]

def load_l1000_ordered_feature_columns(gene_id):
    with importlib.resources.path('tka.data', "l1000_mapped.csv") as file_path:
        return list(pd.read_csv(file_path)[gene_id].values)

def prepare_df_for_mobc_predictions(
    df_dmso, df_real, identifier_col="SMILES", grouping_col="", normalize=True
):
    mobc_features = load_mobc_ordered_feature_columns()

    # Check if all required CellProfiler features are present in the two datasets
    assert all([x in df_real.columns for x in mobc_features])

    df_real = df_real[[identifier_col] + mobc_features]

    if normalize:
        assert all([x in df_dmso.columns for x in mobc_features])
        df_dmso = df_dmso[mobc_features]
        normalizer = SpheringNormalizer(df_dmso)
        normalized_real_vals = normalizer.normalize(df_real[mobc_features])
        df_real[mobc_features] = normalized_real_vals

    if grouping_col != "":
        df_real = df_real.groupby(grouping_col)[mobc_features].mean()

    df_real.set_index(identifier_col, inplace=True)

    return df_real


if __name__ == "__main__":
    pass
