from concurrent.futures import ThreadPoolExecutor, as_completed
from .generator import PromptGenerator, log_handler, setup_logging
from typing import Optional, List, Tuple, Union, Callable, Any


class SynergyParrallel:
    def __init__(self, openai_api_key: str, path_to_dataset: Optional[str] = None):
        self.generator = PromptGenerator(openai_api_key, path_to_dataset)

    def generate_prompts_parallel(
        self, num_prompts: int, max_workers: int, batch_size: int
    ) -> None:
        example_pairs = self.generator.data_engine.get_random_example_pairs()
        generated_prompts = set()
        total_batches = (num_prompts + batch_size - 1) // batch_size

        valid_count = 0
        invalid_count = 0

        for batch_num in range(total_batches):
            log_handler(f"Generating batch {batch_num + 1}/{total_batches}...")

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []

                for i in range(
                    min(batch_size, num_prompts - valid_count)
                ):  # only generate needed prompts
                    prompt, answer = example_pairs.pop()
                    while (prompt, answer) in generated_prompts:
                        prompt, answer = example_pairs.pop()
                    generated_prompts.add((prompt, answer))

                    future = executor.submit(
                        self.generator.generate_prompt_task,
                        prompt,
                        answer,
                    )
                    futures.append(future)

                for future in as_completed(futures):
                    try:
                        future.result()
                        valid_count += 1
                    except Exception as e:
                        print(f"Error generating prompt: {e}")
                        invalid_count += 1

            log_handler(
                f"Generated {valid_count} prompts, {invalid_count} failed to generate."
            )

            if (
                valid_count >= num_prompts
            ):  # break the loop if we have generated enough prompts
                break

            try:
                example_pairs = self.generator.data_engine.get_random_example_pairs()
            except Exception as e:
                print(f"Error loading dataset: {e}")
                break

        # process any remaining prompts
        if valid_count < num_prompts:
            remaining_prompts = num_prompts - valid_count
            log_handler(f"Generating {remaining_prompts} remaining prompts...")

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []

                for i in range(remaining_prompts):
                    prompt, answer = example_pairs.pop()
                    while (prompt, answer) in generated_prompts:
                        prompt, answer = example_pairs.pop()
                    generated_prompts.add((prompt, answer))

                    future = executor.submit(
                        self.generator.generate_prompt_task,
                        prompt,
                        answer,
                    )
                    futures.append(future)

                for future in as_completed(futures):
                    try:
                        future.result()
                        valid_count += 1
                    except Exception as e:
                        print(f"Error generating prompt: {e}")
                        invalid_count += 1

            log_handler(
                f"Finished generating prompts. Total valid: {valid_count}, total invalid: {invalid_count}."
            )
