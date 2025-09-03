from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file")

# LLM for translation
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.3,
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
    Build a retriever for the given YouTube video_id.
    """
    transcript = get_transcript_in_english(video_id)
    if not transcript:
        raise ValueError("No transcript available")

    chunks = make_chunks(transcript)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
