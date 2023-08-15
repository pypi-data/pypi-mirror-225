import re
import time
from typing import Optional, Callable, List, Dict, Tuple, Union, Any
from dl_matrix.utils import (
    log_handler,
    setup_logging,
    APIFailureException,
)
from dl_matrix.infrence.openai import ChatOpenAI
from dl_matrix.infrence.utility import DataEngine
from dl_matrix.infrence.manager import ConversationManager
from dl_matrix.infrence.session import PromptSessionWrapper
from dl_matrix.infrence.callbacks.streaming import StreamingHandler
from dl_matrix.chaintrees import ReplyChainSystem


class PromptGenerator:
    def __init__(self, openai_api_key: str, path_to_dataset: Optional[str] = None):
        self.conversation_manager = ConversationManager()
        self.retries: int = 1
        self.chat = ChatOpenAI(
            callbacks=[StreamingHandler()], openai_api_key=openai_api_key
        )
        self.reply_chain_system = ReplyChainSystem()
        self.data_engine = DataEngine(path_to_dataset)
        self.prompt_session = PromptSessionWrapper()

        setup_logging()

    def create_conversation(self) -> str:
        return self.conversation_manager.create_conversation()

    def select_best_message(
        self,
        generated_messages: List[str],
        custom_ranking_fn: Optional[Callable[[List[str]], str]],
    ):
        return (
            custom_ranking_fn(generated_messages)
            if custom_ranking_fn
            else generated_messages.content
        )

    def split_message(
        self,
        best_generated_message: Union[str, Any],  # Allow other types here as well
        message_split_pattern: Optional[str] = r"\n\n",
    ) -> List[str]:
        split_pattern = re.compile(message_split_pattern)

        # Convert to string if it's not a string or bytes-like object
        if not isinstance(best_generated_message, str):
            best_generated_message = str(best_generated_message)

        return split_pattern.split(best_generated_message)

    def split_text(self, text: str) -> Tuple[str, str]:
        # First, split by ":"
        split_by_colon = text.split(":") if ":" in text else [None, None]

        # Get the epithet text
        epithet_text = (
            split_by_colon[0].strip() if split_by_colon[0] is not None else None
        )

        # Now, split second part by "*"
        split_by_asterisk = (
            split_by_colon[1].split("*") if len(split_by_colon) > 1 else [None, None]
        )

        # Get the highlighted text
        highlighted_text = (
            split_by_asterisk[1].strip() if len(split_by_asterisk) > 1 else None
        )

        return epithet_text, highlighted_text

    def generate_prompt_parts(
        self,
        conversation_id: str,
        prompt: str,
        response: Optional[str] = None,
        use_process_conversations: bool = False,
        custom_conversation_data: Optional[List[Dict[str, str]]] = None,
        max_history_length: Optional[int] = None,
        prioritize_recent: bool = True,
        custom_ranking_fn: Optional[Callable[[List[str]], str]] = None,
        message_split_pattern: Optional[str] = r"\n\n",
    ) -> List[str]:
        conversation_history = self.reply_chain_system.prepare_conversation_history(
            prompt,
            response,
            use_process_conversations,
            custom_conversation_data,
            max_history_length,
            prioritize_recent,
        )

        truncated_history = self.chat._truncate_conversation_history(
            conversation_history
        )

        generated_messages = self.generate_messages(conversation_id, truncated_history)

        best_generated_message = self.select_best_message(
            generated_messages, custom_ranking_fn
        )

        new_res = self.split_message(best_generated_message, message_split_pattern)
        if not new_res:
            log_handler("Empty response", level="error")
            raise APIFailureException("Empty response")

        return new_res

    def generate_prompt_task(
        self,
        prompt: str,
        response: Optional[str] = None,
        use_process_conversations: bool = False,
        custom_conversation_data: Optional[List[Dict[str, str]]] = None,
    ) -> List[str]:
        retry = 0
        while retry < self.chat.max_retries:
            try:
                conversation_id = self.create_conversation()
                prompt_parts = self.generate_prompt_parts(
                    conversation_id=conversation_id,
                    prompt=prompt,
                    response=response,
                    use_process_conversations=use_process_conversations,
                    custom_conversation_data=custom_conversation_data,
                )

                return prompt_parts
            except APIFailureException as e:
                log_handler(e, level="error")
                retry += 1
                log_handler(
                    f"Retrying prompt generation. Retry {retry}/{self.chat.max_retries}",
                    level="warning",
                )
                continue

        log_handler(
            f"Failed to generate prompt after {self.chat.max_retries} retries.",
            level="error",
        )

        return prompt_parts

    def generate_messages(
        self,
        conversation_id: str,
        truncated_history: List[str],
        parent: Optional[str] = None,
    ):
        generated_messages = self.chat(truncated_history)
        self.conversation_manager.add_message(
            conversation_id,
            message_id=generated_messages.id,
            content=generated_messages.content,
            author=generated_messages.author,
            parent=parent,
        )
        return generated_messages

    def save_conversation(self, conversation_id: str, title: str = "Untitled"):
        """Save the current conversation to json file"""
        conversation = self.conversation_manager.get_conversation(conversation_id)
        conversation.save_conversation(title)

    def handle_command(self, command: str, conversation_id: str):
        if command.startswith("/save"):
            parts = command.split(maxsplit=1)  # Split the command into at most 2 parts
            if len(parts) > 1:
                title = parts[1]  # The second part is our title
                try:
                    self.save_conversation(conversation_id, title)
                    return "Conversation saved successfully with title: " + title
                except Exception as e:
                    return f"Error saving conversation: {e}"
            else:
                return "Please provide a title. Use /save <title>."

        commands = {
            "/help": "Type your message to continue the conversation. Use '/quit' to exit, '/restart' to restart the conversation, '/history' to view past messages.",
            "/restart": "Restarting the conversation...",
            "/history": "\n".join(
                self.conversation_manager.get_conversation(
                    conversation_id
                ).get_messages()
            ),
        }
        return commands.get(
            command, "Unknown command. Type '/help' for a list of commands."
        )

    def run_prompt(self, initial_prompt: str = "", request_feedback: bool = False):
        conversation_id = self.conversation_manager.start_conversation(initial_prompt)
        agent_response = None  # Initially, there's no agent response

        while True:
            prompt_message = "You: "
            user_input = self.prompt_session.get_input(prompt_message)
            print("\n")  # Ensure there's a new line after user input

            # Command Handling
            if user_input.startswith("/"):
                response = self.handle_command(
                    user_input.strip().lower(), conversation_id
                )
                print(response)
                print("\n")  # New line after the command's response

                if user_input.strip().lower() == "/restart":
                    self.conversation_manager.end_conversation(conversation_id)
                    conversation_id = self.conversation_manager.start_conversation()
                    agent_response = None  # Reset the agent response when restarting
                continue  # Skip the rest and restart the loop

            # Quit Handling
            if user_input.strip().lower() == "quit":
                print("Thank you for using the system. Goodbye!\n")
                break

            use_process_conversations_flag = True if not agent_response else False

            try:
                last_message_id = self.conversation_manager.get_conversation(
                    conversation_id
                ).get_last_message_id()

                prompt_parts = self.generate_prompt_task(
                    prompt=user_input,
                    response=agent_response,  # Using the agent's response from the previous iteration
                    use_process_conversations=use_process_conversations_flag,
                    custom_conversation_data=None,
                )
                agent_prompt = prompt_parts[0]
                agent_response = (
                    agent_prompt  # Update the agent's response for the next iteration
                )

                self.conversation_manager.handle_user_input(
                    conversation_id, user_input, last_message_id
                )
                print("\n")  # New line after handling user input

                self.conversation_manager.handle_agent_response(
                    conversation_id, agent_prompt, last_message_id
                )
                print("\n")  # New line after handling agent response

                if request_feedback:
                    feedback_prompt = self.get_feedback(agent_prompt, user_input)
                    self.conversation_manager.handle_user_input(
                        conversation_id, feedback_prompt, last_message_id
                    )
                    print("\n")  # New line after handling feedback

                time.sleep(0.5)
            except Exception as e:
                print(
                    f"An error occurred: {e}. Please try again.\n"
                )  # New line after error message

        self.conversation_manager.end_conversation(conversation_id)

    def get_feedback(self, agent_response: str, user_prompt: str):
        feedback_prompt = self.generate_prompt_task(
            prompt=user_prompt,
            response=agent_response,
            use_process_conversations=False,
            custom_conversation_data=None,
        )[0]

        feedback = self.prompt_session.get_input(feedback_prompt)
        print()  # New line after feedback inpu

        return feedback
