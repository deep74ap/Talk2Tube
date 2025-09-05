from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_google_genai import ChatGoogleGenerativeAI
from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file")


# Persistent DB directory
PERSIST_DIR = Path(__file__).resolve().parent / "chroma_db"
PERSIST_DIR.mkdir(parents=True, exist_ok=True)


# LLM for translation
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)
#Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)
#Step 1 :  Document Ingestion
def get_transcript_in_english(video_id: str) -> str:
    """
    Fetch transcript for a YouTube video.
    - If English exists, return it.
    - Otherwise, fetch another available language (e.g. Hindi)
      and translate to English using Gemini via LangChain.
    """
    api = YouTubeTranscriptApi()

    try:
        # Step 1: List available transcripts
        available = api.list(video_id)
        langs = [t.language_code for t in available]
        print("Available languages:", langs)

        # Step 2: If English exists, fetch it directly
        if "en" in langs:
            transcript_list = api.fetch(video_id, languages=["en"])
            # print(transcript_list)
            transcript_text = " ".join(chunk.text for chunk in transcript_list)
            return transcript_text

        # Step 3: Otherwise, pick Hindi if available
        if "hi" in langs:
            transcript_list = api.fetch(video_id, languages=["hi"])
            # print(transcript_list)
            transcript_raw = " ".join(chunk.text for chunk in transcript_list)

            # Step 4: Translate with Gemini (LangChain Chat model)
            prompt = f"""
            Translate the following Hindi transcript into English.
            Keep meaning accurate and natural:

            {transcript_raw}
            """
            response = llm.invoke(prompt)
            return response.content

        return "No transcript available in English or Hindi."
    except TranscriptsDisabled:
        return "Captions are disabled for this video."

    except Exception as e:
        return f"An error occurred: {e}"

# video_id = "Gfr50f6ZBvo"


# transcript = get_transcript_in_english(video_id)


#Step 2 : Text Splitting

def make_chunks(transcript):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])
    return chunks

# print(len(chunks))

# print(chunks[100])


#Step 3 : Generating Embeddings
def build_retriever(video_id: str):
    """
    Build or load a retriever for the given YouTube video_id.
    Uses persistent Chroma DB to avoid recomputing embeddings.
    """
    collection_name = f"yt_{video_id}"
    db_path = str(PERSIST_DIR)

    # Try loading existing collection
    db = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory="./chroma_db" 
    )

    if db._collection.count() > 0:
        print(f"✅ Loaded existing retriever for {video_id}")
        return db.as_retriever(search_type="similarity", search_kwargs={"k": 4}), "cached"

    # Otherwise, fetch transcript + build
    print(f"⚡ Building new retriever for {video_id}")
    transcript = get_transcript_in_english(video_id)
    if not transcript or transcript.startswith("❌"):
        raise ValueError(f"Transcript not available: {transcript}")

    chunks = make_chunks(transcript)
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=db_path
    )
    # db.persist()
    print(f"💾 Persisted embeddings for {video_id}")
    return db.as_retriever(search_type="similarity", search_kwargs={"k": 4}), "new"
