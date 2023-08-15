from typing import Optional, Dict, Any, List, Tuple
from dl_matrix.models import ChainTreeIndex, ChainTree, ChainMap, Message
from dl_matrix.parsers import ChainTreeParser
from dl_matrix.utils import load_json, save_json
import pandas as pd
from tqdm import tqdm


class ChainTreeBuilder:
    def __init__(
        self,
        path: str = "conversation/v4.json",
        key: Optional[str] = "title",
        prompt_key: Optional[str] = "prompt",
        save_path: Optional[str] = "combined.json",
        prompt_dir: Optional[str] = "prompts",
    ):
        self.path = path
        self.key = key
        self.data = load_json(path)
        self.conversations = ChainTreeParser.parse_chain_tree(self.data)
        self.message_coord_map = {}
        self.save_path = save_path
        self.less_than_target = []
        self.prompt_dir = prompt_dir
        self.prompt_key = prompt_key

    def as_list(self) -> List[ChainTreeIndex]:
        return self.create_conversation_trees()

    def as_dict(self) -> Dict[str, ChainTreeIndex]:
        if not self.key:
            raise ValueError("Key must be provided when building a dictionary.")
        conversation_trees = self.create_conversation_trees()
        return {
            getattr(conversation, self.key): tree
            for conversation, tree in zip(self.conversations, conversation_trees)
        }

    def get(self, index: int) -> ChainTreeIndex:
        return self.create_conversation_trees()[index]

    def __iter__(self):
        return iter(self.create_conversation_trees())

    def __getitem__(self, index: int) -> ChainTreeIndex:
        return self.get(index)

    def __len__(self) -> int:
        return len(self.create_conversation_trees())

    def create_conversation_trees(
        self, target_num: int = 6
    ) -> Tuple[List[ChainTreeIndex], List[ChainTreeIndex]]:
        if target_num < 5:
            raise ValueError("target_num must be greater than or equal to 5.")

        greater_than_target = []
        for i, conversation in enumerate(self.conversations):
            if conversation is not None:
                if len(conversation.mapping) >= target_num:
                    greater_than_target.append(
                        ChainTreeIndex(conversation=conversation)
                    )
                else:
                    # Only update title for conversations that are less than target_num
                    conversation.title = str(i)
                    self.less_than_target.append(
                        ChainTreeIndex(conversation=conversation)
                    )

        return greater_than_target

    def create_message_map(self, trees: Optional[List[ChainTreeIndex]] = None) -> Dict:
        """Generate a message coordinate map from the conversation trees.

        Parameters:
        - trees (Optional[List[ChainTreeIndex]]): List of conversation trees.
        Defaults to the result of self.create_conversation_trees().

        Returns:
        - Dict: Message coordinate map.
        """

        if trees is None:
            trees = self.create_conversation_trees()

        message_coord_map = {}

        for tree in trees:
            for message_id, mapping in tree.conversation.mapping.items():
                if (
                    mapping.message is not None
                    and mapping.message.author.role != "system"
                ):
                    message_coord_map[message_id] = {
                        "message_id": mapping.message.id,
                        "text": mapping.message.content.text,
                        "author": mapping.message.author.role,
                        "create_time": mapping.message.create_time,
                        "title": tree.conversation.title,
                        "metadata": mapping.message.metadata,
                        "embeddings": mapping.message.embedding,
                    }

        return message_coord_map

    def format_dataframe(self, df: pd.DataFrame, exclude_columns: List[str] = None):
        if exclude_columns is not None:
            df = df.drop(columns=exclude_columns)

        df = df.reset_index(drop=True)

        return df

    def create_dataframe(
        self,
        exclude_columns: List[str] = None,
        semantic_similarity_model: object = None,
        use_embeddings: bool = False,
    ) -> pd.DataFrame:
        message_coord_map = self.create_message_map()
        df = pd.DataFrame.from_dict(message_coord_map, orient="index")
        df = self.format_dataframe(df, exclude_columns=exclude_columns)

        if semantic_similarity_model is not None:
            df = semantic_similarity_model.compute_message_embeddings(
                main_df=df,
                semantic_similarity_model=semantic_similarity_model,
                use_embeddings=use_embeddings,
            )
        return df

    def combine_conversations_in_batches(
        self, conversation_trees: List[ChainTreeIndex], batch_size: int = 1000
    ) -> List[ChainTreeIndex]:
        batched_trees = []
        for i in tqdm(
            range(0, len(conversation_trees), batch_size), desc="Processing batches"
        ):
            batch = conversation_trees[i : i + batch_size]
            combined_tree = self.combine_conversations(batch)
            batched_trees.append(combined_tree)
        return batched_trees

    def retrieve_mappings(
        self, conversation_trees: List[ChainTreeIndex]
    ) -> List[ChainMap]:
        print("Retrieving mappings from conversations...")
        mappings = []
        for tree in tqdm(conversation_trees):
            mappings.extend(list(tree.conversation.mapping.values()))
        return mappings

    def update_parent_child(self, mappings: List[ChainMap]) -> Dict[str, str]:
        print("Creating new IDs for mappings...")

        # If mappings is None or empty, return an empty dictionary
        if not mappings:
            return {}

        new_mapping_ids = {}
        parent_child_map = {}

        for mapping in tqdm(mappings):
            if mapping.message is not None:
                # Still retain the message ID mapping, as you did before
                new_mapping_ids[mapping.message.id] = mapping.message.id

                # Check for parent and establish a parent-child relationship
                parent_id = mapping.parent
                if parent_id:
                    # Store children IDs in a list against their parent
                    if parent_id not in parent_child_map:
                        parent_child_map[parent_id] = []
                    parent_child_map[parent_id].append(mapping.message.id)

        # Now, update the children information for each mapping based on the parent_child_map
        for mapping in mappings:
            if mapping.message and mapping.message.id in parent_child_map:
                mapping.children = parent_child_map[mapping.message.id]

        return new_mapping_ids

    def extract_and_sort_messages(
        self, mappings: List[ChainMap], new_mapping_ids: Dict[str, str]
    ) -> List[Message]:
        print("Extracting and sorting messages...")
        sorted_messages = []

        for mapping in tqdm(mappings):
            if mapping.message is not None:
                mapping.message.id = new_mapping_ids[mapping.message.id]
                sorted_messages.append(mapping.message)

        # Sort the messages based on their creation time
        # Messages with None as creation time will be placed at the end
        sorted_messages.sort(key=lambda m: (m.create_time is None, m.create_time))

        return sorted_messages

    def create_linked_list(
        self, sorted_messages: List[Message]
    ) -> Tuple[Dict[str, str], List[Message]]:
        print("Creating linked list...")
        id_mapping = {}
        for i, message in tqdm(enumerate(sorted_messages)):
            # For each message, determine its previous and next based on its position in the sorted list
            message.prev = sorted_messages[i - 1].id if i > 0 else None
            message.next = (
                sorted_messages[i + 1].id if i < len(sorted_messages) - 1 else None
            )
            id_mapping[message.id] = message.id
        return sorted_messages

    def update_mappings(
        self, sorted_messages: List[Message], conversation_trees: List[ChainTreeIndex]
    ) -> List[ChainMap]:
        print("Updating mappings...")
        combined_mappings = []

        # Create a message_id to ChainMap dictionary for quick look-up
        existing_mappings = {
            mapping.message.id: mapping
            for tree in conversation_trees
            for mapping in tree.conversation.mapping.values()
            if mapping.message is not None
        }

        # Initialize previous message variable
        prev_message = None

        for message in tqdm(sorted_messages):
            if message.id in existing_mappings:
                mapping = existing_mappings[message.id]
                mapping.message = message
            else:
                mapping = ChainMap(id=message.id, message=message)

            # Check if message is by system
            if message.author.role == "system":
                # If message is by system, check if it is a prompt
                related_conversation = None
                for index, conv in enumerate(conversation_trees):
                    if conv.conversation.mapping.get(message.id):
                        related_conversation = conv
                        break

                if related_conversation:
                    # If message is a prompt, update the message content
                    message.content.text = f"Conversation {index + 1}: {related_conversation.conversation.title}"
                    message.content.parts = [message.content.text]
                    message.create_time = related_conversation.conversation.create_time

                if prev_message:
                    mapping.parent = prev_message.id
                    prev_mapping = existing_mappings.get(
                        prev_message.id,
                        ChainMap(id=prev_message.id, message=prev_message),
                    )
                    if prev_mapping.children:
                        prev_mapping.children.append(message.id)
                    else:
                        prev_mapping.children = [message.id]

            combined_mappings.append(mapping)
            prev_message = message

        return combined_mappings

    def combine_conversations(
        self, filtered_trees: List[ChainTreeIndex]
    ) -> ChainTreeIndex:
        try:
            mappings = self.retrieve_mappings(filtered_trees)
            new_mapping_ids = self.update_parent_child(mappings)
            sorted_messages = self.extract_and_sort_messages(mappings, new_mapping_ids)
            sorted_messages = self.create_linked_list(sorted_messages)
            combined_mappings = self.update_mappings(sorted_messages, filtered_trees)
            print("Creating combined conversation...")
            # convert the combined mappings to a dictionary
            combined_mappings = {mapping.id: mapping for mapping in combined_mappings}
            # sort the combined mappings by create_time
            combined_mappings = dict(
                sorted(
                    combined_mappings.items(),
                    key=lambda item: item[1].message.create_time,
                )
            )

            combined_conversation = ChainTree(
                title="Combined Conversation",
                create_time=sorted_messages[0].create_time,
                update_time=sorted_messages[-1].create_time,
                mapping=combined_mappings,
                moderation_results=[],
                current_node="",
            )
            # convert the combined tree to a dictionary
            combined_tree = combined_conversation.dict()
            # convert the combined tree to a ChainTreeIndex object
            combined_tree = ChainTreeIndex(conversation=combined_conversation)

            return combined_tree

        except Exception as e:
            print(e)
            return None

    def save_conversations(self, conversation_trees: List[ChainTreeIndex], path: str):
        save_json(path, [conversation_trees])


def get_message_map(path: str = "conversation/conversations.json") -> Dict[str, Any]:
    conversation_trees = ChainTreeBuilder(path)
    return conversation_trees.create_message_map()


def get_chain_trees_list(
    path: str = "conversation/v4.json",
) -> List[ChainTreeIndex]:
    conversation_trees = ChainTreeBuilder(path)
    return conversation_trees.as_list()


def get_chain_trees_dict(
    path: str = "conversation/conversations.json",
    key: str = "title",
) -> Dict[str, ChainTreeIndex]:
    conversation_trees = ChainTreeBuilder(path, key)
    return conversation_trees.as_dict()


def get_chain_tree(
    path: str = "conversation/conversations.json",
    index: int = 5,
    key: str = "title",
) -> ChainTreeIndex:
    conversation_trees = ChainTreeBuilder(path, key)
    return conversation_trees.get(index)


def combined_json_conversation(
    path1: str,
    path2: str,
    output_path: str,
) -> ChainTreeIndex:
    conversation_trees = ChainTreeBuilder(path1)
    return conversation_trees.combine_json_files(path1, path2, output_path)


def get_combined_conversations(
    path: str = "conversation/conversations.json",
    batch_size: int = 1000,
) -> List[ChainTreeIndex]:
    conversation_trees = ChainTreeBuilder(path)
    return conversation_trees.combine_conversations_in_batches(
        conversation_trees.as_list(), batch_size
    )


def get_dataframe(
    path: str = "conversation/conversations.json",
    exclude_columns: List[str] = None,
    semantic_similarity_model: object = None,
    use_embeddings: bool = False,
) -> pd.DataFrame:
    conversation_trees = ChainTreeBuilder(path)
    return conversation_trees.create_dataframe(
        exclude_columns=exclude_columns,
        semantic_similarity_model=semantic_similarity_model,
        use_embeddings=use_embeddings,
    )
