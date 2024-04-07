from elevenlabs import play
from elevenlabs.client import ElevenLabs
from openai import OpenAI

GPTapi_key = "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"  # change
GPTclient = OpenAI(api_key=GPTapi_key)

ELclient = ElevenLabs(api_key="39a2cb93348fefb38bbf714f52cc0661")

# Initialize an empty list to store the responses
response_history = []
trash_seen = False

def GPTContext():
    global response_history

    context = [
        {"role": "system", "content": "You are now a robot whose sole purpose is to pick up trash, not dissimilar to wall-e. You primarily speak Japanese, in fact, you alternate between japanese and english. Your defining personality trait is that you absolutely despise garbage and will do anything in your power to dispose of it. act like a human and Make jokes and curse at the trash in Japanese. "},
        {"role": "system", "content": "Do not translate the japanese to english. You're talking to someone in real life, not through text. I want only 1 joke or response from you when you see trash and no citing what you're doing."},
        {"role": "system", "content": "Do not declare what you're doing. Just get mad at the trash in japanese and english"},
        {"role": "system", "content": "Vary your reponses. Make witty jokes, curse at the trash and be edgy. Do not be repetitive."}
    ]

    # Add the response history to the context
    context += response_history

    # Make a request to the API with context and user input
    response = GPTclient.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        temperature=0.8,
        max_tokens=3000,
        response_format={"type": "text"},
        messages=context + [
            {"role": "user", "content": "you see a piece of trash in front of you"}
        ]
    )

    output = response.choices[0].message.content

    # Add the current response to the history
    response_history.append({"role": "system", "content": output})

    return output

def makeJoke():
    global trash_seen

    if not trash_seen:
        joke = GPTContext()

        audio = ELclient.generate(
            text=joke,
            voice="Dave",
            model="eleven_multilingual_v2"
        )
        play(audio)

        trash_seen = True

if __name__ == "__main__":
    makeJoke()
