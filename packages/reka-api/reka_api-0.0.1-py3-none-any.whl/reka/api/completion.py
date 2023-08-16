"""Completion-related server interactions."""
from typing import List, Optional, cast

import reka.api.driver as driver


def completion(
    prompt: str,
    model_name: str = "text-phoenix-v1",
    request_output_len: int = 256,
    temperature: float = 1.0,
    random_seed: int = 0,
    runtime_top_k: int = 1024,
    runtime_top_p: float = 0.95,
    repetition_penalty: float = 1.0,
    len_penalty: float = 1.0,
    stop_tokens: Optional[List[str]] = None,
) -> str:
    """Request a text completion in synchronous mode.

    Example usage:
    ```python
    import reka
    reka.API_KEY = "APIKEY"

    result = reka.completion("What is the capital of the UK?")
    print(completion)  # "The capital of the United Kingdom is London. ..."
    ```

    Args:
        prompt: string.
        model_name: Name of model. Currently only supports text-phoenix-v1.
        request_output_len: Completion length in tokens.
        temperature: Softmax temperature, higher is more diverse.
        random_seed: Seed to obtain different results.
        runtime_top_k: Keep only k top tokens when sampling.
        runtime_top_p: Keep only top p quantile when sampling.
        repetition_penalty: Untested! Penalize repetitions. 1 means no penalty.
        len_penalty: Untested! Penalize short answers. 1 means no penalty.
        stop_tokens: Optinoal list of words on which to stop generation.

    Returns:
        model completion.
    """
    json_dict = dict(
        prompts=[prompt],
        model_name=model_name,
        request_output_len=request_output_len,
        temperature=temperature,
        random_seed=random_seed,
        runtime_top_k=runtime_top_k,
        runtime_top_p=runtime_top_p,
        repetition_penalty=repetition_penalty,
        len_penalty=len_penalty,
        stop_tokens=stop_tokens or [],
    )

    response = driver.make_request(
        method="post",
        endpoint="completion",
        headers={"Content-Type": "application/json"},
        json=json_dict,
    )

    return cast(str, response["text"][0])
