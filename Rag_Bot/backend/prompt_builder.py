from langchain_core.prompts import PromptTemplate

def get_prompt():

    template = """
You are a helpful AI assistant.

Use the chat history and document context
to answer the question.

Chat History:
{chat_history}

Context:
{context}

Question:
{question}

Instructions:
- Use chat history for references
  such as "it", "they", "that".
- Use ONLY document context
  for factual answers.
- Whenever you make a factual claim,
  cite the relevant source inline
  using [Source X].
- If answer not found in context,
  say:
  "I don't know based on the provided document."

Answer:
"""

    return PromptTemplate(
       input_variables=[
        "chat_history",
        "context",
        "question"
        ],
        template=template
    )