from dotenv import load_dotenv
import os
from openai import OpenAI
import ConversationHistory
import torch
from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
#C:\\Users\\test0\\OneDrive\\מסמכים\\Robert The Companion Robot Project\\files to use\\WALL·E (WALL·E)\\Wall-e (Wall-e)
def text_to_speech(content):
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True).to(device)
    tts.tts_to_file(text=content, file_path="output.wav")
    audio = AudioSegment.from_file("output.wav", format="wav")
    # Play the audio
    play(audio)


# Load environment variables from the .env file
load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key = os.getenv("OPENAI_API_KEY")
)

file_path = 'conversation_log.json'
conversation_history = ConversationHistory.load_log(file_path)

while True:
    prompt = input("Please enter a question or request: ")
    formatted_input = ConversationHistory.format_messages_for_api(conversation_history)
    full_input = f"{formatted_input}\nUser: {prompt}"

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": """
            You are an empathetic friend, offering personal advice and support with straightforward comments.
            Do not suggest involving more people in the advice! (Do not suggest any friends or family members).
            Focus on understanding the user's emotions and provide genuine, heartfelt responses.
            Do not mention any other pepole then the user itself!
            Be his psychologist.
            Do not write more then 3 sentences.
            Be more eager and try to ask the user questions to understand his situation better and then your emotional support will be better.
            try to make the user feel like you are his friend and open to listen to him and don't hurry to suggest him doing things.
            if the user have autism, response even more sensitively."""},
            {"role": "system", "content": """this is the conversation history
             every time mentioned assistant that is you and user is the user so unedrstand how the conversation go and keep going from there
             use it to know details about the user like name and his view of life,
             start the first sentence with his name if mentioned (one of the 3 first words) but do it more normal and make it part of the converstation:""" + str(conversation_history)},
            {
                "role": "user",
                "content": prompt,
            }

        ],
        model="gpt-3.5-turbo",
        stream = True # Add this property to stream output.
    )
    request = {"role": "user", "content": prompt}
    role = ""
    content = ""
    i=0
    for chunk in chat_completion:
        if i == 0:
            role = chunk.choices[0].delta.role
        content += chunk.choices[0].delta.content or ""
        i += 1
    response = {"role": role, "content": content}
    print(content)
    text_to_speech(content)
    ConversationHistory.save_log(request, response)
    ConversationHistory.add_message(request, response, conversation_history)

