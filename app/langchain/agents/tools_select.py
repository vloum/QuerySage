from langchain.tools import Tool, StructuredTool
from .tools import *

## 请注意，如果你是为了使用AgentLM，在这里，你应该使用英文版本。

tools = [
    Tool.from_function(
        func=calculate,
        name="calculate",
        description="Useful for when you need to answer questions about simple calculations",
        args_schema=CalculatorInput,
    ),
    Tool.from_function(
        func=arxiv,
        name="arxiv",
        description="A wrapper around Arxiv.org for searching and retrieving scientific articles in various fields.",
        args_schema=ArxivInput,
    ),
    Tool.from_function(
        func=weathercheck,
        name="weather_check",
        description="",
        args_schema=WhetherSchema,
    ),
    Tool.from_function(
        func=shell,
        name="shell",
        description="Use Shell to execute Linux commands",
        args_schema=ShellInput,
    ),
    # Tool.from_function(
    #     func=search_knowledgebase_complex,
    #     name="search_knowledgebase_complex",
    #     description="Use Use this tool to search local knowledgebase and get information",
    #     args_schema=KnowledgeSearchInput,
    # ),
    Tool.from_function(
        func=search_internet,
        name="search_internet",
        description="Use this tool to use bing search engine to search the internet",
        args_schema=SearchInternetInput,
    ),
    Tool.from_function(
        func=wolfram,
        name="Wolfram",
        description="Useful for when you need to calculate difficult formulas",
        args_schema=WolframInput,
    ),
    Tool.from_function(
        func=search_youtube,
        name="search_youtube",
        description="use this tools to search youtube videos",
        args_schema=YoutubeInput,
    ),
    Tool.from_function(
        func=dalle_image_generator,
        name="dalle_image_generator",
        description="Activate the painting function of this tool to create an artistic illustration",
        args_schema=DalleImageGeneratorInput,
    ),
    Tool.from_function(
      func=save_knowledge,
      name="save_knowledge",
      description="Save knowledge, including information about my life, to the knowledge base.",
      args_schema=KnowledgeInput
    ),
    Tool.from_function(
      func=search_knowledge,
      name="search_knowledge",
      description="Retrieve personal data and other relevant information from the knowledge base to address inquiries.",
      args_schema=KnowledgeSearchInput
    ),
    Tool.from_function(
      func=query_big_file,
      name="query_big_file",
      description="Large File Inspection and Correction Expert, used for retrieving information from large files and conducting in-depth review and error correction. Large File Inspection and Correction Expert, used for retrieving information from large files and conducting in-depth review and error correction. The input format must be in YAML. For example:\n\n```yaml\nfile_id: xxx\nquestion: xxx",
      args_schema=BigFileChatInput
    )
]

tool_names = [tool.name for tool in tools]

print('tool_names--', tool_names)
