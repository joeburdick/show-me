from openai import OpenAI

def transcribe(filePath: str):
    client = OpenAI()

    audio_file = open(filePath, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

print(transcribe("./src/show_me/speech_input/test.wav"))
