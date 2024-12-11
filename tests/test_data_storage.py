"""
Tests for data storage functionality.
"""

import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime
from src.utils.data_storage import store_season_data, load_season_data, list_season_data

@pytest.fixture
def test_data():
    return {
        "dict_data": {"test": "value"},
        "list_data": ["item1", "item2"],
        "df_data": pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    }

@pytest.fixture
def test_year():
    return 2024

def test_store_season_data_dict(test_data, test_year, tmp_path):
    data = test_data["dict_data"]
    result = store_season_data(data, test_year, "raw", "test_dict")
    assert result.exists()
    assert result.suffix == ".json"

def test_store_season_data_dataframe(test_data, test_year, tmp_path):
    data = test_data["df_data"]
    result = store_season_data(data, test_year, "standings", "test_df")
    assert result.exists()
    assert result.suffix == ".csv"

def test_load_season_data_json(test_data, test_year, tmp_path):
    # Store test data
    store_season_data(test_data["dict_data"], test_year, "raw", "test_load")
    
    # Load and verify
    loaded_data = load_season_data(test_year, "raw", "test_load")
    assert loaded_data == test_data["dict_data"]

def test_load_season_data_csv(test_data, test_year, tmp_path):
    # Store test data
    store_season_data(test_data["df_data"], test_year, "standings", "test_load")
    
    # Load and verify
    loaded_data = load_season_data(test_year, "standings", "test_load", as_dataframe=True)
    pd.testing.assert_frame_equal(loaded_data, test_data["df_data"])

def test_list_season_data(test_year, tmp_path):
    # Create some test files
    store_season_data({"test": "data"}, test_year, "raw", "test1")
    store_season_data({"test": "data2"}, test_year, "raw", "test2")
    
    # List and verify
    files = list_season_data(test_year, "raw")
    assert "raw" in files
    assert len(files["raw"]) == 2

def test_invalid_data_type(test_data, test_year):
    with pytest.raises(ValueError):
        store_season_data(test_data["dict_data"], test_year, "invalid_type", "test")

def test_missing_data(test_year):
    with pytest.raises(FileNotFoundError):
        load_season_data(test_year, "raw", "nonexistent_file") 