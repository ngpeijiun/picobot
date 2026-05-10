import click
from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk, ToolMessage
from langchain_community.callbacks import get_openai_callback
from langgraph.checkpoint.memory import MemorySaver
from rich.console import Console, Group
from rich.live import Live
from rich.text import Text

from .read_file import read_file
from .list_dir import list_dir

agent = create_agent(
    model="gpt-5.4-mini",
    tools=[read_file, list_dir],
    checkpointer=MemorySaver(),
    system_prompt="Keep your response concise.",
)

console = Console()


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
    config = {"configurable": {"thread_id": "main"}}
    bot_text = ""

    with get_openai_callback() as cb:
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

    console.print(
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

        console.print(block("You", user_input, "slate_blue1"))
        bot_reply_stream(user_input)


if __name__ == "__main__":
    chat()
