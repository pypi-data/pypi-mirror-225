"""This module provides functions to recognize local references of a doc."""
import pandas as pd
from typing import Optional


def recognize_common_refs(
    docs_df: pd.DataFrame,
    refs_df: pd.DataFrame,
    compare_cols: list[str],
    drop_duplicates: bool = False,
):
    """
    Recognize local references of a doc.

    Args:
        docs_df: DataFrame of docs.
        refs_df: DataFrame of references.
        compare_cols: Columns to compare. e.g. `["First_AU", "TI"]`.
        drop_duplicates: Whether to drop duplicated rows with same values in `compare_cols`. Default is False.

    Returns:
        Tuple of two Series, cited_refs_series and local_refs_series.
    """
    # Drop rows with missing values
    docs_df = docs_df.dropna(subset=compare_cols)
    refs_df = refs_df.dropna(subset=compare_cols)

    if drop_duplicates is True:
        docs_df = docs_df.drop_duplicates(subset=compare_cols)

    docs_df = docs_df[["doc_index"] + compare_cols]
    refs_df = refs_df[["doc_index", "ref_index"] + compare_cols]
    shared_df = pd.merge(
        refs_df, docs_df, how="left", on=compare_cols, suffixes=("_x", "_y")
    ).dropna(subset="doc_index_y")
    shared_df = shared_df.astype({"doc_index_y": "int64"})
    cited_refs_series = shared_df.groupby("doc_index_x")["doc_index_y"].apply(list)
    cited_refs_series = cited_refs_series.apply(lambda x: sorted(x))
    local_refs_series = shared_df["ref_index"].reset_index(drop=True)
    return cited_refs_series, local_refs_series


class RecognizeReference:

    @staticmethod
    def recognize_wos_reference(docs_df: pd.DataFrame, refs_df: pd.DataFrame):
        """Recognize local references of a doc from Web of Science. 
        
        If `DOI` exists, use `DOI` to recognize references. 
        Otherwise, use `First_AU`, `PY`, `J9`, `BP` to recognize references.

        Args:
            docs_df: DataFrame of docs.
            refs_df: DataFrame of references.
        
        Returns:
            Tuple of two Series, cited_refs_series and local_refs_series.
        """

        def _merge_lists(list1: Optional[list[int]], list2: Optional[list[int]]):
            if isinstance(list1, list) and isinstance(list2, list):
                return list1 + list2
            else:
                if isinstance(list1, list):
                    return list1
                else:
                    return list2

        # DOI exists
        compare_cols_doi = ["DI"]
        result_doi = recognize_common_refs(docs_df, refs_df, compare_cols_doi)

        # DOI not exists
        compare_cols = ["First_AU", "PY", "J9", "BP"]
        result = recognize_common_refs(
            docs_df[docs_df["DI"].isna()], refs_df[refs_df["DI"].isna()], compare_cols
        )
        cited_refs_series = result_doi[0].combine(result[0], _merge_lists)
        local_refs_series = pd.concat([result_doi[1], result[1]])
        return cited_refs_series, local_refs_series

    @staticmethod
    def recognize_cssci_reference(docs_df: pd.DataFrame, refs_df: pd.DataFrame):
        """Recognize local references of a doc from CSSCI.
        
        Use `First_AU`, `TI` to recognize references.

        Args:
            docs_df: DataFrame of docs.
            refs_df: DataFrame of references.

        Returns:
            Tuple of two Series, cited_refs_series and local_refs_series.
        """
        compare_cols = ["First_AU", "TI"]
        return recognize_common_refs(docs_df, refs_df, compare_cols)

    @staticmethod
    def recognize_scopus_reference(docs_df: pd.DataFrame, refs_df: pd.DataFrame):
        """Recognize local references of a doc from Scopus.
        
        Use `First_AU`, `TI` to recognize references.

        Args:
            docs_df: DataFrame of docs.
            refs_df: DataFrame of references.
        
        Returns:
            Tuple of two Series, cited_refs_series and local_refs_series.
        """
        compare_cols = ["First_AU", "TI"]
        return recognize_common_refs(docs_df, refs_df, compare_cols, drop_duplicates=True)
    
