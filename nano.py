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
    with get_openai_callback() as cb:
        try:
            for mode, data in agent.stream(
                {"messages": [{"role": "user", "content": user_input}]},
                config=config,
                stream_mode=["messages", "updates"],
            ):
                if mode == "messages":
                    # Token-by-token: only stream final AI text
                    chunk, metadata = data
                    if isinstance(chunk, AIMessageChunk) and chunk.content:
                        print(chunk.content, end="", flush=True)

                elif mode == "updates":
                    # Complete node output: tool calls and tool results have full args here
                    for node_name, state_delta in data.items():
                        for msg in state_delta.get("messages", []):
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                for tc in msg.tool_calls:
                                    print(f"\n[Tool Call] {tc['name']}({tc['args']})", flush=True)
                                    print("-" * 6, flush=True)
                            elif isinstance(msg, ToolMessage):
                                print(f"[Tool Result] {msg.name}", flush=True)
                                print(msg.content, flush=True)
                                print("-" * 6, flush=True)

        except Exception as e:
            print(f"\n[Error] {e}", flush=True)
    print()
    print(
        f"(input: {cb.prompt_tokens}, output: {cb.completion_tokens}, "
        f"total: {cb.total_tokens}, cost: ${cb.total_cost})"
    )


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
