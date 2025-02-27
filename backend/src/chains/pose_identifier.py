from typing import Any

from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import Runnable, RunnablePassthrough
from common.constants import ALL_CONFIGS

# Load the model settings
MODEL_SETTINGS = ALL_CONFIGS.get_config("analyst_perspective", "llm")


class PoseIdentifierChain:
    def __init__(self, *args, **kwargs):
        self._chain = []

    def create_chain(self) -> Runnable[dict[str, Any], Any]:
        """
        Creates a Gemini chain to summarize transcripts.
        """

        # Get context chain
        contexts_chain = RunnablePassthrough().assign(
            transcript_data=lambda x: get_transcripts([x["company_id"]], count=1, filter="Analysts"),
            company_name=lambda x: get_company_metadata(int(x["company_id"]))[0]["company_name"],
        )

        llm = ChatGoogleGenerativeAI(
            model=MODEL_SETTINGS["model_name"],
            temperature=MODEL_SETTINGS["temperature"],
            max_output_tokens=MODEL_SETTINGS["max_output_tokens"],
            cache=self.cache,
        )

        parser = JsonOutputParser(pydantic_object=Output)

        PROMPT = PromptTemplate(
            template=TEMPLATE,
            input_variables=["company_id", "company_name", "transcript_data"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        base_chain = (PROMPT | llm | parser).with_types(input_type=BaseChainInput, output_type=Output)

        return (contexts_chain | base_chain).with_types(input_type=Input, output_type=Output)
