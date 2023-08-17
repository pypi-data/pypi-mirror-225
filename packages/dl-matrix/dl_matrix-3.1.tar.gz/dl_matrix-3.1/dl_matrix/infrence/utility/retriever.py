import logging
from functools import lru_cache
import re
from typing import List, Tuple, Union, Dict
import pandas as pd
from dl_matrix.infrence.utility.helper import DataHelper
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity


class DataRetriever:
    def __init__(self, data_helper: DataHelper):
        """Initializes the DataRetriever with a given DataHelper."""
        self.data = data_helper.finalize()
        self.prompt_col = data_helper.prompt_col
        self.response_col = data_helper.response_col
        self._validate_columns()

    def _validate_columns(self) -> None:
        """Validates if the specified columns exist in the dataset."""
        for col in [self.prompt_col, self.response_col]:
            if col not in self.data.columns:
                logging.error(f"Column '{col}' not found in data.")
                raise ValueError(f"Column '{col}' not found in data.")

    def _validate_pair_type(self, pair_type: str) -> None:
        """Validates if the provided pair_type is valid."""
        valid_pair_types = ["both", self.prompt_col, self.response_col]
        if pair_type not in valid_pair_types:
            logging.error(
                f"Invalid pair_type. Choose from {', '.join(valid_pair_types)}"
            )
            raise ValueError(
                f"Invalid pair_type. Choose from {', '.join(valid_pair_types)}"
            )

    def _get_data_by_pair_type(
        self, data_subset: pd.DataFrame, pair_type: str
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """Returns data based on the pair_type from a given data subset."""
        self._validate_pair_type(pair_type)

        if pair_type == "both":
            return list(
                zip(
                    data_subset[self.prompt_col].tolist(),
                    data_subset[self.response_col].tolist(),
                )
            )
        return data_subset[pair_type].tolist()

    def filter_prompts_by_complexity(self, min_words: int, max_words: int) -> List[str]:
        """Filters the prompts based on their complexity."""
        prompts = self.data[self.prompt_col].tolist()
        return [
            prompt
            for prompt in prompts
            if min_words <= len(prompt.split()) <= max_words
        ]

    def get_examples(
        self, pair_type: str = "both"
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """Gets examples of the specified type from the data."""
        return self._get_data_by_pair_type(self.data, pair_type)

    def get_random_examples(
        self, n: int, pair_type: str = "both"
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """Gets n random examples of the specified type from the data."""
        return self._get_data_by_pair_type(self.data.sample(n), pair_type)

    def get_first_n_examples(
        self, n: int, pair_type: str = "both"
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """Gets the first n examples of the specified type from the data."""
        return self._get_data_by_pair_type(self.data.head(n), pair_type)

    def search_examples(
        self, keywords: Union[str, List[str]], pair_type: str = "both"
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """Searches examples containing the keyword(s) of the specified type from the data."""
        if isinstance(keywords, str):
            keywords = [keywords]

        mask = self.data[self.prompt_col].str.contains(
            "|".join(map(re.escape, keywords))
        ) | self.data[self.response_col].str.contains(
            "|".join(map(re.escape, keywords))
        )

        filtered_data = self.data[mask]
        return self._get_data_by_pair_type(filtered_data, pair_type)

    def count_keyword(
        self, keyword: str, pair_type: str = "both"
    ) -> Union[int, Dict[str, int]]:
        data = self.data  # We get the data directly from the DataHelper instance

        if pair_type == "both":
            return {
                "prompt": data[self.prompt_col]
                .apply(lambda x: x.lower().count(keyword.lower()))
                .sum(),
                "response": data[self.response_col]
                .apply(lambda x: x.lower().count(keyword.lower()))
                .sum(),
            }
        elif pair_type == self.prompt_col:
            return (
                data[self.prompt_col]
                .apply(lambda x: x.lower().count(keyword.lower()))
                .sum()
            )
        elif pair_type == self.response_col:
            return (
                data[self.response_col]
                .apply(lambda x: x.lower().count(keyword.lower()))
                .sum()
            )
        else:
            raise ValueError(
                f"Invalid pair_type. Choose from '{self.prompt_col}', '{self.response_col}', 'both'"
            )

    def create_prompt_matrix(self) -> csr_matrix:
        """Creates a sparse matrix of prompts"""
        vectorizer = TfidfVectorizer()
        return vectorizer.fit_transform(self.data[self.prompt_col].tolist())

    def filter_data(self, word: str, pair_type: str = None) -> List[str]:
        """Returns the data that contain a specific word"""
        if pair_type not in [self.prompt_col, self.response_col]:
            raise ValueError(
                f"Invalid pair_type. Choose from '{self.prompt_col}', '{self.response_col}'"
            )
        data_column = (
            self.prompt_col if pair_type == self.prompt_col else self.response_col
        )
        data = self.data[data_column].tolist()
        return [text for text in data if word in text]

    def count_occurrences(self, word: str, pair_type: str = "prompt") -> int:
        """Counts the number of occurrences of a word in the data"""
        if pair_type not in [self.prompt_col, self.response_col, "both"]:
            raise ValueError(
                f"Invalid pair_type. Choose from '{self.prompt_col}', '{self.response_col}', 'both'"
            )

        text = ""
        if pair_type in [self.prompt_col, "both"]:
            text += " ".join(self.data[self.prompt_col].tolist())

        if pair_type in [self.response_col, "both"]:
            text += " ".join(self.data[self.response_col].tolist())

        return Counter(text.split())[word]

    def find_similar(
        self, text: str, top_n: int = 1, pair_type: str = None
    ) -> List[str]:
        """
        Finds the top_n most similar data to the input text based on TF-IDF cosine similarity.

        Args:
            text (str): The input text for which similar data is to be found.
            top_n (int): Number of top similar data to return.
            pair_type (str): Column to consider for similarity; should be either prompt_col or response_col.

        Returns:
            List[str]: List of the top_n most similar data to the input text.
        """

        if pair_type not in [self.prompt_col, self.response_col]:
            raise ValueError(
                f"Invalid pair_type. Choose from '{self.prompt_col}', '{self.response_col}'"
            )

        data_column = (
            self.prompt_col if pair_type == self.prompt_col else self.response_col
        )
        data = self.data[data_column].tolist()

        # Compute the TF-IDF vectors for the existing data and the input text
        vectorizer = TfidfVectorizer().fit_transform(data + [text])

        # Compute the cosine similarities between the input text and existing data
        cosine_similarities = cosine_similarity(vectorizer[-1], vectorizer).flatten()[
            :-1
        ]

        # Get the indices of the top_n most similar data
        similar_indices = cosine_similarities.argsort()[-top_n:][::-1]

        # Return the top_n most similar data
        return [data[i] for i in similar_indices]
