from conduit.async_ import ConduitAsync, GenerationParams, ConduitOptions, Verbosity
from conduit.config import settings
from conduit.core.prompt.prompt_loader import PromptLoader
from pathlib import Path
import argparse
import sys

PROMPTS_PATH = Path(__file__).parent / "prompts"

prompt_loader = PromptLoader(PROMPTS_PATH)


async def judge(draft: str) -> str:
    """
    Judge the quality of the draft and provide feedback.
    """
    prompt = prompt_loader["judge"]
    options = ConduitOptions(
        project_name="deslop",
        verbosity=Verbosity.PROGRESS,
        cache=settings.default_cache("deslop"),
    )
    params = GenerationParams(model="gemini3")
    conduit = ConduitAsync(prompt=prompt)
    input_variables = {"draft": draft}
    response = await conduit.run(
        input_variables=input_variables, params=params, options=options
    )
    return str(response.content)


async def revise(draft: str, critique: str) -> str:
    """
    Revise the draft based on the critique provided by the judge.
    """
    prompt = prompt_loader["reviser"]
    options = ConduitOptions(
        project_name="deslop",
        verbosity=Verbosity.PROGRESS,
        cache=settings.default_cache("deslop"),
    )
    params = GenerationParams(model="opus")
    conduit = ConduitAsync(prompt=prompt)
    input_variables = {"draft": draft, "critique": critique}
    response = await conduit.run(
        input_variables=input_variables, params=params, options=options
    )
    return str(response.content)


async def deslop(draft: str) -> str:
    """
    Main function to perform the deslop process.
    """
    critique = await judge(draft)
    draft = await revise(draft, critique)
    return draft


async def main():
    # Capture stdio input if no draft is provided as an argument
    stdin_input = sys.stdin.read().strip()
    if stdin_input:
        draft = stdin_input
    else:
        parser = argparse.ArgumentParser(
            description="Deslop: A tool for improving writing drafts."
        )
        parser.add_argument("draft", type=str, help="The initial draft to be improved.")
        args = parser.parse_args()
        draft = args.draft

    final_draft = await deslop(draft)
    print("Final Draft:\n", final_draft)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
