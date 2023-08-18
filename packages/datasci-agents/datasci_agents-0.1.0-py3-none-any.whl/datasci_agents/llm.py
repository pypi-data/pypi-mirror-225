import json
from dotenv import load_dotenv

from litellm import completion as llm_completion

load_dotenv(override=True)


def print_messages(messages):
    for message in messages:
        print(f"[{message['role']}]\n{message['content']}\n\n")


def llm_complete(
    messages,
    model="gpt-4",
    temperature=0.0,
    json_keys=None,
    json_retry=3,
    verbose=False,
):
    if verbose:
        print_messages(messages)
    response = llm_completion(messages=messages, model=model, temperature=temperature)  # type: ignore
    content = response["choices"][0]["message"]["content"]
    if verbose:
        print(f"[llm]\n{content if content is not None else '[FAILED]'}\n\n")
    content = content.strip()
    if json_keys:
        try:
            content = json.loads(content)
            for key in json_keys:
                assert key in content
        except:
            if json_retry > 0:
                print("JSON completion failed, retrying...")
                return llm_complete(
                    messages=messages,
                    model=model,
                    temperature=max(temperature, 0.5),
                    json_keys=json_keys,
                    json_retry=json_retry - 1,
                )
            else:
                print("JSON completion failed, giving up.")
                raise
    return content
