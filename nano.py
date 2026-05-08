import click
from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk, ToolMessage
from langchain_community.callbacks import get_openai_callback
from langgraph.checkpoint.memory import MemorySaver

from read_file import read_file

agent = create_agent(
    model="gpt-5.4-mini",
    tools=[read_file],
    checkpointer=MemorySaver(),
    system_prompt="Keep your response concise.",
)


def bot_reply(user_input: str) -> str:
    config = {"configurable": {"thread_id": "main"}}
    with get_openai_callback() as cb:
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]}, config=config)
    response = result["messages"][-1].content
    usage_text = f"(input: {cb.prompt_tokens}, output: {cb.completion_tokens}, total: {cb.total_tokens}, cost: ${cb.total_cost})"
    return f"{response}\n{usage_text}"


def bot_reply_stream(user_input: str) -> None:
    config = {"configurable": {"thread_id": "main"}}
    tool_call_accumulator: dict[int, dict] = {}  # index -> {name, args}

    with get_openai_callback() as cb:
        for chunk, metadata in agent.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
            stream_mode="messages"
        ):
            if isinstance(chunk, AIMessageChunk):
                if chunk.tool_call_chunks:
                    for tc in chunk.tool_call_chunks:
                        idx = tc.get("index", 0)
                        if idx not in tool_call_accumulator:
                            tool_call_accumulator[idx] = {"name": tc.get("name", ""), "args": ""}
                        else:
                            if tc.get("name"):
                                tool_call_accumulator[idx]["name"] = tc["name"]
                        tool_call_accumulator[idx]["args"] += tc.get("args") or ""
                elif chunk.content:
                    print(chunk.content, end="", flush=True)
            elif isinstance(chunk, ToolMessage):
                # Flush any pending tool calls now that we have complete args
                for tc in tool_call_accumulator.values():
                    print(f"\n[Tool Call]\n{tc['name']}({tc['args']})", flush=True)
                    print("-" * 6)
                tool_call_accumulator.clear()
                print(f"[Tool Result]\n{chunk.name}\n{chunk.content}", flush=True)
                print("-" * 6)
    print()
    print(f"(input: {cb.prompt_tokens}, output: {cb.completion_tokens}, total: {cb.total_tokens}, cost: ${cb.total_cost})")


@click.command()
def chat():
    click.echo("Bot: Hello! Type 'exit' to quit.")

    while True:
        user_input = click.prompt("You")

        if user_input.lower() in {"exit", "quit"}:
            click.echo("Bot: Bye!")
            break

        #click.echo(f"Bot: {bot_reply(user_input)}")
        print("Bot: ", end="", flush=True)
        bot_reply_stream(user_input)


if __name__ == "__main__":
    chat()
