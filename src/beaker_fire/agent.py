import json
import logging
import re
import requests
from time import sleep
import asyncio
import os

from archytas.tool_utils import AgentRef, LoopControllerRef, ReactContextRef, tool
from typing import Any, List, Optional

from beaker_kernel.lib.agent import BeakerAgent
from beaker_kernel.lib.context import BeakerContext
from beaker_kernel.lib.utils import ExecutionError

from pathlib import Path

logger = logging.getLogger(__name__)

JSON_OUTPUT = False

class BeakerFireAgent(BeakerAgent):
    """
    You are the Beaker Fire Agent, a chat assistant that helps users with wildfire research tasks.
    """

    def __init__(
        self,
        context: "BeakerContext" = None,
        tools: Optional[list] = None,
        **kwargs
    ):
        super().__init__(context=context, tools=tools, **kwargs)
        
        # Load prompt files and set the Agent context
        self.logger = logger
        self.root_folder = Path(__file__).resolve().parent
        prompts_dir = os.path.join(self.root_folder, 'prompts')

        # Read agent.md first
        agent_file = os.path.join(prompts_dir, 'agent.md')
        if os.path.exists(agent_file):
            with open(agent_file, 'r') as f:
                self.add_context(f.read())
        
        # Read remaining .md files
        for file in os.listdir(prompts_dir):
            if file.endswith('.md') and file != 'agent.md' and file != 'acled.md': 
                with open(os.path.join(prompts_dir, file), 'r') as f:
                    self.add_context(f.read())

    @tool(autosummarize=True)
    async def extract_pdf(self, pdf_path: str, agent: AgentRef) -> str:
        """
        Extract the text from a PDF file using PyPDF2.

        Args:
            pdf_path (str): The path to the PDF file to extract text from.            

        Returns:
            str: The extracted text from the PDF file.
        """
        code = agent.context.get_code("extract_pdf", {'pdf_path': pdf_path})
        response = await agent.context.evaluate(code)
        return response["return"]