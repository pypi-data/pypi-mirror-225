import pytest
import pandas as pd
from histcite.compute_metrics import ComputeMetrics


source_type = 'cssci'
docs_df_path = 'tests/testdata/docs_df.csv'
citation_relationship_path = 'tests/testdata/citation_relationship.csv'

docs_df = pd.read_csv(docs_df_path, dtype_backend='pyarrow')
citation_relationship = pd.read_csv(citation_relationship_path, dtype_backend='pyarrow')
cm = ComputeMetrics(docs_df, None, citation_relationship, source_type)

def test_generate_author_df():
    keyword_df = cm.generate_keyword_df()
    assert keyword_df.index[0] == '智慧图书馆'
    assert keyword_df.iloc[0, 0] == 303

def test_generate_reference_df():
    with pytest.raises(AssertionError) as excinfo:
        cm.generate_reference_df()
    assert str(excinfo.value) == "Param refs_df can't be None"