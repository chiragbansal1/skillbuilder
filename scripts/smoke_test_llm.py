"""
Smoke test — confirm the configured LLM works end-to-end.

Run: python -m scripts.smoke_test_llm
"""
from dotenv import load_dotenv
load_dotenv()

from core.llm.factory import make_llm_client
from core.types import Message


def main():
    client = make_llm_client()
    print(f"Using LLM client: {client.__class__.__name__}")

    resp = client.chat(
        messages=[Message(role="user", content="Say hello in one short sentence.")],
        system="You are a friendly assistant.",
    )
    print("---")
    print(f"Response: {resp.content}")
    print(f"Stop reason: {resp.stop_reason}")
    print(f"Usage: {resp.usage}")


if __name__ == "__main__":
    main()
