from typing import List, Dict, Optional, Union
from .synthesis import SynthesisTechniqueManager
from .builder import ReplyChainBuilder
from .technique import SynthesisTechniqueDirector
from .director import ReplyChainDirector


class ReplyChainSystem:
    def __init__(self):
        self.reply_chain_builder = ReplyChainBuilder()

        self.technique_manager = SynthesisTechniqueManager()
        self.name = self.technique_manager.get_random_synthesis_technique_name()

        self.tech_director = SynthesisTechniqueDirector(
            technique_name=self.name,
            builder=self.reply_chain_builder,
            technique_manager=self.technique_manager,
        )

        self.director = ReplyChainDirector(
            technique_director=self.tech_director,
        )

    def construct_reply_chain(self, prompt, response: Optional[str] = None):
        """
        Construct the reply chain with given prompt and response.
        """

        if not isinstance(prompt, str):
            raise ValueError("Prompt must be a string.")
        if response is not None and not isinstance(response, str):
            raise ValueError("Response must be a string.")

        self.director.construct(prompt, response)
        self.chain_tree = self.reply_chain_builder.get_result()

    def _validate_conversation_data(self, data: List[Dict[str, Union[str, None]]]):
        """
        Validate conversation data.
        """
        if not isinstance(data, list):
            raise ValueError("Conversation data must be a list of dictionaries.")

        if not data:
            raise ValueError("Conversation data must not be empty.")

        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Each conversation item must be a dictionary.")
            if "prompt" not in item or not isinstance(item["prompt"], str):
                raise ValueError("The 'prompt' key must exist and be a string.")
            if "response" in item and not (
                isinstance(item["response"], str) or item["response"] is None
            ):
                raise ValueError("The 'response' key must be either a string or None.")

    def process_conversations(self, data: List[Dict[str, str]]):
        """
        Process a list of conversation data.
        """
        self._validate_conversation_data(data)

        for item in data:
            print(f"Constructing reply chain...")
            self.director.construct(item["prompt"], item["response"])

        self.chain_tree = self.reply_chain_builder.get_result()
        print("Reply chains constructed.")

    def add_nodes_from_chains(self, chains=None):
        """
        Add nodes from chains to the chain tree.
        """
        if chains is None:
            chains = self.get_chains()
        for chain in chains:
            if chain.content and chain.content.text:
                node_id = str(len(self.chain_tree.nodes) + 1)
                raw = chain.content.text
                self.chain_tree.add_node(raw, node_id)

    def _truncate_conversation_history(
        self,
        chains: List[str],
        max_history_length: Optional[int] = None,
        prioritize_recent: bool = True,
    ):
        if not isinstance(chains, list):
            raise ValueError("Conversation history must be a list of chains.")

        if not chains:
            raise ValueError("Conversation history must not be empty.")

        if max_history_length is not None:
            total_length = sum(len(chain.content.text) for chain in chains)
            while total_length > max_history_length:
                if prioritize_recent:
                    removed_chain = chains.pop(0)
                else:
                    removed_chain = chains.pop()
                total_length -= len(removed_chain.content.text)

        return chains

    def prepare_conversation_history(
        self,
        prompt: str,
        response: Optional[str] = None,
        use_process_conversations: bool = False,
        custom_conversation_data: Optional[List[Dict[str, str]]] = None,
        max_history_length: Optional[int] = None,
        prioritize_recent: bool = True,
    ):
        if max_history_length is not None:
            if not isinstance(max_history_length, int) or max_history_length < 1:
                raise ValueError("max_history_length must be a positive integer.")

        if custom_conversation_data is not None:
            if not isinstance(custom_conversation_data, list) or not all(
                isinstance(item, dict) for item in custom_conversation_data
            ):
                raise ValueError(
                    "custom_conversation_data should be a list of dictionaries with 'prompt' and 'response' keys."
                )

            if use_process_conversations:
                self.process_conversations(custom_conversation_data)
            else:
                for conversation_item in custom_conversation_data:
                    if "prompt" not in conversation_item or (
                        response is not None and "response" not in conversation_item
                    ):
                        raise ValueError(
                            "Each dictionary in custom_conversation_data should have 'prompt' and 'response' keys."
                        )
                    self.construct_reply_chain(
                        prompt=conversation_item["prompt"],
                        response=conversation_item.get("response"),
                    )

        else:
            if response:
                if use_process_conversations:
                    conversation_data = [{"prompt": prompt, "response": response}]
                    self.process_conversations(conversation_data)
                else:
                    self.construct_reply_chain(prompt=prompt, response=response)
            else:
                self.construct_reply_chain(prompt=prompt)

        self.add_nodes_from_chains()

        conversation_history = self._truncate_conversation_history(
            self.get_chains(),
            max_history_length=max_history_length,
            prioritize_recent=prioritize_recent,
        )

        return conversation_history

    def get_chains(self):
        """
        Get chains from the chain tree.
        """
        return self.chain_tree.get_chains()
