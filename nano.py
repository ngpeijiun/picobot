import click
from langchain.agents import create_agent
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

@click.command()
def chat():
    click.echo("Bot: Hello! Type 'exit' to quit.")

    while True:
        user_input = click.prompt("You")

        if user_input.lower() in {"exit", "quit"}:
            click.echo("Bot: Bye!")
            break

        click.echo(f"Bot: {bot_reply(user_input)}")


if __name__ == "__main__":
    chat()
