from llama_cpp import Llama

PROMPT_TEMPLATE = """[INST] Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not use `WHERE EXISTS` clause to check the existence of a property because Kùzu database has a fixed schema.
Do not omit relationship pattern. Always use `()-[]->()` instead of `()->()`.
Do not include any text except the generated Cypher statement.
Do not use `WITH` clause for aggregates

The question is:
{question} [/INST]
"""

class LlmEngine():
    def __init__(self, file_name: str) -> None:
        self.llm = Llama(
            model_path=file_name,
            n_gpu_layers=10,
        )

    def generate_cypher_statement(self, schema: str, question: str) -> str | None:
        prompt = PROMPT_TEMPLATE.format(schema=schema, question=question)
       
        output = self.llm(
            prompt,
            max_tokens=None,
            stop=None,
            echo=False,
            temperature=0,
        )

        if output["choices"]:
            query = bytes(output["choices"][0]["text"], "utf-8").decode("unicode_escape").replace('`', '')
            return query

        return None