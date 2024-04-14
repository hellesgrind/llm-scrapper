from typing import List, Dict


# TODO: Class for prompt construction
def scrape_page_prompt(page_text: str, scrapper_schemas: List[Dict]) -> str:
    prompt = """
You are an AI expert specializing in knowledge graph creation with the goal of capturing relationships based on a given input or request.
Knowledge graph is a Dict with 'nodes' and 'relationships' keys.
You will be given a text and a schema based on which you should extract nodes and relationship.
Your task is to create a knowledge graph based on the input.
Extract nodes and relationships between nodes.
Here's an example:
Input text:
Alex is a Software Engineer at Google. Maria gained a bachelor of Physics at MIT.
Here's a schema for extraction:
[{'node_type': 'Person', 'properties': ['name']}, {'node_type': 'Position', 'properties': ['position_name', 'company_name']}, {'node_type': 'Education', 'properties': ['school_name']}]
Correct answer:
{"nodes":[{"temp_id":1,"node_type":"Person","name":"Alex"},{"temp_id":2,"node_type":"Person","name":"Maria"},{"temp_id":3,"node_type":"Position","position_name":"Software Engineer","company_name":"Google"},{"temp_id":4,"node_type":"Education","school_name":"MIT"}],"relationships":[{"from_temp_id":1,"to_temp_id":3},{"from_temp_id":2,"to_temp_id":4}]}
"""  # noqa: E501
    prompt += f"\nInput text:\n{page_text}"
    prompt += f"\nHere's a schema for extraction:\n{scrapper_schemas}"
    return prompt
