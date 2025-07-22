#from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch

def get_tools():
    """Returns the list of tools to be used in the chatbot"""

    tools = [TavilySearch(max_results = 2)]
    return tools

def create_tool_node(tools):
    """Creates and returns a tool node for the graph"""
    return ToolNode(tools=tools)