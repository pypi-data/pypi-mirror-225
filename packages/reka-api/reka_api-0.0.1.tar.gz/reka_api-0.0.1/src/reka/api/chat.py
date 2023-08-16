"""Chat-related server interactions (including VLM chat)"""
from typing import Dict, List, Optional

import reka.api.driver as driver
from reka.errors import InvalidConversationError


def chat(
    human: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    retrieval_dataset: Optional[str] = None,
    model_name: str = "text-phoenix-v1",
    request_output_len: int = 256,
    temperature: float = 1.0,
    random_seed: Optional[int] = None,
    runtime_top_k: int = 1024,
    runtime_top_p: float = 0.95,
    repetition_penalty: float = 1.0,
    len_penalty: float = 1.0,
    stop_tokens: Optional[List[str]] = None,
    assistant_start_text: Optional[str] = None,
) -> Dict[str, str]:
    """Chat endpoint.

    Example usage:
    ```python
    import reka

    reka.API_KEY = "APIKEY"

    conversation_history = [
        {"type": "human", "text": "Hi, my name is John."},
        {"type": "model", "text": "Hi, I'm Reka's assistant."},
    ]
    response = reka.chat(
        human="What was my name?",
        conversation_history=conversation_history,
    )
    print(response) # {"type": "model", "text": "Your name is John.\\n\\n"}
    ```

    Args:
        human: latest message from human.
        conversation_history: where each dict has a key "type"
            indicating the speaker, either "human" or "model", and a key "text"
            containing the message from the speaker. If not set, will default to
            an empty history.
        retrieval_dataset: Previousy adapted dataset to do retrieval on.
        model_name: Name of model. Currently only supports text-phoenix-v1.
        request_output_len: Completion length in tokens.
        temperature: Softmax temperature, higher is more diverse.
        random_seed: Seed to obtain different results.
        runtime_top_k: Keep only k top tokens when sampling.
        runtime_top_p: Keep only top p quantile when sampling.
        repetition_penalty: Untested! Penalize repetitions. 1 means no penalty.
        len_penalty: Untested! Penalize short answers. 1 means no penalty.
        stop_tokens: Optional list of words on which to stop generation.
        assistant_start_text: Optional text that the assistant response should start with.

    Raises:
        InvalidConversationError: if the conversation history is not valid.

    Returns:
        Dict[str, str]: A dict containing `{"type": "model", "text": <response from the model>}`
    """
    full_conv = (conversation_history or []) + [{"type": "human", "text": human}]
    _check_conversation_history(full_conv, is_vlm=False)
    json_dict = dict(
        conversation_history=full_conv,
        retrieval_dataset=retrieval_dataset,
        model_name=model_name,
        request_output_len=request_output_len,
        temperature=temperature,
        random_seed=random_seed,
        runtime_top_k=runtime_top_k,
        runtime_top_p=runtime_top_p,
        repetition_penalty=repetition_penalty,
        len_penalty=len_penalty,
        stop_tokens=stop_tokens or [],
        assistant_start_text=assistant_start_text,
    )

    response = driver.make_request(
        method="post",
        endpoint="chat",
        headers={"Content-Type": "application/json"},
        json=json_dict,
    )

    return response


def vlm_chat(
    conversation_history: List[Dict[str, str]],
    retrieval_dataset: Optional[str] = None,
    model_name: str = "default_vlm",
    request_output_len: int = 256,
    temperature: float = 1.0,
    random_seed: Optional[int] = None,
    runtime_top_k: int = 1024,
    runtime_top_p: float = 0.95,
    repetition_penalty: float = 1.0,
    len_penalty: float = 1.0,
    stop_tokens: Optional[List[str]] = None,
    assistant_start_text: Optional[str] = None,
) -> Dict[str, str]:
    """VLM Chat endpoint.

    Example usage:
    ```python
    import reka
    reka.API_KEY = "APIKEY"

    conversation_history = [
        {"type": "human", "text": "What's in the photo?", "image_url": "http://images.cocodataset.org/test2017/000000557146.jpg"},
    ]
    response = reka.vlm_chat(conversation_history=conversation_history)
    print(response) # {"type": "model", "text": "A cat laying on the ground with a toy."}
    ```

    Args:
        conversation_history: list of dicts, where each dict has a key "type"
            indicating the speaker, either "human" or "model", and a key "text"
            containing the message from the speaker. This should end with a human turn,
            and the first turn should be a human turn that also contains an "image_url"
            key.
        retrieval_dataset: Previously adapted dataset to do retrieval on.
        model_name: Name of model. Currently only supports text-phoenix-v1.
        request_output_len: Completion length in tokens.
        temperature: Softmax temperature, higher is more diverse.
        random_seed: Seed to obtain different results.
        runtime_top_k: Keep only k top tokens when sampling.
        runtime_top_p: Keep only top p quantile when sampling.
        repetition_penalty: Untested! Penalize repetitions. 1 means no penalty.
        len_penalty: Untested! Penalize short answers. 1 means no penalty.
        stop_tokens: Optional list of words on which to stop generation.
        assistant_start_text: Optional text that the assistant response should start with.

    Raises:
        InvalidConversationError: if the conversation history is not valid.

    Returns:
        Dict[str, str]: A dict containing `{"type": "model", "text": <response from the model>}`
    """
    _check_conversation_history(conversation_history, is_vlm=True)
    json_dict = dict(
        conversation_history=conversation_history,
        retrieval_dataset=retrieval_dataset,
        model_name=model_name,
        request_output_len=request_output_len,
        temperature=temperature,
        random_seed=random_seed,
        runtime_top_k=runtime_top_k,
        runtime_top_p=runtime_top_p,
        repetition_penalty=repetition_penalty,
        len_penalty=len_penalty,
        stop_tokens=stop_tokens or [],
        assistant_start_text=assistant_start_text,
    )

    response = driver.make_request(
        method="post",
        endpoint="vlm-chat",
        headers={"Content-Type": "application/json"},
        json=json_dict,
    )

    return response


def _check_conversation_history(
    conversation_history: List[Dict[str, str]], is_vlm: bool = False
) -> None:
    """Checks that a conversation is well constructed.

    Raises InvalidConversationError otherwise.
    """
    if len(conversation_history) == 0:
        raise InvalidConversationError("Conversation history cannot be empty")

    for i, turn in enumerate(conversation_history):
        expected_keys = {"type", "text"} | (
            {"image_url"} if is_vlm and i == 0 else set()
        )
        turn_keys = set(turn.keys())
        if turn_keys != expected_keys:
            raise InvalidConversationError(
                f"Expected keys {expected_keys} for turn {i} '{turn}', got keys {turn_keys}."
            )
        for key, value in turn.items():
            if not isinstance(value, str):
                raise InvalidConversationError(
                    f"Expected string for value of '{key}' in turn {i} '{turn}', got {type(value)}."
                )
        expected_type = ["human", "model"][i % 2]
        if turn["type"] != expected_type:
            raise InvalidConversationError(
                f"Expected type '{expected_type}' for turn {i} '{turn}', got '{turn['type']}'. Conversations should "
                "alternate between 'human' and 'model', starting with 'human'."
            )
    if conversation_history[-1]["type"] != "human":
        raise InvalidConversationError("Conversation should end with a 'human' turn.")
