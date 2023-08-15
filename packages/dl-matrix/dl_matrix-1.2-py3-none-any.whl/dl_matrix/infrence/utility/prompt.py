import os
import re
import json
import glob
import logging
from enum import Enum
from typing import Optional, Tuple, Union


class PromptStatus(Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"
    NOT_FOUND = "Not Found"


class PromptManager:
    def __init__(
        self, prompt_directory: str, filename_pattern: str = "synergy_chat_{}.json"
    ):
        """
        Initialize the PromptManager.

        Args:
        - prompt_directory (str): The directory where prompts will be stored.
        - filename_pattern (str): The pattern for filenames. '{}' is replaced by the prompt number.
        """
        self.prompt_directory = prompt_directory
        self.filename_pattern = filename_pattern
        os.makedirs(prompt_directory, exist_ok=True)

        # Logger setup
        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _get_prompt_file_path(self, prompt_num: int) -> str:
        """Generate the file path based on the prompt number."""
        return os.path.join(
            self.prompt_directory, self.filename_pattern.format(prompt_num)
        )

    def load_prompt(self, prompt_num: Optional[int] = None) -> dict:
        """Load a prompt object."""
        if not prompt_num:
            prompt_num = self.get_last_prompt_num()

        prompt_path = self._get_prompt_file_path(prompt_num)
        if os.path.exists(prompt_path):
            with open(prompt_path, "r") as f:
                return json.load(f)
        else:
            self.logger.warning(f"Prompt {prompt_num} file does not exist.")
            return {"status": PromptStatus.NOT_FOUND.value}

    def get_last_prompt_num(self) -> int:
        """Retrieve the number of the latest prompt."""
        prompt_files = glob.glob(
            os.path.join(self.prompt_directory, self.filename_pattern.format("*"))
        )
        if prompt_files:
            prompt_files.sort(
                key=lambda f: int(re.search(r"\d+", os.path.basename(f)).group())
            )
            return int(re.search(r"\d+", os.path.basename(prompt_files[-1])).group())
        return 0

    def create_prompt_object(self, prompt_parts: list) -> dict:
        """Construct a new prompt object."""
        if not prompt_parts:
            self.logger.error("No content provided for the prompt.")
            return {"status": PromptStatus.FAILURE.value}

        prompt_num = self.get_last_prompt_num() + 1
        prompt_object = {
            "prompt_num": prompt_num,
            "prompt": prompt_parts,
            "status": PromptStatus.SUCCESS.value,
        }
        self.logger.info(f"New prompt object {prompt_num} created.")
        return prompt_object

    def save_prompt_object(self, prompt_object: dict):
        """Save the prompt object to a file."""
        try:
            prompt_path = self._get_prompt_file_path(prompt_object["prompt_num"])
            with open(prompt_path, "w") as f:
                json.dump(prompt_object, f, indent=4)
            self.logger.info(f"Prompt {prompt_object['prompt_num']} saved.")
        except Exception as e:
            self.logger.error(f"Failed to save prompt: {e}")
            return {"status": PromptStatus.FAILURE.value}
        return {"status": PromptStatus.SUCCESS.value}

    def delete_prompt(self, prompt_num: int):
        """Remove a specific prompt."""
        try:
            prompt_path = self._get_prompt_file_path(prompt_num)
            if os.path.exists(prompt_path):
                os.remove(prompt_path)
                self.logger.info(f"Prompt {prompt_num} deleted.")
            else:
                self.logger.warning(f"Prompt {prompt_num} does not exist.")
        except Exception as e:
            self.logger.error(f"Failed to delete prompt {prompt_num}: {e}")

    def list_prompts(self) -> list:
        """List all available prompt filenames."""
        return [
            os.path.basename(f)
            for f in glob.glob(
                os.path.join(self.prompt_directory, self.filename_pattern.format("*"))
            )
        ]

    def delete_all_prompts(self):
        """Remove all prompts."""
        for f in glob.glob(
            os.path.join(self.prompt_directory, self.filename_pattern.format("*"))
        ):
            os.remove(f)
        self.logger.info("All prompts deleted.")

    def get_prompt_status(self, prompt_num: int) -> str:
        """Retrieve the status of a prompt."""
        prompt = self.load_prompt(prompt_num)
        return prompt["status"] if "status" in prompt else PromptStatus.NOT_FOUND.value

    def create_prompt_from_example(self, example: Tuple[str, str]) -> Union[dict, None]:
        """
        Create a prompt from an example.

        Args:
        - example (Tuple[str, str]): An example tuple where the first element
          contains the prompt data, and the second element is unused in this context.

        Returns:
        - dict or None: The created prompt object or None in case of failure.
        """
        if not isinstance(example, tuple) or len(example) != 2:
            self.logger.error(
                "Provided example is not in the expected format (Tuple[str, str])."
            )
            return None

        prompt_parts = example[0].split("\n")
        if not prompt_parts:
            self.logger.warning(
                "No valid content found in the provided example for prompt creation."
            )
            return None

        return self.create_prompt_object(prompt_parts)

    def create_prompt_from_text(self, text: str) -> Union[dict, None]:
        """
        Create a prompt from a text string.

        Args:
        - text (str): The text string to use for the prompt.

        Returns:
        - dict or None: The created prompt object or None in case of failure.
        """
        if not isinstance(text, str):
            self.logger.error("Provided text is not a string.")
            return None

        prompt_parts = text.split("\n")
        if not prompt_parts:
            self.logger.warning("No valid content found in the provided text.")
            return None

        return self.create_prompt_object(prompt_parts)
