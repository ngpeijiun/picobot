import click
from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from rich.console import Console, Group
from rich.live import Live
from rich.text import Text

from .tools import (
    delete_path,
    edit_file,
    list_dir,
    move_path,
    read_file,
    write_file,
)

agent = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[list_dir, read_file, write_file, edit_file, move_path, delete_path],
    checkpointer=MemorySaver(),
    system_prompt="Keep your response concise. Make any changes minimal and non-disruptive.",
)

console = Console()
session_cost = 0.0


def block(title: str, content: str, style: str) -> Group:
    w = console.width
    top = f"\u2500 {title} " + "\u2500" * (w - len(f"\u2500 {title} "))
    bot = "\u2500" * w
    return Group(
        Text(top, style=style),
        Text(content, style=style),
        Text(bot, style=style),
    )


def bot_reply_stream(user_input: str) -> None:
    global session_cost
    config = {"configurable": {"thread_id": "main"}}
    bot_text = ""
    input_tokens = 0
    cached_input_tokens = 0
    output_tokens = 0

    try:
        with Live(
            block("Bot", "", "cornflower_blue"),
            console=console,
            refresh_per_second=10,
        ) as live:
            for mode, data in agent.stream(
                {"messages": [{"role": "user", "content": user_input}]},
                config=config,
                stream_mode=["messages", "updates"],
            ):
                if mode == "messages":
                    chunk, metadata = data
                    if isinstance(chunk, AIMessageChunk) and chunk.content:
                        bot_text += chunk.content
                        live.update(block("Bot", bot_text, "cornflower_blue"))

                    usage_metadata = getattr(chunk, "usage_metadata", None) or {}

                    if usage_metadata:
                        used_input = usage_metadata.get("input_tokens", 0)
                        used_output = usage_metadata.get("output_tokens", 0)
                        input_tokens += used_input
                        output_tokens += used_output

                        input_details = usage_metadata.get("input_token_details", {}) or {}
                        cached = input_details.get("cache_read", 0)
                        cached_input_tokens += cached
                elif mode == "updates":
                    for node_name, state_delta in data.items():
                        for msg in state_delta.get("messages", []):
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                for tc in msg.tool_calls:
                                    console.print(block("Tool Call", f"{tc['name']}({tc['args']})", "gold3"))
                            elif isinstance(msg, ToolMessage):
                                console.print(block(f"Tool Result: {msg.name}", msg.content.strip(), "cyan"))
    except Exception as e:
        console.print(f"[red][Error][/red] {e}")

    cost = (input_tokens * 0.00000075) + (cached_input_tokens * 0.000000075) + (output_tokens * 0.0000045)
    session_cost += cost
    console.print(
        f"(input: {input_tokens}, cached: {cached_input_tokens}, output: {output_tokens}, "
        f"cost: ${cost:.6f}, session total: ${session_cost:.6f})"
    )


@click.command()
def chat():
    click.echo("Bot: Hello! Type 'exit' to quit.")

    while True:
        user_input = click.prompt("You")

        if user_input.lower() in {"exit", "quit"}:
            click.echo("Bot: Bye!")
            break

        console.print(block("You", user_input, "slate_blue1"))
        bot_reply_stream(user_input)


if __name__ == "__main__":
    chat()
