from typing import List, Callable, Tuple
from dl_matrix.infrence.utility.loader import DatasetLoader
import logging
import random
import pandas as pd


class DataHelper:
    def __init__(self, dataset_loader: DatasetLoader):
        self.dataset_loader = dataset_loader
        self.original_data = dataset_loader.filter_responses()
        self.prompt_col, self.response_col = dataset_loader.get_data_columns()
        self.operations = []
        self.processed_data = self.original_data.copy()

    def start(self):
        """Initialize the chain."""
        logging.info(f"Starting with {len(self.processed_data)} records.")
        return self

    def get_prompts(self) -> List[str]:
        return self.processed_data[self.prompt_col].tolist()

    def get_responses(self) -> List[str]:
        return self.processed_data[self.response_col].tolist()

    def get_example_pairs(self) -> List[Tuple[str, str]]:
        return list(zip(self.get_prompts(), self.get_responses()))

    def filter_prompts_by_complexity(
        self, min_words: int, max_words: int
    ) -> "DataHelper":
        self.processed_data = self.processed_data[
            self.processed_data[self.prompt_col].apply(
                lambda x: min_words <= len(x.split()) <= max_words
            )
        ]
        self.operations.append(
            f"Filtered prompts by complexity: {min_words}-{max_words} words. Remaining records: {len(self.processed_data)}"
        )
        return self

    def get_random_example_pairs(self) -> List[Tuple[str, str]]:
        return random.sample(self.get_example_pairs(), len(self.get_example_pairs()))

    def get_random_response(self) -> str:
        return random.choice(self.get_responses())

    def get_random_prompt(self) -> str:
        return random.choice(self.get_prompts())

    def filter_by_keyword(self, keyword: str) -> "DataHelper":
        self.processed_data = self.processed_data[
            self.processed_data[self.response_col].str.contains(keyword, case=False)
        ]
        self.operations.append(
            f"Filtered by keyword: {keyword}. Remaining records: {len(self.processed_data)}"
        )
        return self

    def reset_filters(self) -> "DataHelper":
        self.processed_data = self.original_data.copy()
        self.operations = ["Reset filters"]
        return self

    def get_operations(self) -> List[str]:
        return self.operations

    def __repr__(self):
        return f"DataHelper with {len(self.processed_data)} entries. Operations: {', '.join(self.operations)}"

    def filter_by_condition(self, column: str, condition_fn: Callable) -> "DataHelper":
        """Dynamic Filtering based on user-specified column and condition."""
        self.processed_data = self.processed_data[
            self.processed_data[column].apply(condition_fn)
        ]
        logging.info(
            f"Filtered by {column}. Remaining records: {len(self.processed_data)}"
        )
        self.operations.append(
            f"Filtered by {column}. Remaining records: {len(self.processed_data)}"
        )
        return self

    def randomize_order(self) -> "DataHelper":
        """Shuffle the order of rows."""
        self.processed_data = self.processed_data.sample(frac=1).reset_index(drop=True)
        logging.info("Order randomized.")
        self.operations.append("Randomized order")
        return self

    def apply_transformation(
        self, column: str, transformation_fn: Callable
    ) -> "DataHelper":
        """Apply transformations on a specific column."""
        self.processed_data[column] = self.processed_data[column].apply(
            transformation_fn
        )
        logging.info(f"Applied transformation to column: {column}")
        self.operations.append(f"Transformed column: {column}")
        return self

    def peek(self, rows: int = 5) -> "DataHelper":
        """Allow users to peek into the current state of the data."""
        print(self.processed_data.head(rows))
        return self

    def finalize(self) -> pd.DataFrame:
        """Conclude the chain."""
        logging.info("Finalized.")
        return self.processed_data

    def handle_error(self, error_message: str) -> "DataHelper":
        """Gracefully handle errors and continue the chain if possible."""
        logging.error(error_message)
        return self

    def chain(self, operations: List[Callable]) -> "DataHelper":
        """
        Apply a series of operations sequentially on the data.

        Args:
            operations (List[Callable]): A list of functions (operations) to be applied in order.
                                        Each item in the list should be a tuple of (function, args, kwargs),
                                        where function is a reference to the function to be called,
                                        args is a tuple of arguments, and kwargs is a dictionary of keyword arguments.

        Returns:
            DataHelper: The updated DataHelper instance after applying operations.
        """

        for operation in operations:
            function, args, kwargs = operation

            if not callable(function):
                logging.error(f"{function} is not a callable operation.")
                continue

            try:
                function(*args, **kwargs)
            except Exception as e:
                logging.error(f"Error executing {function}: {e}")
                self.handle_error(str(e))

        return self
