from typing import Optional, Callable, Union, Tuple, List
import os
import re
import json
import glob
import logging


class DataLoader:
    def __init__(self, prompt_dir: str, verbose: bool = False):
        self.prompt_dir = prompt_dir
        self.logger = logging.getLogger("DataPromptLoader")
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def traverse_keys(
        self,
        data: dict,
        keys: List[str],
        return_all_values: bool = False,
        include_key_with_value: bool = False,
        callback: Optional[Callable] = None,
    ) -> Union[dict, List[dict], List[Tuple[str, dict]], None]:
        """
        Traverse through the keys in the given data.

        Args:
            data (dict): Data to traverse.
            keys (List[str]): List of keys to follow.
            return_all_values (bool, optional): If True, returns all values from the keys. Defaults to False.
            include_key_with_value (bool, optional): If True, returns a tuple of key and value. Defaults to False.
            callback (Optional[Callable], optional): A function to apply to each value as it is retrieved. Defaults to None.

        Returns:
            Union[dict, List[dict], List[Tuple[str, dict]], None]: Resulting value(s) or None if keys are not found.
        """

        # Initialize a list to store all values if return_all_values is True
        all_values = []

        try:
            # Iterate through the provided keys to traverse the data
            for key in keys:
                # Check if the key exists in the current level of the data
                if isinstance(data, dict) and key in data:
                    value = data[key]

                    # Apply the callback function to the value if provided
                    if callback:
                        value = callback(value)

                    # If return_all_values is True, store the value (and key if include_key_with_value is True)
                    if return_all_values:
                        result = (key, value) if include_key_with_value else value
                        all_values.append(result)

                    # Move to the next level of the data using the current key
                    data = value
                else:
                    # If the key is not found, return None
                    return None

            # Return either all the values or the final value, depending on return_all_values
            return all_values if return_all_values else data

        except Exception as e:
            # Log an error if an exception occurs during traversal
            self.logger.error(f"Error traversing keys {keys}: {str(e)}")
            return None

    def get_prompt_files(
        self,
        directory: str,
        file_pattern: str = "**/*.json",
        sort_function: Optional[Callable] = None,
    ) -> List[str]:
        """
        Retrieve the list of prompt files from a specified directory.

        Args:
            directory (str): The directory to search for prompt files.
            file_pattern (str, optional): The pattern to match files. Defaults to "**/*.json" (matches all JSON files in the directory).
            sort_function (Callable, optional): A custom sorting function. Defaults to None.

        Returns:
            List[str]: A list of paths to prompt files.
        """

        # Use glob to match all files in the directory with the specified pattern (e.g., all JSON files).
        prompt_files = glob.glob(os.path.join(directory, file_pattern))

        # Sort the files using the custom sort function if provided.
        if sort_function:
            prompt_files.sort(key=sort_function)
        else:
            # If no custom sort function is provided, sort the files based on the numeric part in their filenames.
            prompt_files.sort(
                key=lambda f: int(re.search(r"\d+", os.path.basename(f)).group())
                if re.search(r"\d+", os.path.basename(f))
                else 0
            )

        # Return the list of prompt files.
        return prompt_files

    def filter_by_prefix(
        self,
        data: Union[List[str], List[dict]],
        prefix: str,
        include_more: bool = False,
        case_sensitive: bool = False,
        match_strategy: str = "start",
    ) -> List[Union[str, dict]]:
        """
        Filter the given data based on the provided prefix.

        Args:
            data (Union[List[str], List[dict]]): Data to filter. Accepts both string lists and dictionaries.
            prefix (str): Prefix to match against each data item.
            include_more (bool, optional): Include data with content beyond the prefix. Defaults to False.
            case_sensitive (bool, optional): Consider case in matching. Defaults to False.
            match_strategy (str, optional): Matching strategy ("start", "exact", "contains"). Defaults to "start".

        Returns:
            List[Union[str, dict]]: Filtered data.
        """

        # Convert the prefix to lowercase if case sensitivity is not required.
        if not case_sensitive:
            prefix = prefix.lower()

        # Inner function to determine if an item matches the prefix based on the specified match strategy.
        def match(item):
            # Convert the item to string for uniformity, and make it lowercase if case sensitivity is off.
            content = item if isinstance(item, str) else str(item)
            if not case_sensitive:
                content = content.lower()

            # Determine if the content matches the prefix based on the match strategy.
            if match_strategy == "start":
                return content.startswith(prefix)
            elif match_strategy == "exact":
                return content == prefix
            elif match_strategy == "contains":
                return prefix in content
            else:
                # Log an error if an unknown match strategy is used.
                self.logger.error(f"Unknown match strategy: {match_strategy}")
                return False

        # Apply the match function to filter the data based on the prefix.
        filtered_data = [item for item in data if match(item)]

        # If the include_more option is enabled, filter the data to include items with more content than the prefix.
        if include_more:
            filtered_data = [
                item
                for item in filtered_data
                if len(str(item).strip()) > len(prefix) and str(item).strip() != prefix
            ]

        # Return the filtered data.
        return filtered_data

    def process_prompt_file(
        self,
        prompt_file: str,
        keys: List[str],
        return_all_values: bool,
        include_key_with_value: bool,
        callback: Optional[Callable],
    ) -> dict:
        try:
            file_data = self.load_json_file(prompt_file)
            return self.traverse_keys(
                file_data,
                keys,
                return_all_values=return_all_values,
                include_key_with_value=include_key_with_value,
                callback=callback,
            )
        except Exception as e:
            self.logger.error(f"Error processing file {prompt_file}: {str(e)}")
            return None

    def load_json_file(self, file_path: str) -> dict:
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading file {file_path}: {str(e)}")
            return None

    def process_loader(
        self,
        mode: str,  # 'data' or 'prompts'
        keys: List[str] = ["mapping"],
        key: str = "prompt",
        min_length: Optional[int] = None,
        prefix: Optional[str] = None,
        include_more: bool = False,
        directory: Optional[str] = None,
        file_pattern: Optional[str] = "**/*.json",
        sort_function: Optional[Callable] = None,
        return_all_values: bool = False,
        include_key_with_value: bool = False,
        callback: Optional[Callable] = None,
        case_sensitive: bool = False,
        match_strategy: str = "start",
    ) -> Union[List[dict], List[Tuple[str, dict]], None]:
        """
        A consolidated function to load data or prompts based on the specified mode.

        Args:
            mode (str): Specifies the mode of operation; 'data' to load data, 'prompts' to load prompts.
            keys (List[str]): List of keys to traverse when loading data. Used only in 'data' mode.
            key (str): Key to access the prompt object in the JSON file. Used only in 'prompts' mode.
            min_length (Optional[int]): Minimum length of the prompt objects to filter.
            prefix (Optional[str]): Prefix to check for in the first index of each prompt object.
            include_more (bool): Whether to include objects with content beyond the specified prefix.
            directory (Optional[str]): Directory to search for JSON files.
            file_pattern (Optional[str]): File pattern to search for within the directory.
            sort_function (Optional[Callable]): Optional custom sort function for sorting files.
            return_all_values (bool): Whether to return all values when traversing keys. Used only in 'data' mode.
            include_key_with_value (bool): Whether to include the key with the value. Used only in 'data' mode.
            callback (Optional[Callable]): Optional callback function when traversing keys. Used only in 'data' mode.
            case_sensitive (bool): Consider case when matching prefix. Used only in 'data' mode.
            match_strategy (str): Matching strategy for prefix ("start", "exact", "contains"). Used only in 'data' mode.

        Returns:
            Union[List[dict], List[Tuple[str, dict]], None]: List of loaded data or prompts, or None if no objects are found.
        """

        # Function to clean prompt objects by removing leading and trailing whitespaces.
        def clean_prompt_object(prompt_object: List[str]) -> List[str]:
            return [item.strip() for item in prompt_object]

        # Determine directory, falling back to the class attribute if not provided.
        directory = directory or self.prompt_dir

        # Retrieve the sorted list of prompt files based on the provided pattern.
        prompt_files = self.get_prompt_files(directory, file_pattern, sort_function)

        # Initialize a list to store the processed prompt objects.
        prompt_objects = []

        # Iterate through the prompt files and process them based on the specified mode.
        for prompt_file in prompt_files:
            if mode == "data":
                # In 'data' mode, use a custom function to process the file and traverse keys.
                prompt_data = self.process_prompt_file(
                    prompt_file,
                    keys,
                    return_all_values,
                    include_key_with_value,
                    callback,
                )
                if prompt_data:
                    prompt_objects.append(prompt_data)
            elif mode == "prompts":
                # In 'prompts' mode, simply read the JSON file and access the specified key.
                with open(prompt_file, "r") as f:
                    prompt_object = json.load(f)
                prompt_objects.append(prompt_object[key])

        # Apply the minimum length filter if specified.
        if min_length:
            prompt_objects = [
                prompt for prompt in prompt_objects if len(prompt) >= min_length
            ]

        # If in 'prompts' mode, clean the prompt objects and apply the prefix filter if needed.
        if mode == "prompts":
            prompt_objects = [clean_prompt_object(prompt) for prompt in prompt_objects]

            if prefix:
                prefix = prefix.strip()
                prompt_objects = [
                    prompt for prompt in prompt_objects if prompt[0] == prefix
                ]

                if include_more:
                    prompt_objects = [
                        prompt
                        for prompt in prompt_objects
                        if len(prompt[0]) > len(prefix) and prompt[0].strip() != prefix
                    ]

        # If in 'data' mode and prefix is specified, apply the custom filter function.
        if mode == "data" and prefix:
            prompt_objects = self.filter_by_prefix(
                prompt_objects, prefix, include_more, case_sensitive, match_strategy
            )

        # Return the prompt objects if found, else None.
        return prompt_objects if prompt_objects else None

    def load_data_prompts(
        self,
        keys: List[str] = ["prompt"],
        min_length: Optional[int] = None,
        prefix: Optional[str] = None,
        include_more: bool = False,
        directory: Optional[str] = None,
        file_pattern: Optional[str] = "**/*.json",
        sort_function: Optional[Callable] = None,
    ) -> List[dict]:
        prompt_objects = []

        # If no directory specified, use the default one
        dir_to_use = directory if directory else self.prompt_dir

        # Recursive function to traverse nested directories and find matching files
        prompt_files = glob.glob(os.path.join(dir_to_use, file_pattern))

        # If a custom sorting function is provided
        if sort_function:
            prompt_files.sort(key=sort_function)
        else:
            # Default sorting mechanism
            prompt_files.sort(
                key=lambda f: int(re.sub("\D", "", os.path.basename(f)))
                if re.sub("\D", "", os.path.basename(f))
                else 0
            )
        for prompt_file in prompt_files:
            with open(prompt_file, "r") as f:
                prompt_object = json.load(f)

            # Traverse the nested structure using the provided keys
            for key in keys:
                prompt_object = prompt_object.get(key, {})
            if prompt_object:
                prompt_objects.append(prompt_object)

        # Filter the prompt objects based on the minimum length if specified
        if min_length is not None:
            prompt_objects = [
                prompt for prompt in prompt_objects if len(prompt) >= min_length
            ]

        def clean_prompt_object(prompt_object: List[str]) -> List[str]:
            """
            Clean the prompt object by removing leading and trailing whitespaces from each element.

            Args:
                prompt_object (List[str]): The prompt object to clean.

            Returns:
                List[str]: The cleaned prompt object.
            """
            return [item.strip() for item in prompt_object]

        # Clean the prompt objects by removing leading and trailing whitespaces
        prompt_objects = [clean_prompt_object(prompt) for prompt in prompt_objects]

        # Check if the first index of each prompt object starts with the provided prefix
        if prefix is not None:
            # Clean the prefix by removing leading and trailing whitespaces
            prefix = prefix.strip()
            prompt_objects = [
                prompt for prompt in prompt_objects if prompt.startswith(prefix)
            ]

            # Optionally include prompt objects with content beyond the specified prefix
            if include_more:
                prompt_objects = [
                    prompt
                    for prompt in prompt_objects
                    if len(prompt) > len(prefix) and prompt.strip() != prefix
                ]

        return prompt_objects if prompt_objects else None
