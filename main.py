from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a:float, b:float)->str:
    """Useful for performing basic arithmetic calculations"""
    print("Calcy tool has been called")
    return f"The sum of {a} and {b} is {a+b}"

@tool
def say_hello(name:str)->str:
    """Useful for sending customized greetings"""
    print("Greeting tool has been called")
    return f"Hello {name}, hope you are feeling fab today!"

def main():
    #load the model
    model=ChatOpenAI(temperature=0)
    tools =[calculator,say_hello]
    agent_executor = create_react_agent(model,tools)

    print("Hello WOrld; I am your AI Bestie. Type 'quit' to exit. ")
    print("You can ask me to do math or chat with me")

    while True:
        #take user input 
        user_input = input("\nYou: ").strip()
          
        if user_input == "quit":
            break
            
        #send user input to the agent
        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}
            ):
                if "agent" in chunk and "messages" in chunk["agent"]:
                    for message in chunk["agent"]["messages"]:
                        print(message.content, end="")
        print()
            

if __name__ == "__main__":
    main()

    