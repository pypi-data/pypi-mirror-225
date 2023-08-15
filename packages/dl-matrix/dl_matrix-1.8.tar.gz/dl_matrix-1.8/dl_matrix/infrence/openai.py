"""OpenAI chat wrapper."""
from __future__ import annotations
import random
import logging
import sys
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Union
from dl_matrix.utils import log_handler
from pydantic import Extra, Field, root_validator
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
import os
from dl_matrix.infrence.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from dl_matrix.infrence.base import BaseChatModel
from dl_matrix.base import (
    _convert_dict_to_message,
    Chain,
    ChatGeneration,
    ChatResult,
)

import numpy as np
import openai

from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


def _create_retry_decorator(llm: ChatOpenAI) -> Callable[[Any], Any]:
    import openai

    min_seconds = 1
    max_seconds = 60
    # Wait 2^x * 1 second between each retry starting with
    # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
    return retry(
        reraise=True,
        stop=stop_after_attempt(llm.max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(
            retry_if_exception_type(openai.error.Timeout)
            | retry_if_exception_type(openai.error.APIError)
            | retry_if_exception_type(openai.error.APIConnectionError)
            | retry_if_exception_type(openai.error.RateLimitError)
            | retry_if_exception_type(openai.error.ServiceUnavailableError)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )


def _convert_message_to_dict(message: Dict[str, Any]) -> dict:
    if "role" in message and "content" in message:
        message_dict = {"role": message["role"], "content": message["content"]}
    else:
        raise ValueError(f"Got unknown type {message}")

    if "name" in message:
        message_dict["name"] = message["name"]
    return message_dict


class ChatOpenAI(BaseChatModel):
    """Wrapper around OpenAI Chat large language models.

    To use, you should have the ``openai`` python package installed, and the
    environment variable ``OPENAI_API_KEY`` set with your API key.

    Any parameters that are valid to be passed to the openai.create call can be passed
    in, even if not explicitly saved on this class.

    Example:
        .. code-block:: python

            from langchain.chat_models import ChatOpenAI
            openai = ChatOpenAI(model_name="gpt-3.5-turbo")
    """

    client: Any  #: :meta private:
    model_name: str = "gpt-3.5-turbo"
    """Model name to use."""
    temperature: float = 1
    """What sampling temperature to use."""
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Holds any model parameters valid for `create` call not explicitly specified."""
    openai_api_key: Optional[str] = None

    openai_organization: Optional[str] = None

    request_timeout: Optional[Union[float, Tuple[float, float]]] = None
    """Timeout for requests to OpenAI completion API. Default is 600 seconds."""
    max_retries: int = 2
    """Maximum number of retries to make when generating."""
    streaming: bool = True
    """Whether to stream the results or not."""
    n: int = 1
    """Number of chat completions to generate for each prompt."""
    max_tokens: Optional[int] = 2000
    """Maximum number of tokens to generate."""

    frequency_penalty: Optional[float] = 1

    presence_penalty: Optional[float] = 1

    keywords: Optional[List[str]] = None

    _semantic_vectors: Optional[List[List[float]]] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.ignore

    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Build extra kwargs from additional params that were passed in."""
        all_required_field_names = {field.alias for field in cls.__fields__.values()}

        extra = values.get("model_kwargs", {})
        for field_name in list(values):
            if field_name in extra:
                raise ValueError(f"Found {field_name} supplied twice.")
            if field_name not in all_required_field_names:
                logger.warning(
                    f"""WARNING! {field_name} is not default parameter.
                    {field_name} was transferred to model_kwargs.
                    Please confirm that {field_name} is what you intended."""
                )
                extra[field_name] = values.pop(field_name)

        disallowed_model_kwargs = all_required_field_names | {"model"}
        invalid_model_kwargs = disallowed_model_kwargs.intersection(extra.keys())
        if invalid_model_kwargs:
            raise ValueError(
                f"Parameters {invalid_model_kwargs} should be specified explicitly. "
                f"Instead they were passed in as part of `model_kwargs` parameter."
            )

        values["model_kwargs"] = extra
        return values

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        openai_api_key = values.get("openai_api_key", None)

        os.environ["OPENAI_API_KEY"] = openai_api_key
        try:
            import openai

            openai.api_key = openai_api_key
        except ImportError:
            raise ValueError(
                "Could not import openai python package. "
                "Please it install it with `pip install openai`."
            )
        try:
            values["client"] = openai.ChatCompletion
        except AttributeError:
            raise ValueError(
                "`openai` has no `ChatCompletion` attribute, this is likely "
                "due to an old version of the openai package. Try upgrading it "
                "with `pip install --upgrade openai`."
            )
        if values["n"] < 1:
            raise ValueError("n must be at least 1.")
        if values["n"] > 1 and values["streaming"]:
            raise ValueError("n must be 1 when streaming.")
        if "API_KEYS" in values:
            values["api_keys"] = values["API_KEYS"]
        return values

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling OpenAI API."""
        return {
            "model": self.model_name,
            "request_timeout": self.request_timeout,
            "max_tokens": self.max_tokens,
            "stream": self.streaming,
            "n": self.n,
            "temperature": self.temperature,
            **self.model_kwargs,
        }

    def _create_retry_decorator(self) -> Callable[[Any], Any]:
        import openai

        min_seconds = 1
        max_seconds = 60
        # Wait 2^x * 1 second between each retry starting with
        # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
        return retry(
            reraise=True,
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
            retry=(
                retry_if_exception_type(openai.error.Timeout)
                | retry_if_exception_type(openai.error.APIError)
                | retry_if_exception_type(openai.error.APIConnectionError)
                | retry_if_exception_type(openai.error.RateLimitError)
                | retry_if_exception_type(openai.error.ServiceUnavailableError)
            ),
            before_sleep=before_sleep_log(logger, logging.WARNING),
        )

    def completion_with_retry(self, **kwargs: Any) -> Any:
        """Use tenacity to retry the completion call."""
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def _completion_with_retry(**kwargs: Any) -> Any:
            return self.client.create(**kwargs)

        return _completion_with_retry(**kwargs)

    def _combine_llm_outputs(self, llm_outputs: List[Optional[dict]]) -> dict:
        overall_token_usage: dict = {}
        for output in llm_outputs:
            if output is None:
                # Happens in streaming
                continue
            token_usage = output["token_usage"]
            for k, v in token_usage.items():
                if k in overall_token_usage:
                    overall_token_usage[k] += v
                else:
                    overall_token_usage[k] = v
        return {"token_usage": overall_token_usage, "model_name": self.model_name}

    def _generate(
        self,
        messages: List[Chain],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> ChatResult:
        message_dicts, params = self._create_message_dicts(messages, stop)
        if self.streaming:
            inner_completion = ""
            role = "assistant"
            params["stream"] = True
            for stream_resp in self.completion_with_retry(
                messages=message_dicts, **params
            ):
                role = stream_resp["choices"][0]["delta"].get("role", role)
                token = stream_resp["choices"][0]["delta"].get("content", "")
                inner_completion += token
                if run_manager:
                    run_manager.on_llm_new_token(token)
            message = _convert_dict_to_message(
                {"content": inner_completion, "role": role}
            )
            return ChatResult(generations=[ChatGeneration(message=message)])
        response = self.completion_with_retry(messages=message_dicts, **params)
        return self._create_chat_result(response)

    def _create_message_dicts(
        self, messages: List[Chain], stop: Optional[List[str]]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        params: Dict[str, Any] = {**{"model": self.model_name}, **self._default_params}
        if stop is not None:
            if "stop" in params:
                raise ValueError("`stop` found in both the input and default params.")
            params["stop"] = stop
        message_dicts = [_convert_message_to_dict(m) for m in messages]
        return message_dicts, params

    def _create_chat_result(self, response: Mapping[str, Any]) -> ChatResult:
        generations = []
        for res in response["choices"]:
            message = _convert_dict_to_message(res["message"])
            gen = ChatGeneration(message=message)
            generations.append(gen)
        llm_output = {"token_usage": response["usage"], "model_name": self.model_name}
        return ChatResult(generations=generations, llm_output=llm_output)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {**{"model_name": self.model_name}, **self._default_params}

    def get_num_tokens(self, text: str) -> int:
        """Calculate num tokens with tiktoken package."""
        # tiktoken NOT supported for Python 3.7 or below
        if sys.version_info[1] <= 7:
            return super().get_num_tokens(text)
        try:
            import tiktoken
        except ImportError:
            raise ValueError(
                "Could not import tiktoken python package. "
                "This is needed in order to calculate get_num_tokens. "
                "Please install it with `pip install tiktoken`."
            )
        # create a GPT-3.5-Turbo encoder instance
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

        # encode the text using the GPT-3.5-Turbo encoder
        tokenized_text = enc.encode(text)

        # calculate the number of tokens in the encoded text
        return len(tokenized_text)

    def get_num_tokens_from_messages(self, messages: List[Chain]) -> int:
        """Calculate num tokens for gpt-3.5-turbo and gpt-4 with tiktoken package.

        Official documentation: https://github.com/openai/openai-cookbook/blob/
        main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb"""
        try:
            import tiktoken
        except ImportError:
            raise ValueError(
                "Could not import tiktoken python package. "
                "This is needed in order to calculate get_num_tokens. "
                "Please install it with `pip install tiktoken`."
            )

        model = self.model_name
        if model == "gpt-3.5-turbo":
            # gpt-3.5-turbo may change over time.
            # Returning num tokens assuming gpt-3.5-turbo-0301.
            model = "gpt-3.5-turbo-0301"
        elif model == "gmsg.content.rawpt-4":
            # gpt-4 may change over time.
            # Returning num tokens assuming gpt-4-0314.
            model = "gpt-4-0314"

        # Returns the number of tokens used by a list of messages.
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            logger.warning("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        if model == "gpt-3.5-turbo-0301":
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            tokens_per_message = 4
            # if there's a name, the role is omitted
            tokens_per_name = -1
        elif model == "gpt-4-0314":
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(
                f"get_num_tokens_from_messages() is not presently implemented "
                f"for model {model}."
                "See https://github.com/openai/openai-python/blob/main/chatml.md for "
                "information on how messages are converted to tokens."
            )
        num_tokens = 0
        messages_dict = [_convert_message_to_dict(m) for m in messages]
        for message in messages_dict:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        # every reply is primed with <im_start>assistant
        num_tokens += 3
        return num_tokens

    def _truncate_conversation_history(
        self,
        conversation_history: List[Any],
        preserve_context: bool = True,
        min_context_tokens: int = 50,
    ) -> List[Dict[str, str]]:
        if not conversation_history:
            return []

        if self.max_tokens <= 0:
            raise ValueError("max_tokens should be a positive integer.")

        conversation_history_dicts = [
            {
                "role": msg.__class__.__name__.replace("Chain", "").lower(),
                "content": msg.content.text,
            }
            for msg in conversation_history
            if msg.content.text
            is not None  # Only consider messages with non-None content
        ]

        truncated_history = []
        tokens_so_far = 0

        def add_message_to_truncated_history(message: Dict[str, str]) -> int:
            nonlocal tokens_so_far

            # Make sure that message content is a string
            if not isinstance(message["content"], str):
                raise TypeError(
                    f"Expected string for message content, but got {type(message['content'])}"
                )

            tokens_in_message = self.get_num_tokens(message["content"])
            truncated_history.insert(0, message)
            tokens_so_far += tokens_in_message
            return tokens_in_message

        def can_add_message(tokens_in_message: int) -> bool:
            return tokens_so_far + tokens_in_message <= self.max_tokens

        last_user_msg = next(
            (
                msg
                for msg in reversed(conversation_history_dicts)
                if msg["role"] == "user"
            ),
            None,
        )

        if last_user_msg is not None:
            tokens_in_last_user_msg = add_message_to_truncated_history(last_user_msg)
            if tokens_in_last_user_msg > self.max_tokens:
                log_handler(
                    "User message exceeds max_tokens, including it anyway.",
                    level="warning",
                )

        if not preserve_context:
            for msg in reversed(conversation_history_dicts[:-1]):
                tokens_in_msg = self.get_num_tokens(msg["content"])

                if can_add_message(tokens_in_msg):
                    add_message_to_truncated_history(msg)
                else:
                    break
        for idx, msg in enumerate(reversed(conversation_history_dicts[:-1])):
            tokens_in_msg = self.get_num_tokens(msg["content"])

            if can_add_message(tokens_in_msg):
                add_message_to_truncated_history(msg)
            else:
                if preserve_context and tokens_so_far < min_context_tokens:
                    for next_msg in reversed(conversation_history_dicts[: -(idx + 2)]):
                        if next_msg["role"] == "assistant":
                            tokens_in_next_msg = self.get_num_tokens(
                                next_msg["content"]
                            )

                            if can_add_message(tokens_in_next_msg):
                                add_message_to_truncated_history(next_msg)
                                log_handler(
                                    f"Assistant message added to preserve context: {next_msg['content']}",
                                    level="info",
                                )
                            else:
                                log_handler(
                                    "Assistant message skipped due to insufficient tokens for preserving context.",
                                    level="warning",
                                )
                        if tokens_so_far >= min_context_tokens:
                            break
                break

        log_handler(
            f"Truncated conversation history: {truncated_history}", level="info"
        )
        # print detailed token info in a dictioanry
        token_info = {
            "tokens_so_far": tokens_so_far,
        }
        log_handler(f"Token info: {token_info}", level="info")

        return truncated_history

    def invoke(self, messages: List[Chain], stop: Optional[List[str]] = None) -> str:
        """Invoke the completion endpoint synchronously.

        Args:
            messages (List[Chain]): Messages to send to the endpoint.
            stop (Optional[List[str]]): Stop tokens to use for the completion.

        Returns:
            str: The response from the endpoint.
        """
        return self._generate(messages, stop=stop)

    async def _agenerate(
        self,
        messages: List[Chain],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
    ) -> ChatResult:
        message_dicts, params = self._create_message_dicts(messages, stop)
        if self.streaming:
            inner_completion = ""
            role = "assistant"
            params["stream"] = True
            async for stream_resp in await acompletion_with_retry(
                self, messages=message_dicts, **params
            ):
                role = stream_resp["choices"][0]["delta"].get("role", role)
                token = stream_resp["choices"][0]["delta"].get("content", "")
                inner_completion += token
                if run_manager:
                    await run_manager.on_llm_new_token(token)
            message = _convert_dict_to_message(
                {"content": inner_completion, "role": role}
            )
            return ChatResult(generations=[ChatGeneration(message=message)])
        else:
            response = await acompletion_with_retry(
                self, messages=message_dicts, **params
            )
            return self._create_chat_result(response)

    def _embed_text(self, text: str) -> List[float]:
        """Embed a piece of text as a list of floats using the OpenAI API."""
        try:
            response = openai.Embedding.create(
                input=text, engine="text-embedding-ada-002"
            )
            return response["data"][0]["embedding"]
        except Exception as e:
            print(f"Error embedding text: {e}")
            return []

    def _embed_text_batch(
        self, keywords: List[str], batch_size: int = 100
    ) -> List[List[float]]:
        """Embed a list of keywords as a list of lists of floats using the OpenAI API."""
        try:
            for i in range(0, len(keywords), batch_size):
                response = openai.Embedding.create(
                    input=keywords[i : i + batch_size], engine="text-embedding-ada-002"
                )

                embeddings = [item["embedding"] for item in response["data"]]
                if i == 0:
                    all_embeddings = embeddings
                else:
                    all_embeddings.extend(embeddings)
            return all_embeddings
        except Exception as e:
            print(f"Error embedding text: {e}")
            return []

    def _embed_keywords(self, keywords: List[str]) -> List[List[float]]:
        """Embed a list of keywords as a list of embedded vectors using the OpenAI API."""
        return [self._embed_text(keyword) for keyword in keywords]

    def _compute_semantic_vectors(
        self, terms: List[str]
    ) -> List[Tuple[str, List[float]]]:
        """Compute the semantic vectors of a list of terms."""
        return [(term, self._embed_text(term)) for term in terms]

    def _group_terms(
        self, semantic_vectors: List[Tuple[str, List[float]]], use_argmax: bool = True
    ) -> Dict[str, List[Tuple[str, List[float]]]]:
        """Group a list of terms into clusters based on semantic similarity."""
        # Compute pairwise cosine similarity
        terms, vectors = zip(*semantic_vectors)
        similarity_matrix = cosine_similarity(vectors)
        np.fill_diagonal(similarity_matrix, 0)

        # Group terms into clusters
        clusters = {}
        for i, term in enumerate(terms):
            if use_argmax:
                cluster = np.argmax(similarity_matrix[i])
            else:
                cluster = np.max(similarity_matrix[i])
            if cluster not in clusters:
                clusters[cluster] = []
            clusters[cluster].append((term, vectors[i]))

        return clusters

    def compute_similar_keywords(
        self, keywords: List[str], num_keywords: int = 10, use_argmax: bool = True
    ) -> List[str]:
        """Compute a list of similar keywords using a specified language model."""
        semantic_vectors = self._compute_semantic_vectors(keywords)
        clusters = self._group_terms(semantic_vectors, use_argmax=use_argmax)
        sorted_clusters = sorted(clusters.values(), key=len, reverse=True)[
            :num_keywords
        ]
        similar_keywords = [term for cluster in sorted_clusters for term, _ in cluster]
        return similar_keywords

    def group_terms_by_similarity(
        self, semantic_vectors: List[Tuple[str, List[float]]], use_argmax: bool = True
    ) -> Dict[str, List[Tuple[str, List[float]]]]:
        """
        Group a list of terms into clusters based on semantic similarity.
        :param semantic_vectors: List of tuples where the first element is a string term and the second element is a list of float values representing its vector.
        :param use_argmax: If True, the function will use the argmax of the similarity matrix to group terms into clusters. Otherwise, it will use the maximum value.
        :return: Dictionary where the keys are cluster IDs and the values are lists of tuples representing the terms and their vectors.
        """
        if not isinstance(use_argmax, bool):
            raise TypeError("use_argmax must be a boolean.")

        if not semantic_vectors:
            raise ValueError("semantic_vectors must not be empty.")

        terms, vectors = zip(*semantic_vectors)
        similarity_matrix = cosine_similarity(vectors)
        np.fill_diagonal(similarity_matrix, 0)

        clusters = {}
        for i, term in enumerate(terms):
            cluster = np.argmax(similarity_matrix[i])
            if not use_argmax:
                cluster = np.max(similarity_matrix[i])
            if cluster not in clusters:
                clusters[cluster] = []
            clusters[cluster].append((term, vectors[i]))

        return clusters

    def compute_semantic_similarity(
        self, query: str, keywords: List[str]
    ) -> List[Tuple[str, float]]:
        """
        Compute the semantic similarity between a query and a list of keywords using a specified language model.
        """

        try:
            # Compute similarity scores
            query_vector = self._embed_text(query)
            embeddings = self._embed_keywords(keywords)
            similarities = cosine_similarity([query_vector], embeddings)[0]
            similarity_scores = [
                (keyword, similarity)
                for keyword, similarity in zip(keywords, similarities)
            ]
            return similarity_scores

        except ValueError as e:
            logging.error(f"An error occurred while computing semantic similarity: {e}")
            return []

    def predict_semantic_similarity(
        self, query: str, keywords: List[str], threshold: float = 0.5
    ) -> List[str]:
        """
        Predict a list of keywords that are similar to a query using a specified language model.
        """

        try:
            # Compute similarity scores
            query_vector = self._embed_text(query)
            embeddings = self._embed_keywords(keywords)
            similarities = cosine_similarity([query_vector], embeddings)[0]
            similarity_scores = [
                (keyword, similarity)
                for keyword, similarity in zip(keywords, similarities)
            ]

            # Predict keywords
            predicted_keywords = [
                keyword
                for keyword, similarity in similarity_scores
                if similarity >= threshold
            ]

            return predicted_keywords

        except ValueError as e:
            logging.error(
                f"An error occurred while predicting semantic similarity: {e}"
            )
            return []

    def predict_semantic_similarity_batch(
        self, queries: List[str], keywords: List[str], threshold: float = 0.5
    ) -> List[List[str]]:
        """
        Predict a list of keywords that are similar to a list of queries using a specified language model.
        """
        try:
            # Compute similarity scores
            query_vectors = self._embed_text_batch(queries)
            embeddings = self._embed_keywords(keywords)
            similarities = cosine_similarity(query_vectors, embeddings)
            similarity_scores = [
                [
                    (keyword, similarity)
                    for keyword, similarity in zip(keywords, similarities[i])
                ]
                for i in range(len(queries))
            ]

            # Predict keywords
            predicted_keywords = [
                [
                    keyword
                    for keyword, similarity in similarity_score
                    if similarity >= threshold
                ]
                for similarity_score in similarity_scores
            ]
            return predicted_keywords

        except ValueError as e:
            logging.error(
                f"An error occurred while predicting semantic similarity: {e}"
            )
            return []

    def compute_semantic_similarity_batch(
        self, queries: List[str], keywords: List[str]
    ) -> List[List[Tuple[str, float]]]:
        """
        Compute the semantic similarity between a list of queries and a list of keywords using a specified language model.
        """

        try:
            # Compute similarity scores
            query_vectors = self._embed_text_batch(queries)
            embeddings = self._embed_keywords(keywords)
            similarities = cosine_similarity(query_vectors, embeddings)
            similarity_scores = [
                [
                    (keyword, similarity)
                    for keyword, similarity in zip(keywords, similarities[i])
                ]
                for i in range(len(queries))
            ]

            return similarity_scores

        except ValueError as e:
            logging.error(f"An error occurred while computing semantic similarity: {e}")
            return []

    def predict_batch(
        self, queries: List[str], top_n: int = 5
    ) -> List[List[Tuple[str, float]]]:
        """Predict the top N keywords for a list of user queries."""

        # Compute similarity scores
        query_vectors = self._embed_text_batch(queries)
        similarities = cosine_similarity(query_vectors, self._semantic_vectors)
        similarity_scores = [
            [
                (keyword, similarity)
                for keyword, similarity in zip(self.keywords, similarities[i])
            ]
            for i in range(len(queries))
        ]

        # Sort similarity scores
        similarity_scores = [
            [
                (keyword, similarity)
                for keyword, similarity in sorted(
                    similarity_score, key=lambda x: x[1], reverse=True
                )
            ]
            for similarity_score in similarity_scores
        ]

        # Return top N keywords
        return [similarity_score[:top_n] for similarity_score in similarity_scores]

    def predict_batch(
        self, queries: List[str], top_n: int = 5
    ) -> List[List[Tuple[str, float]]]:
        """Predict the top N keywords for a list of user queries."""

        # Compute similarity scores
        query_vectors = self._embed_text_batch(queries)
        similarities = cosine_similarity(query_vectors, self._semantic_vectors)
        similarity_scores = [
            [
                (keyword, similarity)
                for keyword, similarity in zip(self.keywords, similarities[i])
            ]
            for i in range(len(queries))
        ]

        # Sort similarity scores
        similarity_scores = [
            [
                (keyword, similarity)
                for keyword, similarity in sorted(
                    similarity_score, key=lambda x: x[1], reverse=True
                )
            ]
            for similarity_score in similarity_scores
        ]

        # Return top N keywords
        return [similarity_score[:top_n] for similarity_score in similarity_scores]

    def predict(
        self, query: str, top_n: int = 5, threshold: float = 0.5
    ) -> List[Tuple[str, float]]:
        """Predict the top N keywords for a user query."""

        # Compute similarity scores
        query_vector = self._embed_text(query)
        similarities = cosine_similarity([query_vector], self._semantic_vectors)[0]
        similarity_scores = [
            (keyword, similarity)
            for keyword, similarity in zip(self.keywords, similarities)
        ]

        # Sort similarity scores
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Return top N keywords
        return [
            similarity_score
            for similarity_score in similarity_scores
            if similarity_score[1] >= threshold
        ][:top_n]


async def acompletion_with_retry(llm: ChatOpenAI, **kwargs: Any) -> Any:
    """Use tenacity to retry the async completion call."""
    retry_decorator = _create_retry_decorator(llm)

    @retry_decorator
    async def _completion_with_retry(**kwargs: Any) -> Any:
        # Use OpenAI's async api https://github.com/openai/openai-python#async-api
        return await llm.client.acreate(**kwargs)

    return await _completion_with_retry(**kwargs)
