# ragGeneration.py
from .ragIndexing import build_retriever
from .ragAugmentation import final_prompt, format_docs
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()


# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file")

# Load LLM with explicit API key
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)

def get_answer(video_id: str, question: str) -> str:
    """Retrieve transcript, augment context, and generate an answer."""
    retriever,status = build_retriever(video_id)
    print(f"📂 Retriever status for {video_id}: {status}")
    # Parallel chain: gather context + pass question
    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    # Full pipeline
    parser = StrOutputParser()
    main_chain = parallel_chain | final_prompt | llm | parser

      # --- Debugging ---
    retrieved_docs = retriever.invoke(question)
    print("\n🔍 Retrieved Docs Count:", len(retrieved_docs))
    for i, doc in enumerate(retrieved_docs[:2]):  # show first 2 docs
        print(f"\nDoc {i+1}:\n", doc.page_content[:300], "...\n")



    return main_chain.invoke(question)


# Example standalone run
# print(get_answer("Gfr50f6ZBvo", "What is this video about?"))
