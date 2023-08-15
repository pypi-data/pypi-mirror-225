import pandas as pd
from typing import Union, Optional
import os
import json
from dl_matrix.infrence.utility.prompt import PromptManager
import logging
from pathlib import Path
from typing import Optional
import pandas as pd


class DatasetLoader:
    """
    A class to handle loading datasets either from local paths or from the HuggingFace datasets library.
    """

    def __init__(
        self,
        prompt_directory: str,
        prompt_col: str,
        response_col: str,
        data_split: str = "train",
        local_dataset_path: Optional[str] = None,
        huggingface_dataset_name: Optional[str] = None,
    ):
        """
        Initialize the DatasetLoader.

        Args:
        - local_dataset_path (str, optional): Path to a local dataset file. Either CSV or JSON.
        - huggingface_dataset_name (str, optional): Name of the dataset in HuggingFace if loading from there.
        - data_split (str, optional): Desired data split if using HuggingFace datasets. Defaults to 'train'.
        - prompt_directory (str, optional): Directory to save prompts.
        """

        # Ensure only one of local_dataset_path or huggingface_dataset_name is provided.
        if local_dataset_path and huggingface_dataset_name:
            logging.error(
                "Please provide either a local dataset path OR a HuggingFace dataset name, not both."
            )
            raise ValueError("Multiple data sources provided.")

        # Load the dataset based on the source
        if local_dataset_path:
            self._load_data_from_local_path(local_dataset_path)
            self.output_directory = Path(os.path.dirname(local_dataset_path))
        else:
            data = self._load_data_from_huggingface(
                huggingface_dataset_name, data_split, prompt_col, response_col
            )
            self.output_directory = Path.cwd()
        self.data = data
        self.prompt_manager = PromptManager(prompt_directory)
        # Set and create prompt directory
        self.prompt_directory = self.output_directory / prompt_directory
        self.prompt_directory.mkdir(parents=True, exist_ok=True)

        self.prompt_col = prompt_col
        self.response_col = response_col
        self.SPF = [
            "Imagine That:",
            "Brainstorming:",
            "Thought Provoking Questions:",
            "Create Prompts:",
            "Synergetic Prompt:",
            "Category:",
        ]
        logging.info(
            f"Data loaded and prompt directory set to: {self.prompt_directory}"
        )

    def _load_data_from_local_path(self, dataset_path: str):
        """Load data from a given local path."""

        if not Path(dataset_path).exists():
            logging.error(f"Provided dataset path does not exist: {dataset_path}")
            raise FileNotFoundError("Dataset path not found.")

        _, file_extension = os.path.splitext(dataset_path)
        if file_extension == ".csv":
            self.data = pd.read_csv(dataset_path)
            logging.info(f"Loaded data from CSV at {dataset_path}")
        elif file_extension == ".json":
            with open(dataset_path, "r") as file:
                json_data = json.load(file)
                self.data = pd.DataFrame(json_data)
            logging.info(f"Loaded data from JSON at {dataset_path}")
        else:
            logging.error(
                f"Unsupported file format {file_extension}. Only .csv and .json are supported."
            )
            raise ValueError("Unsupported file format.")

    def _load_data_from_huggingface(
        self, dataset_name: str, split: str, prompt_col, response_col
    ):
        """Load data from the HuggingFace datasets library."""

        from datasets import load_dataset

        dataset = load_dataset(dataset_name, split=split)

        # Rename columns
        dataset = dataset.rename_column("input_text", prompt_col)
        dataset = dataset.rename_column("output_text", response_col)

        # Convert to pandas DataFrame
        self.data = dataset.to_pandas()

        logging.info(f"Loaded data from HuggingFace dataset: {dataset_name} ({split})")

        return self.data

    def preview(self, n: int = 5) -> None:
        """Preview the first n rows of the loaded dataset."""
        if n <= 0:
            print("Please provide a positive integer for preview.")
            return
        print(self.data.head(n))

    def get_dataset(self) -> pd.DataFrame:
        """Return the loaded dataset."""
        return self.data

    def get_data_columns(self):
        """Return the names of the prompt and response columns."""
        return self.prompt_col, self.response_col

    @classmethod
    def from_dataframe(
        cls,
        dataframe: pd.DataFrame,
        output_path: Union[str, Path],
        file_format: str = "csv",  # Default is csv, but can be set to json
        prompt_dir: str = "prompts",
        prompt_col: str = "prompt",  # New parameter
        response_col: str = "response",  # New parameter
    ) -> "DatasetLoader":
        """
        Create a DatasetLoader instance from a pandas DataFrame.

        Args:
        - dataframe (pd.DataFrame): The input dataframe.
        - output_path (Union[str, Path]): Path to save the processed dataset.
        - file_format (str): Desired output format, either "csv" or "json".
        - prompt_dir (str): Directory to save prompts.
        - prompt_col (str): Name of the prompt column.
        - response_col (str): Name of the response column.

        Returns:
        DatasetLoader: An instance of the DatasetLoader class.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame.")

        # Ensure that the dataframe contains the necessary columns
        required_columns = [prompt_col, response_col]
        missing_columns = [
            col for col in required_columns if col not in dataframe.columns
        ]
        if missing_columns:
            raise ValueError(
                f"DataFrame is missing columns: {', '.join(missing_columns)}"
            )

        # Save to the appropriate format
        if file_format == "csv":
            dataframe.to_csv(output_path, index=False)
        elif file_format == "json":
            dataframe.to_json(output_path, orient="records", indent=4)
        else:
            raise ValueError(
                f"Unsupported file format: {file_format}. Supported formats are 'csv' and 'json'."
            )

        print(f"Data successfully saved to {output_path}")

        return cls(
            str(output_path),
            prompt_dir,
            prompt_col=prompt_col,
            response_col=response_col,
        )  # Updated constructor call

    def get_data_columns(self):
        """Return the names of the prompt and response columns."""
        return self.prompt_col, self.response_col

    def filter_responses(
        self,
        use_specific_patterns: bool = False,
        min_elements: Optional[int] = 6,
        element_type: str = "STEP",
    ) -> pd.DataFrame:
        """
        Filter responses based on the data source and certain conditions.

        Args:
        - use_specific_patterns (bool): Whether to use specific patterns for filtering.
        - min_elements (int, optional): Minimum number of elements for filtering.
        - element_type (str, optional): Type of element for filtering.

        Returns:
        - pd.DataFrame: The filtered or original data.
        """

        if not use_specific_patterns:
            logging.info("Using data directly without filtering.")
            return self.data

        # If specific patterns are to be used for filtering
        cleaned_data = self.data.copy()

        # Clean up leading and trailing whitespaces from the response column
        cleaned_data[self.response_col] = cleaned_data[self.response_col].apply(
            lambda x: "\n".join([line.strip() for line in x.split("\n")])
        )

        for pattern in self.SPF:  # Assuming SPF is a list of patterns to check against
            cleaned_data = cleaned_data[
                cleaned_data[self.response_col].str.contains(pattern)
            ]

        cleaned_data = cleaned_data[
            cleaned_data[self.response_col].apply(
                lambda x: len([part for part in x.split(element_type) if ":" in part])
                >= min_elements
            )
        ]

        logging.info(
            f"Filtered data using specific patterns and found {len(cleaned_data)} relevant responses."
        )
        return cleaned_data
