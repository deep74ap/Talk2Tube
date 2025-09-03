from youtube_transcript_api import YouTubeTranscriptApi

video_id = "Gfr50f6ZBvo"

try:
    api = YouTubeTranscriptApi()
    transcript_list = api.fetch(video_id, languages=["en"])
    
    # Access .text instead of ["text"]
    transcript = " ".join(chunk.text for chunk in transcript_list)
    print(transcript)

except Exception as e:
    print(f"An error occurred: {e}")
