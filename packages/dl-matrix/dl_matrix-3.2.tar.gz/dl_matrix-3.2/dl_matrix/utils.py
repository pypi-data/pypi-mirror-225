import logging
from typing import List, Dict, Any, Tuple, Optional, Iterable, Union
import uuid
import os
import json


class APIFailureException(Exception):
    pass


def log_handler(message: str, level: str = "info"):
    """
    Handle logging with different log levels.
    """

    if level.lower() == "info":
        logging.info(message)
    elif level.lower() == "warning":
        logging.warning(message)
    elif level.lower() == "error":
        logging.error(message)


def setup_logging():
    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler("dl_matrix/infrence/logs/synergy_chat.log"),
            logging.StreamHandler(),
        ],
    )


def generate_id() -> str:
    return str(uuid.uuid4())


def split_string_to_parts(raw: str, delimiter: str = "\n") -> List[str]:
    return raw.split(delimiter)


def get_from_dict_or_env(
    data: Dict[str, Any], key: str, env_key: str, default: Optional[str] = None
) -> str:
    """Get a value from a dictionary or an environment variable."""
    if key in data and data[key]:
        return data[key]
    else:
        return get_from_env(key, env_key, default=default)


def get_from_env(key: str, env_key: str, default: Optional[str] = None) -> str:
    """Get a value from a dictionary or an environment variable."""
    if env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    elif default is not None:
        return default
    else:
        raise ValueError(
            f"Did not find {key}, please add an environment variable"
            f" `{env_key}` which contains it, or pass"
            f"  `{key}` as a named parameter."
        )


def _flatten_dict(
    nested_dict: Dict[str, Any], parent_key: str = "", sep: str = "_"
) -> Iterable[Tuple[str, Any]]:
    """
    Generator that yields flattened items from a nested dictionary for a flat dict.

    Parameters:
        nested_dict (dict): The nested dictionary to flatten.
        parent_key (str): The prefix to prepend to the keys of the flattened dict.
        sep (str): The separator to use between the parent key and the key of the
            flattened dictionary.

    Yields:
        (str, any): A key-value pair from the flattened dictionary.
    """
    for key, value in nested_dict.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            yield from _flatten_dict(value, new_key, sep)
        else:
            yield new_key, value


def flatten_dict(
    nested_dict: Dict[str, Any], parent_key: str = "", sep: str = "_"
) -> Dict[str, Any]:
    """Flattens a nested dictionary into a flat dictionary.

    Parameters:
        nested_dict (dict): The nested dictionary to flatten.
        parent_key (str): The prefix to prepend to the keys of the flattened dict.
        sep (str): The separator to use between the parent key and the key of the
            flattened dictionary.

    Returns:
        (dict): A flat dictionary.

    """
    flat_dict = {k: v for k, v in _flatten_dict(nested_dict, parent_key, sep)}
    return flat_dict


def manage_conversations(
    path_1: str,
    path_2: str,
    output_path: str,
    key_field: str = "create_time",
    operation_mode: str = "update",
    strict_mode: bool = False,
    target_num: int = None,  # Added the target_num parameter
    verbose: bool = True,
    save_result: bool = True,
) -> List[Dict[str, Any]]:
    # Nested helper functions
    def log(message: str):
        if verbose:
            print(message)

    def load_json_data(path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(path):
            log(f"Error: File {path} does not exist.")
            return []
        with open(path, "r") as file:
            data = json.load(file)
        if not isinstance(data, list) or not all(
            isinstance(item, dict) for item in data
        ):
            log(f"Error: File {path} doesn't contain a list of dictionaries.")
            return []
        return data

    data_1 = load_json_data(path_1)
    data_2 = load_json_data(path_2)

    if not data_1 or not data_2:
        log("Error: One or both input files are not loaded properly.")
        return []

    # Filter the conversations based on the length of mapping attribute
    if target_num is not None:
        data_1 = [item for item in data_1 if len(item.get("mapping", [])) >= target_num]
        data_2 = [item for item in data_2 if len(item.get("mapping", [])) >= target_num]

    keys_1 = {item.get(key_field) for item in data_1 if key_field in item}
    keys_2 = {item.get(key_field) for item in data_2 if key_field in item}

    # Check for strict mode
    if strict_mode and (None in keys_1 or None in keys_2):
        log(f"Error: Missing '{key_field}' field in one or more entries.")
        return []

    # Handle the 'difference' operation
    if operation_mode == "difference":
        difference_keys = keys_2 - keys_1

        if not difference_keys:
            log("No new entries found in the second file based on the provided key.")
            return []

        result = [item for item in data_2 if item.get(key_field) in difference_keys]
        log(f"Found {len(result)} new entries based on '{key_field}'.")

    # Handle the 'update' operation
    elif operation_mode == "update":
        # Conversations unique to data_1
        unique_to_data_1 = [
            item for item in data_1 if item.get(key_field) not in keys_2
        ]

        # Conversations present in both but taking the version from data_1
        shared_keys = keys_1.intersection(keys_2)
        updated_shared_conversations = [
            item for item in data_1 if item.get(key_field) in shared_keys
        ]

        # Conversations unique to data_2
        unique_to_data_2 = [
            item for item in data_2 if item.get(key_field) not in keys_1
        ]

        result = unique_to_data_1 + updated_shared_conversations + unique_to_data_2
        log(f"Total of {len(result)} entries after updating.")

    else:
        log(f"Error: Invalid operation mode '{operation_mode}'.")
        return []

    if save_result:
        with open(output_path, "w") as file_output:
            json.dump(result, file_output)
        log(f"Saved results to {output_path}.")

    return result


def load_json(source: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    if not os.path.isfile(source):
        raise ValueError(f"{source} does not exist.")
    with open(source, "r") as f:
        data = json.load(f)
    return data


def save_json(path: str, data: Union[Dict[str, Any], List[Dict[str, Any]]]):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def combine_json_files(path1: str, path2: str, output_path: str) -> None:
    data1 = load_json(path1)
    data2 = load_json(path2)

    if not isinstance(data1, list) or not isinstance(data2, list):
        raise ValueError("Both input files should contain a list of JSON objects.")

    combined_data = data1 + data2

    save_json(output_path, combined_data)
    print(f"Combined data saved to {output_path}.")


class InvalidChainTypeException(Exception):
    pass


class InvalidIdException(Exception):
    pass


class InvalidContentException(Exception):
    pass


class InvalidCoordinateException(Exception):
    pass
