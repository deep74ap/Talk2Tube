# ragAugmentation.py
from langchain_core.prompts import PromptTemplate

# Prompt template object (not a function)


final_prompt = PromptTemplate(
    template="""
    You are an expert assistant.
    Use ONLY the transcript context below to answer the question.
    
    - Always answer directly and confidently.
    - Never say "based on the context" or "according to the transcript".
    - If the context is truly empty, then say: "I don't know."
    - If the context is partial, still try to give the best possible answer.

    Context:
    {context}

    Question: {question}

    Answer:
    """,
    input_variables=["context", "question"]
)


# Format docs into a single context string
def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)
