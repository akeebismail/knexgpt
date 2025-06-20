"""
Data Extraction Agent for parsing structured and unstructured data.
"""

import asyncio
import csv
import json
from typing import Union

from knexgpt.communication.message_queue import MessageQueueClient
from knexgpt.db.adapter import GraphQuery
from knexgpt.db.adapter_factory import create_adapter
from knexgpt.db.query_translator import QueryTranslator

from .base import BaseAgent


class DataExtractionAgent(BaseAgent):
    """Agent responsible for data extraction tasks."""

    def __init__(self, db_type: str, db_config: dict):
        super().__init__(name="DataExtractionAgent")
        self.adapter = create_adapter(db_type, **db_config)
        self.translator = QueryTranslator()
        self.mq_client = MessageQueueClient(queue_name="data_extraction")

    async def perform_task(self, data_source: Union[str, dict], *args, **kwargs):
        """Perform data extraction from the given source.

        Args:
            data_source: Source of the data to extract
        """
        self.log(f"Extracting data from {data_source}")
        extracted_data = self.extract_data(data_source)
        # Translate and execute a query
        sparql_query = "SELECT ?s WHERE { ?s ?p ?o }"
        cypher_query = self.translator.translate(sparql_query, "cypher")
        if cypher_query:
            result = await self.adapter.execute_query(GraphQuery(query=cypher_query))
            self.log(f"Query result: {result.data}")
        self.mq_client.send_message({"task": "enrich", "data": extracted_data})
        return extracted_data

    def extract_data(self, data_source: Union[str, dict]) -> dict:
        """Extract data from the source.

        Args:
            data_source: Source of the data to extract (file path or dictionary)

        Returns:
            Extracted data as a dictionary
        """
        if isinstance(data_source, dict):
            return data_source

        try:
            with open(data_source, "r") as file:
                if data_source.endswith(".json"):
                    return json.load(file)
                elif data_source.endswith(".csv"):
                    reader = csv.DictReader(file)
                    return [row for row in reader]
                else:
                    return {"text": file.read()}
        except Exception as e:
            self.log(f"Failed to extract data: {e}")
            return {}

    def start_listening(self):
        """Start listening for incoming messages."""
        self.mq_client.receive_messages(self.handle_message)

    def handle_message(self, message: dict):
        """Handle incoming messages."""
        self.log(f"Received message: {message}")
        if message.get("task") == "extract":
            data_source = message.get("data_source")
            if data_source:
                asyncio.run(self.perform_task(data_source))

    def process_json_output(self, json_output: dict) -> dict:
        """Process the JSON output from the PDF upload.

        Args:
            json_output: The JSON output from the upload.

        Returns:
            Processed data extracted from the JSON.
        """
        if json_output.get("status") == "success":
            extracted_text = json_output["data"].get("text", "")
            metadata = json_output["data"].get("metadata", {})

            # Extract relevant information
            title = metadata.get("title", "Unknown Title")
            author = metadata.get("author", "Unknown Author")
            pages = metadata.get("pages", 0)
            keywords = metadata.get("keywords", [])

            # Create a structured output
            processed_data = {
                "extracted_text": extracted_text,
                "title": title,
                "author": author,
                "pages": pages,
                "keywords": keywords,
            }

            self.log(f"Processed data: {processed_data}")
            return processed_data
        else:
            self.log("Failed to process JSON output.")
            return {}
