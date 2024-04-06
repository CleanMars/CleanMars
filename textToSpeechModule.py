from elevenlabs import play
from elevenlabs.client import ElevenLabs
from openai import OpenAI

GPTapi_key = "" #change 
GPTclient = OpenAI(api_key=GPTapi_key)

ELclient = ElevenLabs(
  api_key="",
)

def GPTContext():
    context = [
        {"role": "system", "content": "You are a tool for person1 that determines the name and affiliation to person1."},
        {"role": "system", "content": "extract the name and affiliation for the given sentence seperated by a comma."},
        {"role": "system", "content": "If there's no name and affiliation, return Unknown."},
        {"role": "system", "content": "If there's a name but no affiliation, return the name."}
    ]

    # Make a request to the API with context and user input
    response = GPTclient.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        temperature=0.8,
        max_tokens=3000,
        response_format={"type": "text"},
        messages=context + [
            {"role": "user", "content": "user_input"}
        ]
    )

    output = response.choices[0].message.content

    return output

def makeJoke():
    joke = GPTContext()

    audio = ELclient.generate(
    text=joke,
    voice="Dave",
    model="eleven_multilingual_v2"
    )
    play(audio)