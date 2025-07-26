from langgraph.graph import StateGraph, START, END
from src.langgraphagenticAI.state.state import State
from src.langgraphagenticAI.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticAI.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition, ToolNode
from src.langgraphagenticAI.nodes.chatbot_with_tool import ChatbotWithToolNode
from src.langgraphagenticAI.nodes.ainews_node import AINewsNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the 'BasicChatbotNode' class
        and integrates it into the graph. the chatbot node is set as both the entry
        and exit point of the graph
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_build_graph(self):
        """Builds an advanced chatbot graph with tools integration.
        This method creates a chatbot graph that includes both a chatbot node
        and a tool node. It defines tools, initializes the chatbot with tool
        capabilities and sets up conditional and direct edges between nodes.
        The chatbot node is set as the entry point."""

        #Define the tools and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)

        llm = self.llm

        obj_chatbot_with_node= ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)

        #ADd nodes
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        #define the conditional and direct edges:
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")


    def ainews_builder_graph(self):
        ainews_node = AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news", ainews_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ainews_node.summarize_news)
        self.graph_builder.add_node("save_results", ainews_node.save_result)


        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_results")
        self.graph_builder.add_edge("save_results", END)


    def setup_graph(self, usecase:str):
        """Sets up the graph for the selected use case."""
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with Web":
            self.chatbot_with_tools_build_graph()

        if usecase=="AI News":
            self.ainews_builder_graph()

        return self.graph_builder.compile()
