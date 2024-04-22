from  chatbot_core.rag_gpt_integration import load_csv_url_from_directory

import os


def test_load_csv_url_from_directory():
    current_directory = os.getcwd()

    # Get the parent directory of the current directory
    parent_directory = os.path.dirname(current_directory)

    # Define the directory containing the data source
    data_source_directory = os.path.join(parent_directory, 'data_source')

    # Load CSV files from the data source directory
    load_list = load_csv_url_from_directory(data_source_directory)

    # Get a list of CSV files in the data source directory
    csv_list = [file for file in os.listdir(data_source_directory) if file.endswith('.csv')]

    assert isinstance(csv_list, list)
    assert len(load_list)==len(csv_list)



