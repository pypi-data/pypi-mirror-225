import replicate

from cursive.build_input import build_completion_input
from cursive.custom_types import CompletionPayload
from cursive.utils import filter_null_values

class ReplicateClient:
    client: replicate.Client

    def __init__(self, api_key: str):
        self.client = replicate.Client(api_key)

    def create_completion(self, payload: CompletionPayload):  # noqa: F821
        prompt = build_completion_input(payload.messages)
        payload = filter_null_values({
            'model': payload.model,
            'max_new_tokens': payload.max_tokens or 2000,
            'max_length': payload.max_length or 2000,
            'prompt': prompt,
            'temperature': payload.temperature or 0.7,
            'top_p': payload.top_p,
            'top_k': payload.top_k,
            'stop': payload.stop,
        })
        return self.client.predictions.create(
            input=payload, 
            stream=payload.stream or False
        )