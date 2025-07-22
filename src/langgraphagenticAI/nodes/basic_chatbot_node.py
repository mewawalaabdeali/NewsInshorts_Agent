from src.langgraphagenticAI.state.state import State

class BasicChatbotNode:
    """Basic Chatbot logic implementation"""
    def __init__(self, model):
        self.llm = model

    def process(self, state:State) -> dict:
        """Process the input state and generate a response"""

        return {"messages": self.llm.invoke(state["messages"])}