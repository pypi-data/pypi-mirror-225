from dl_matrix.base import (
    create_user_message,
    create_assistant_message,
    create_system_message,
)
from dl_matrix.embedding import SpatialSimilarity, calculate_similarity
from typing import List, Optional, Dict, Any
from dl_matrix.type import ElementType
import uuid
from dl_matrix.models import ChainMap, NodeRelationship, ChainTree
from dl_matrix.type import NodeRelationship
import time
import numpy as np
import pandas as pd
import glob
import re
import os
import json


class HierarchicalProcessor:
    def __init__(self, prompt_dir: str, key: str):
        """
        Initialize a PromptLoader with a specified directory and a semantic model.
        """
        self.prompt_dir = prompt_dir
        self.key = key
        self.semantic_model = SpatialSimilarity()
        self.hierarchy_dir = "hierarchy"
        self.embedding_size = 768

    def load_hierarchy(self, hierarchy_file_path: str = "hierarchy.json") -> ChainTree:
        """
        Load the hierarchy from a JSON file.

        Args:
            hierarchy_file_path (str, optional): The path to the hierarchy JSON file. Defaults to "hierarchy.json".

        Returns:
            ChainTree: The loaded hierarchy.
        """
        try:
            with open(hierarchy_file_path, "r") as f:
                hierarchy = ChainTree.parse_obj(json.load(f))
            return hierarchy
        except Exception as e:
            print(f"Error loading hierarchy: {e}")
            return None

    def save_hierarchy(
        self, hierarchy: ChainTree, hierarchy_file_path: str = "hierarchy.json"
    ) -> None:
        """
        Save the hierarchy to a JSON file.

        Args:
            hierarchy (ChainTree): The hierarchy to save.
        """
        try:
            with open(hierarchy_file_path, "w") as f:
                json.dump(hierarchy.dict(), f, indent=4)
        except Exception as e:
            print(f"Error saving hierarchy: {e}")

    def create_hierarchy(
        self, df: pd.DataFrame, element_type: ElementType
    ) -> List[ChainTree]:
        """
        Create a hierarchy with the prefix as the parent and the element index as the count of children.

        Args:
            df (pd.DataFrame): The DataFrame containing the elements and their embeddings.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).

        Returns:
            List[ChainTree]: A list of ChainTree objects representing the hierarchy.
        """
        conversations = []

        for i, row in df.iterrows():  # Use i as the index for the element
            prefix_text = row[
                element_type.value + " 0"
            ]  # Use the element_type for column selection
            prefix_id = str(uuid.uuid4())
            prefix_embeddings = row[
                element_type.value + " 0 embedding"
            ]  # Use the element_type for column selection
            # Create the System message
            system_message = create_system_message()

            # Create the User message for the prefix
            prefix_user_message = create_user_message(
                message_id=prefix_id,
                text=prefix_text,
                user_embeddings=prefix_embeddings.tolist(),
            )

            # Create the ChainMap for the prefix
            prefix_chain_map = ChainMap(
                id=prefix_id,
                message=prefix_user_message,
                parent=system_message.id,
                children=[],
                references=[],
                relationships={
                    NodeRelationship.SOURCE: system_message.id,
                },
            )

            # Append the prefix chain map to the list of conversations
            conversations.append(
                ChainTree(
                    title=f"{i}",  # Use i as the title
                    create_time=time.time(),
                    update_time=time.time(),
                    mapping={
                        system_message.id: ChainMap(
                            id=system_message.id,
                            message=system_message,
                            children=[prefix_user_message.id],
                        ),
                        prefix_user_message.id: prefix_chain_map,
                    },
                    current_node=prefix_user_message.id,
                )
            )

            # Initialize the ID of the previous assistant message to the prefix
            previous_assistant_message_id = prefix_user_message.id

            # Add the element chain maps as children to the prefix chain map
            for j in range(1, len(df.columns)):
                element_col = f"{element_type.value} {j}"
                element_text = row.get(
                    element_col, ""
                )  # Use get method to safely access the column
                if not element_text:
                    continue

                element_id = str(uuid.uuid4())  # Generate a new UUID for each element
                element_embeddings = row.get(
                    f"{element_col} embedding"
                )  # Use get method for embeddings

                # Create the Assistant message for the element
                element_assistant_message = create_assistant_message(
                    text=element_text,
                    assistant_embeddings=element_embeddings.tolist(),
                )

                # Create the ChainMap for the element
                element_chain_map = ChainMap(
                    id=element_id,
                    message=element_assistant_message,
                    parent=prefix_id,
                    children=[],
                    references=[],
                    relationships={
                        NodeRelationship.PARENT: prefix_id,
                        NodeRelationship.PREVIOUS: previous_assistant_message_id,  # Add the previous assistant message's ID
                    },
                )

                # Append the element chain map to the prefix chain map's children
                prefix_chain_map.children.append(element_chain_map.id)

                # Add the element chain map to the mapping of the same ChainTree
                conversations[-1].mapping[
                    element_assistant_message.id
                ] = element_chain_map

                # Update the ID of the previous assistant message to the current element's assistant message ID
                previous_assistant_message_id = element_assistant_message.id

        return conversations

    def group_similar_terms_from_dict(
        self, embedding_dict: Dict[str, np.ndarray], similarity_threshold: float = 0.9
    ) -> List[str]:
        """
        Group similar terms based on their embeddings.
        Return the resulting list of grouped terms.

        Args:
            embedding_dict (Dict[str, np.ndarray]): The dictionary containing the terms and their embeddings.
            similarity_threshold (float, optional): The similarity threshold for grouping similar terms.
                Defaults to 0.9.

        Returns:
            List[str]: The list of grouped terms.
        """
        try:
            # Group similar terms based on their embeddings
            grouped_terms = []
            for term in embedding_dict.keys():
                if term not in grouped_terms:
                    grouped_terms.append(term)
                    for other_term in embedding_dict.keys():
                        if (
                            other_term not in grouped_terms
                            and calculate_similarity(
                                embedding_dict[term], embedding_dict[other_term]
                            )
                            >= similarity_threshold
                        ):
                            grouped_terms.append(other_term)

            return grouped_terms

        except Exception as e:
            print(f"Error grouping similar terms: {e}")
            return []

    def get_top_n_similar_terms(
        self,
        df: pd.DataFrame,
        element_type: ElementType,
        embedding_column: str,
        term: str,
        n: int = 5,
    ) -> pd.DataFrame:
        """
        Get the top n similar terms for a given term based on their embeddings.
        Return the resulting DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the elements and their embeddings.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).
            embedding_column (str): The name of the column containing the embeddings.
            term (str): The term for which to find similar terms.
            n (int, optional): The number of similar terms to return. Defaults to 5.

        Returns:
            pd.DataFrame: The DataFrame with the top n similar terms.
        """
        try:
            # Get the embeddings for the given term
            term_embeddings = df[df[element_type.value] == term][embedding_column]

            # Calculate the similarity between the term and all other terms
            df_copy = (
                df.copy()
            )  # Create a copy of the DataFrame to avoid potential warnings
            df_copy["Similarity"] = df_copy[embedding_column].apply(
                lambda x: calculate_similarity(term_embeddings, x)
            )

            # Sort the DataFrame by similarity and return the top n similar terms
            return df_copy.sort_values(by="Similarity", ascending=False).head(n)

        except Exception as e:
            print(f"Error getting top n similar terms: {e}")
            return pd.DataFrame()

    def group_similar_terms(
        self,
        df: pd.DataFrame,
        element_type: ElementType,
        embedding_column: str,
        similarity_threshold: float = 0.9,
    ) -> pd.DataFrame:
        """
        Group similar terms in the DataFrame based on their embeddings.
        Return the resulting DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the elements and their embeddings.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).
            embedding_column (str): The name of the column containing the embeddings.
            similarity_threshold (float, optional): The similarity threshold for grouping similar terms.
                Defaults to 0.9.

        Returns:
            pd.DataFrame: The DataFrame with grouped similar terms.
        """
        try:
            # Group similar terms based on their embeddings
            df_copy = (
                df.copy()
            )  # Create a copy of the DataFrame to avoid potential warnings
            embedding_dict = dict(
                zip(df_copy[element_type.value], df_copy[embedding_column])
            )
            grouped_terms = self.group_similar_terms_from_dict(
                embedding_dict, similarity_threshold
            )

            # Add the grouped terms to the DataFrame
            df_copy[element_type.value] = grouped_terms

            return df_copy

        except Exception as e:
            print(f"Error grouping similar terms: {e}")
            return pd.DataFrame()

    def build_hierarchy(
        self,
        conversations: List[List[ChainTree]],
        similarity_threshold: float = 0.8,
    ) -> ChainTree:
        """
        Build a hierarchy from a list of conversations.

        Args:
            conversations (List[List[ChainTree]]): A list of conversations.
            similarity_threshold (float): The threshold for considering messages as similar.

        Returns:
            ChainTree: The hierarchy.
        """
        # Merge the conversations into a single hierarchy
        merged_hierarchy = self.combined_hierarchy(conversations)

        # Build another layer of hierarchy based on assistant messages' similarity
        new_hierarchy = self.build_assistant_hierarchy(
            merged_hierarchy, similarity_threshold
        )

        return new_hierarchy

    def compute_embeddings(
        self, df: pd.DataFrame, element_type: ElementType, separate_columns: bool = True
    ) -> pd.DataFrame:
        """
        Compute embeddings for each step.

        Args:
            df (pd.DataFrame): The DataFrame containing the steps.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).
            separate_columns (bool, optional): Whether to separate the columns (Prefix and Steps)
                during the embedding process. Defaults to True.

        Returns:
            pd.DataFrame: The DataFrame with added columns for embeddings.
        """
        try:
            # Prepare the data for embedding
            if separate_columns:
                # Separate the columns (Prefix and Elements) and drop NaN values
                element_columns = [
                    col for col in df.columns if col.startswith(element_type.value)
                ]
                all_elements = pd.concat(
                    [df[col] for col in element_columns], ignore_index=True
                )
                prefix = pd.Series(
                    dtype=str
                )  # Explicitly specify the dtype of the empty Series
            else:
                # Combine all columns (Prefix and Elements) into a single column and drop NaN values
                all_elements = df.stack().dropna()
                prefix = pd.Series(
                    dtype=str
                )  # Explicitly specify the dtype of the empty Series

            # Compute embeddings for all elements
            embeddings = self.semantic_model.fit(
                all_elements.tolist() + prefix.tolist()
            )
            embedding_dict = {i: embeddings[i] for i in range(len(embeddings))}

            # Add embeddings to the DataFrame for each element
            df_copy = (
                df.copy()
            )  # Create a copy of the DataFrame to avoid potential warnings
            for col in df_copy.columns:
                if col.startswith(element_type.value):
                    element_len = len(df_copy[col])
                    embedding_col = f"{col} embedding"
                    if separate_columns:
                        # Separate columns: Add embeddings for each element separately
                        df_copy[embedding_col] = (
                            pd.Series(embedding_dict).loc[: element_len - 1].tolist()
                        )
                    else:
                        # Combined columns: Add embeddings for all elements in a single column
                        df_copy[embedding_col] = pd.Series(
                            list(embedding_dict.values())
                        )

                    embedding_dict = {
                        k - element_len: v
                        for k, v in embedding_dict.items()
                        if k >= element_len
                    }

            return df_copy

        except Exception as e:
            print(f"Error computing embeddings: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of errors

    def prepare_initial_data(
        self,
        processed_elements: List[List[str]],
        element_type: ElementType = ElementType.STEP,
    ) -> pd.DataFrame:
        """
        Create a DataFrame from the processed elements.
        Compute embeddings for each element and group similar terms.
        Perform element-wise similarity propagation and add columns for propagated similarity information.
        Retrieve pattern frequency information and add columns 'exact_frequency' and 'similar_frequency'.
        Return the resulting DataFrame.

        Args:
            processed_elements (List[List[str]]): The list of processed elements.
            element_type (ElementType, optional): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).
                Defaults to ElementType.STEP.

        Returns:
            pd.DataFrame: The DataFrame containing the elements and their embeddings.
        """
        try:
            # Check if elements are already present in the data
            if all(len(row) >= 2 for row in processed_elements):
                # Elements are already present, use the default elements
                elements = [
                    f"{element_type.value} {i}"
                    for i in range(len(processed_elements[0]) - 1)
                ]  # Subtract 1 for the prefix column
            else:
                # Elements are not present, add elements accordingly
                num_elements = (
                    len(processed_elements[0]) - 1
                )  # Subtract 1 for the prefix column
                elements = [f"{element_type.value} {i}" for i in range(num_elements)]

            # Prepare the initial data using the computed elements
            data = {"Prefix": [row[0] for row in processed_elements]}
            for i, element in enumerate(elements):
                data[element] = [
                    row[i + 1] if len(row) > (i + 1) else ""
                    for row in processed_elements
                ]

            df = pd.DataFrame(data)

            # Filter rows that do not start with the element name
            for element in elements:
                df = df[df[element].str.startswith(element + ":")]

        except Exception as e:
            print(f"Error processing elements: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of errors

        return df

    def load_data_prompts(
        self,
        min_length: Optional[int] = None,
        prefix: Optional[str] = None,
        include_more: bool = False,
    ) -> List[dict]:
        """
        Load all prompt objects from the stored JSON files.

        Args:
            min_length (int, optional): Minimum length of the prompt objects to filter. Defaults to None.
            prefix (str, optional): Prefix to check for in the first index of each prompt object. Defaults to None.
            include_more (bool, optional): Whether to include prompt objects with content beyond the specified prefix. Defaults to False.

        Returns:
            List[dict]: A list of prompt objects.
        """
        prompt_objects = []
        prompt_files = glob.glob(os.path.join(self.prompt_dir, "**/*.json"))
        if prompt_files:
            prompt_files.sort(
                key=lambda f: int(re.search(r"\d+", os.path.basename(f)).group())
            )
            for prompt_file in prompt_files:
                with open(prompt_file, "r") as f:
                    prompt_object = json.load(f)
                prompt_objects.append(prompt_object[self.key])

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
                    prompt for prompt in prompt_objects if prompt[0] == prefix
                ]

                # Optionally include prompt objects with content beyond the specified prefix
                if include_more:
                    prompt_objects = [
                        prompt
                        for prompt in prompt_objects
                        if len(prompt[0]) > len(prefix) and prompt[0].strip() != prefix
                    ]

            return prompt_objects

        else:
            print("No prompt files found.")
            return None

    def _build_assistant_hierarchy(
        self, merged_hierarchy: ChainTree, similarity_threshold: float
    ) -> ChainTree:
        """
        Build another layer of hierarchy based on assistant messages' similarity.

        Args:
            merged_hierarchy (ChainTree): The merged hierarchy.
            similarity_threshold (float): The threshold for considering messages as similar.

        Returns:
            ChainTree: A new hierarchy with additional layers based on assistant messages.
        """
        new_hierarchy = ChainTree(
            title="Assistant Hierarchy",
            create_time=time.time(),
            update_time=time.time(),
            mapping={},
            current_node=None,
        )

        # Iterate through the ChainMaps in the merged hierarchy
        for chain_map in merged_hierarchy.mapping.values():
            # Check if the ChainMap belongs to an assistant message
            if chain_map.message.author.role == "assistant":
                # Find similar assistant messages within the new hierarchy
                similar_messages = self.find_similar_messages(
                    chain_map, new_hierarchy, similarity_threshold
                )

                # Create a new ChainMap and add it to the new hierarchy
                new_chain_map = self.create_new_chain_map(
                    chain_map, similar_messages, new_hierarchy
                )
                new_hierarchy.mapping[new_chain_map.id] = new_chain_map

        # Set the current node to the first ChainMap in the new hierarchy
        new_hierarchy.current_node = list(new_hierarchy.mapping.keys())[0]

        return new_hierarchy

    def find_similar_messages(
        self, chain_map: ChainMap, hierarchy: ChainTree, similarity_threshold: float
    ) -> List[ChainMap]:
        """
        Find similar messages within a hierarchy.

        Args:
            chain_map (ChainMap): The ChainMap to find similar messages for.
            hierarchy (ChainTree): The hierarchy to find similar messages in.
            similarity_threshold (float): The threshold for considering messages as similar.

        Returns:
            List[ChainMap]: A list of similar ChainMaps.
        """
        similar_messages = []

        # Iterate through the ChainMaps in the hierarchy
        for other_chain_map in hierarchy.mapping.values():
            # Exclude the ChainMap itself
            if chain_map.id != other_chain_map.id:
                # Check if the ChainMap is similar to the ChainMap being compared
                if self.is_similar(chain_map, other_chain_map, similarity_threshold):
                    similar_messages.append(other_chain_map)

        return similar_messages

    def is_similar(
        self,
        chain_map: ChainMap,
        other_chain_map: ChainMap,
        similarity_threshold: float,
    ) -> bool:
        """
        Check if two ChainMaps are similar.

        Args:
            chain_map (ChainMap): The ChainMap to compare.
            other_chain_map (ChainMap): The other ChainMap to compare.
            similarity_threshold (float): The threshold for considering messages as similar.

        Returns:
            bool: True if the ChainMaps are similar, False otherwise.
        """
        # Check if the ChainMaps have the same author
        if chain_map.message.author.id == other_chain_map.message.author.id:
            # Check if the ChainMaps have the same parent
            if chain_map.parent == other_chain_map.parent:
                # Check if the ChainMaps have the same message
                if chain_map.message.content == other_chain_map.message.content:
                    return True

                # Check if the ChainMaps have similar messages
                similarity_score = calculate_similarity(
                    chain_map.message.embedding, other_chain_map.message.embedding
                )
                if similarity_score >= similarity_threshold:
                    return True

        return False

    def create_new_chain_map(
        self,
        chain_map: ChainMap,
        similar_messages: List[ChainMap],
        hierarchy: ChainTree,
    ) -> ChainMap:
        """
        Create a new ChainMap based on a ChainMap and a list of similar ChainMaps.

        Args:
            chain_map (ChainMap): The ChainMap to create a new ChainMap from.
            similar_messages (List[ChainMap]): A list of similar ChainMaps.
            hierarchy (ChainTree): The hierarchy to create the new ChainMap in.

        Returns:
            ChainMap: The new ChainMap.
        """
        # Create a new ChainMap
        new_chain_map = ChainMap(
            id=str(uuid.uuid4()),
            message=chain_map.message,
            parent=chain_map.parent,
            children=[],
            references=[],
            relationships={},
        )

        # Add the new ChainMap to the hierarchy
        hierarchy.mapping[new_chain_map.id] = new_chain_map

        # Add the new ChainMap to the parent's children
        if new_chain_map.parent:
            hierarchy.mapping[new_chain_map.parent].children.append(new_chain_map.id)

        # Add the new ChainMap to the similar messages' references
        for similar_message in similar_messages:
            similar_message.references.append(new_chain_map.id)

        return new_chain_map

    def build_assistant_hierarchy(
        self, merged_hierarchy: ChainTree, similarity_threshold: float = 0.8
    ) -> ChainTree:
        """
        Build another layer of hierarchy based on assistant messages' similarity.

        Args:
            merged_hierarchy (ChainTree): The merged hierarchy.
            similarity_threshold (float): The threshold for considering messages as similar.

        Returns:
            ChainTree: A new hierarchy with additional layers based on assistant messages.
        """
        new_hierarchy = ChainTree(
            title="Assistant Hierarchy",
            create_time=time.time(),
            update_time=time.time(),
            mapping={},
            current_node=None,
        )

        # Iterate through the ChainMaps in the merged hierarchy
        for chain_map in merged_hierarchy.mapping.values():
            # If the ChainMap belongs to an assistant message
            if chain_map.message.author.role == "assistant":
                # Find similar assistant messages within the new hierarchy
                similar_messages = []
                for existing_chain_map in new_hierarchy.mapping.values():
                    if existing_chain_map.message.author.role == "assistant":
                        similarity_score = calculate_similarity(
                            chain_map.message.embedding,
                            existing_chain_map.message.embedding,
                        )
                        if similarity_score >= similarity_threshold:
                            similar_messages.append(existing_chain_map)

                # If similar assistant messages exist, create a new ChainMap and add them as children
                if similar_messages:
                    new_chain_map = ChainMap(
                        id=str(uuid.uuid4()),
                        message=chain_map.message,
                        parent=None,
                        children=[similar_map.id for similar_map in similar_messages],
                        references=[],
                        relationships={},
                    )
                    new_hierarchy.mapping[new_chain_map.id] = new_chain_map

                    # Update parent and relationship information for similar assistant messages
                    for similar_map in similar_messages:
                        similar_map.parent = new_chain_map.id
                        similar_map.relationships[
                            NodeRelationship.PARENT
                        ] = new_chain_map.id

                # If no similar assistant messages exist, create a new ChainMap with no children
                else:
                    new_chain_map = ChainMap(
                        id=str(uuid.uuid4()),
                        message=chain_map.message,
                        parent=None,
                        children=[],
                        references=[],
                        relationships={},
                    )
                    new_hierarchy.mapping[new_chain_map.id] = new_chain_map

        # Set the current node to the first ChainMap in the new hierarchy
        new_hierarchy.current_node = list(new_hierarchy.mapping.keys())[0]

        return new_hierarchy

    def combined_hierarchy(self, conversations: List[List[ChainTree]]) -> ChainTree:
        """
        Merge a list of hierarchies into a single hierarchy.

        Args:
            conversations (List[List[ChainTree]]): A list of hierarchies.

        Returns:
            ChainTree: A single merged hierarchy.
        """
        # Create a new ChainTree
        merged_hierarchy = ChainTree(
            title="Merged Hierarchy",
            create_time=time.time(),
            update_time=time.time(),
            mapping={},
            current_node=None,
        )

        # Keep track of unique ChainMap IDs in the merged hierarchy
        merged_chain_map_ids = set()

        # Iterate through each hierarchy
        for conversation in conversations:
            # Iterate through each ChainMap in the hierarchy
            for chain_map in conversation.mapping.values():
                # Exclude the system message role
                if chain_map.message.author.role != "system":
                    # Add the ChainMap to the merged hierarchy if its ID is not already present
                    if chain_map.id not in merged_chain_map_ids:
                        merged_hierarchy.mapping[chain_map.id] = chain_map
                        merged_chain_map_ids.add(chain_map.id)

        # Set the current node to the first ChainMap in the merged hierarchy
        if merged_chain_map_ids:
            merged_hierarchy.current_node = list(merged_chain_map_ids)[0]

        return merged_hierarchy

    def process(
        self,
        min_length: Optional[int] = 6,
        prefix: Optional[str] = "Challange Accepted!",
        include_more: bool = False,
        element_type: ElementType = ElementType.STEP,
        separate_columns: bool = True,
        compute_embeddings: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Load all prompts, filter steps based on prefix,
        process the steps into a DataFrame, compute embeddings, and return the resulting DataFrame.

        Args:
            min_length (Optional[int], optional): Minimum length of the steps to consider. Defaults to None.
            prefix (Optional[str], optional): Prefix to filter steps. Defaults to None.
            include_more (bool, optional): Whether to include steps that contain more than just the prefix.
                Defaults to False.
            element_type (ElementType, optional): The type of elements to process (STEP, CHAPTER, or PAGE).
                Defaults to ElementType.STEP.
            separate_columns (bool, optional): Whether to separate the columns (Prefix and Steps) during the embedding process.
                Defaults to True.
            compute_embeddings (bool, optional): Whether to compute embeddings. Defaults to True.

        Returns:
            List[Dict[str, Any]]: The list of ChainTree dicts.
        """
        # Load all prompts and filter steps based on prefix
        example_list = self.load_data_prompts(min_length, prefix, include_more)

        # Prepare initial data as a DataFrame
        df = self.prepare_initial_data(example_list, element_type=element_type)

        # Compute embeddings and save
        if compute_embeddings:
            df = self.compute_embeddings(df, element_type, separate_columns)
            self.save_dataframe(df, "prompt_response_768")
        else:
            df = self.create_prompt_response_dataframe(df, element_type)
            global_embedding = self.semantic_model.encode_texts_openai_batches(
                df["response"].tolist()
            )
            df["embeddings"] = global_embedding
            self.save_dataframe(df, "prompt_response_1536")

        # Convert the DataFrame to a list of ChainTree dicts
        return df.to_dict(orient="records")

    def save_dataframe(self, df: pd.DataFrame, name: str):
        df = df.reset_index(drop=True)
        df.to_json(f"{name}.json", orient="records", indent=4)
        df.to_csv(f"{name}.csv")
        df.to_json(f"{name}.jsonl", orient="records", lines=True)

    def create_prompt_response_dataframe(
        self, df: pd.DataFrame, element_type: ElementType
    ) -> pd.DataFrame:
        """
        Create a new dataframe with prompt and response columns where the prefix is removed and step 1 is the prompt and the remaining steps are cobined the response

        Args:
            df (pd.DataFrame): The DataFrame containing the steps.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).

        Returns:
            pd.DataFrame: The DataFrame with added columns for prompt and response.
        """
        try:
            # Create a new dataframe with prompt and response columns where the prefix is removed and step 1 is the prompt and the remaining steps are cobined the response
            prompt_response_df = pd.DataFrame()
            prompt_response_df["prompt"] = df[element_type.value + " 0"]
            prompt_response_df["response"] = df.iloc[:, 2:].apply(
                lambda x: " ".join(x.dropna().astype(str)), axis=1
            )

            # reset index
            prompt_response_df.reset_index(drop=True, inplace=True)

            return prompt_response_df

        except Exception as e:
            print(f"Error creating prompt and response dataframe: {e}")
            return pd.DataFrame()

    def convert_to_long_format(
        self, df: pd.DataFrame, element_type: ElementType, format_type: str = "linear"
    ) -> pd.DataFrame:
        """
        Convert the DataFrame to "long" format where each row corresponds to a single step and its associated embedding.

        Args:
            df (pd.DataFrame): The DataFrame containing the elements and their embeddings.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).
            format_type (str): The format type, either 'incremental' or 'linear'.

        Returns:
            pd.DataFrame: The DataFrame in "long" format.
        """
        long_format_data = []
        num_elements = df.columns.str.startswith(element_type.value).sum()

        # Dictionary to store element_id based on the element value
        element_id_dict = {}

        for idx, row in df.iterrows():
            prefix_text = row["Prefix"]
            # Get or create the element_id for the current element value
            element_id = element_id_dict.get(prefix_text)
            if element_id is None:
                element_id = str(uuid.uuid4())
                element_id_dict[prefix_text] = element_id

            for i in range(num_elements):
                element_col = f"{element_type.value} {i}"
                element_embed_col = f"{element_type.value} {i} embedding"
                if element_col in df.columns and element_embed_col in df.columns:
                    element_text = row[element_col]
                    embedding = row[element_embed_col]
                    if element_text:
                        if format_type == "incremental":
                            long_format_data.append(
                                {
                                    "id": str(uuid.uuid4()),  # Unique uuid for each row
                                    "element_id": element_id,  # Assigning the element_id
                                    "Element Type": element_type.value,
                                    "Element Index": i,  # Incremental element index starting from 0
                                    "Element Text": element_text,
                                    "Embedding": embedding,
                                }
                            )
                        elif format_type == "linear":
                            long_format_data.append(
                                {
                                    "id": str(uuid.uuid4()),  # Unique uuid for each row
                                    "Prefix": row[f"{element_type.value} 0"],
                                    "Element": i,
                                    "Element Text": element_text,
                                    "Embedding": embedding,
                                }
                            )

        # Create the final DataFrame in "long" format
        long_df = pd.DataFrame(long_format_data)

        return long_df

    def group_similar_terms_from_dict(
        self, embedding_dict: Dict[str, np.ndarray], similarity_threshold: float = 0.9
    ) -> List[str]:
        """
        Group similar terms based on their embeddings.
        Return the resulting list of grouped terms.

        Args:
            embedding_dict (Dict[str, np.ndarray]): The dictionary containing the terms and their embeddings.
            similarity_threshold (float, optional): The similarity threshold for grouping similar terms.
                Defaults to 0.9.

        Returns:
            List[str]: The list of grouped terms.
        """
        try:
            # Group similar terms based on their embeddings
            grouped_terms = []
            for term in embedding_dict.keys():
                if term not in grouped_terms:
                    grouped_terms.append(term)
                    for other_term in embedding_dict.keys():
                        if (
                            other_term not in grouped_terms
                            and calculate_similarity(
                                embedding_dict[term], embedding_dict[other_term]
                            )
                            >= similarity_threshold
                        ):
                            grouped_terms.append(other_term)

            return grouped_terms

        except Exception as e:
            print(f"Error grouping similar terms: {e}")
            return []

    def group_similar_terms(
        self,
        df: pd.DataFrame,
        element_type: ElementType,
        embedding_column: str,
        similarity_threshold: float = 0.9,
    ) -> pd.DataFrame:
        """
        Group similar terms in the DataFrame based on their embeddings.
        Return the resulting DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the elements and their embeddings.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).
            embedding_column (str): The name of the column containing the embeddings.
            similarity_threshold (float, optional): The similarity threshold for grouping similar terms.
                Defaults to 0.9.

        Returns:
            pd.DataFrame: The DataFrame with grouped similar terms.
        """
        try:
            # Group similar terms based on their embeddings
            df_copy = (
                df.copy()
            )  # Create a copy of the DataFrame to avoid potential warnings
            embedding_dict = dict(
                zip(df_copy[element_type.value], df_copy[embedding_column])
            )
            grouped_terms = self.group_similar_terms_from_dict(
                embedding_dict, similarity_threshold
            )

            # Add the grouped terms to the DataFrame
            df_copy[element_type.value] = grouped_terms

            return df_copy

        except Exception as e:
            print(f"Error grouping similar terms: {e}")
            return pd.DataFrame()

    def get_top_n_similar_terms(
        self,
        df: pd.DataFrame,
        element_type: ElementType,
        embedding_column: str,
        term: str,
        n: int = 5,
    ) -> pd.DataFrame:
        """
        Get the top n similar terms for a given term based on their embeddings.
        Return the resulting DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the elements and their embeddings.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).
            embedding_column (str): The name of the column containing the embeddings.
            term (str): The term for which to find similar terms.
            n (int, optional): The number of similar terms to return. Defaults to 5.

        Returns:
            pd.DataFrame: The DataFrame with the top n similar terms.
        """
        try:
            # Get the embeddings for the given term
            term_embeddings = df[df[element_type.value] == term][embedding_column]

            # Calculate the similarity between the term and all other terms
            df_copy = (
                df.copy()
            )  # Create a copy of the DataFrame to avoid potential warnings
            df_copy["Similarity"] = df_copy[embedding_column].apply(
                lambda x: calculate_similarity(term_embeddings, x)
            )

            # Sort the DataFrame by similarity and return the top n similar terms
            return df_copy.sort_values(by="Similarity", ascending=False).head(n)

        except Exception as e:
            print(f"Error getting top n similar terms: {e}")
            return pd.DataFrame()

    def get_term_frequencies_from_string(self, text: str) -> Dict[str, int]:
        """
        Get the term frequencies for the given text.
        Return the resulting dictionary.

        Args:
            text (str): The text to get the term frequencies for.

        Returns:
            Dict[str, int]: The dictionary containing the term frequencies.
        """
        try:
            # Get the term frequencies for the given text
            term_frequencies = {}
            for term in text.split():
                if term in term_frequencies.keys():
                    term_frequencies[term] += 1
                else:
                    term_frequencies[term] = 1

            return term_frequencies

        except Exception as e:
            print(f"Error getting term frequencies: {e}")
            return {}

    def get_embeddings_separate_columns(
        self,
        df: pd.DataFrame,
        element_type: ElementType = ElementType.STEP,
    ) -> pd.DataFrame:
        """
        Add the embeddings for each step in a separate column.
        Return the resulting DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the steps.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).

        Returns:
            pd.DataFrame: The DataFrame with the embeddings for each step in a separate column.
        """
        try:
            # Add the embeddings for each step in a separate column
            for i in range(self.embedding_size):
                df[f"{element_type.value}_{i}"] = df[element_type.value].apply(
                    lambda x: x[i] if len(x) > i else 0
                )

            return df

        except Exception as e:
            print(f"Error getting embeddings for each step in a separate column: {e}")
            return pd.DataFrame()

    def get_embeddings(
        self,
        df: pd.DataFrame,
        element_type: ElementType = ElementType.STEP,
        grouped_terms: Optional[Dict[str, str]] = None,
    ) -> Dict[str, np.ndarray]:
        """
        Get the embeddings for each element in the DataFrame.
        Return the resulting dictionary.

        Args:
            df (pd.DataFrame): The DataFrame containing the elements.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).
            grouped_terms (Optional[Dict[str, str]], optional): The dictionary containing the grouped terms. Defaults to None.

        Returns:
            Dict[str, np.ndarray]: The dictionary containing the embeddings.
        """
        try:
            # Get the embeddings for each element
            embedding_dict = {}
            for index, row in df.iterrows():
                embedding_dict[row[element_type.value]] = self.get_embedding(
                    row[element_type.value], grouped_terms
                )

            return embedding_dict

        except Exception as e:
            print(f"Error getting embeddings: {e}")
            return {}

    def get_embedding(
        self,
        text: str,
        grouped_terms: Optional[Dict[str, str]] = None,
    ) -> np.ndarray:
        """
        Get the embedding for the given text.
        Return the resulting array.

        Args:
            text (str): The text to get the embedding for.
            grouped_terms (Optional[Dict[str, str]], optional): The dictionary containing the grouped terms. Defaults to None.

        Returns:
            np.ndarray: The array containing the embedding.
        """
        try:
            # Get the embedding for the given text
            embedding = np.zeros(self.embedding_size)
            term_frequencies = self.get_term_frequencies(text)
            for term, frequency in term_frequencies.items():
                if grouped_terms is not None and term in grouped_terms.keys():
                    term = grouped_terms[term]
                try:
                    embedding += self.model[term] * frequency
                except:
                    pass

            return embedding

        except Exception as e:
            print(f"Error getting embedding: {e}")
            return np.zeros(self.embedding_size)

    def get_term_frequencies(
        self, df: pd.DataFrame, element_type: ElementType
    ) -> pd.DataFrame:
        """
        Get the term frequencies for each element in the DataFrame.
        Return the resulting DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the elements.
            element_type (ElementType): The type of the elements (e.g., ElementType.STEP, ElementType.CHAPTER, ElementType.PAGE).

        Returns:
            pd.DataFrame: The DataFrame with added columns for term frequencies.
        """
        try:
            # Get the term frequencies for each element
            df_copy = (
                df.copy()
            )  # Create a copy of the DataFrame to avoid potential warnings
            df_copy["term frequencies"] = df_copy[element_type.value].apply(
                lambda x: self.get_term_frequencies_from_string(x)
            )

            return df_copy

        except Exception as e:
            print(f"Error getting term frequencies: {e}")
            return pd.DataFrame()
