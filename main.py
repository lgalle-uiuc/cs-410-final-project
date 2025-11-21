from dotenv import load_dotenv
import logging

load_dotenv()

from agent import get_agent
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        # https://docs.langchain.com/oss/python/langchain/rag
        agent = get_agent()

        while True:
            # Prompt user for question
            question = input("Please enter your question (or type 'exit' to quit): ")

            if question.lower() == 'exit':
                print("Exiting the program. Goodbye!")
                break

            for step in agent.stream(
                {"messages": [{"role": "user", "content": question}]},
                stream_mode="values",
            ):
                step["messages"][-1].pretty_print()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    

if __name__ == "__main__":
    main()