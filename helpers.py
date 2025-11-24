import json
import pyttsx3
tts = pyttsx3.init()
from openai import OpenAI

# Project path
PATH = "project/socialAI_storyteller/"

# Get API key and client
with open("key.json", 'r') as file:
    data = json.load(file)
    client = OpenAI(api_key=data["api_key"])


###################################################################
#                                                                 #
#                          AI INTERACTION                         #
#                                                                 #
###################################################################

def magic_box(convo, temp=0.7, tokens=1200, top=0.9, frequency=0, presence=0):
        
    # Create GPT response
    GeneratedResponse = client.chat.completions.create(
        model="gpt-4o-mini",            # testing mini, could swap to turbo
        messages=convo,
        temperature=temp,               # Controls the randomness of the output (0.0 to 2.0) 0 more focused and deterministic, 2 increase creativity and randomness.]
        max_tokens=tokens,              # Limits the length of the generated output.
        top_p=top,                      # Nucleus sampling: Controls the diversity of the output by considering only the most probable token options.
                                        # (0-1); (Focus on the top few most likely tokens, Allow more diverse token choices)
        frequency_penalty=frequency,    # Discourages repetition of words or phrases. (-2.0, 2.0.) -- (Encourage repetition, Reduce repetition)
        presence_penalty=presence       # Encourages or discourages introducing new topics or ideas. (-2.0, 2.0) --  (focused discussions, brainstorming or creative tasks)
        # seed=42                       # Ensures reproducibility of outputs by initializing the random number generator with a fixed value (unavailable <-- temperature, top_p).
    )

    AgentResponse = GeneratedResponse.choices[0].message.content
    return AgentResponse


def read_story(story, convo):

    # Save the story to a file titled by name
    title_start = story.find("**")+2
    title_end = story[title_start:].find("**")
    title = story[title_start:title_end]

    with open(PATH+"Stories/"+title+".txt", 'w+') as file:
        file.write(story[title_end:])


    # Split content into pages based on returns
    pages = story.split('\n\n')

    for i, page in enumerate(pages):

        # Output the current page
        # TODO make it say this as the story
        
        print(page)
        tts.say(page)
        tts.runAndWait()
        tts.stop()

        # Ask for input or to continue
        user_input = input("Press ENTER to continue")

        # Check if input given
        if user_input != None and not user_input.isspace() and len(user_input) > 2:

            # Edit prompt to adhere to guidelines
            edited_prompt = interrupt_prompt(user_input)
            
            # Set up the conversation so far
            convo.append({"role" : "assistant", "content" : "\n\n".join(pages[:i+1])})
            convo.append({"role" : "user", "content" : edited_prompt})


            #TODO make it say this in separate voice
            print(f'Alright, I hear you and will edit the story with your request of "{user_input}".')
            

            # Get GPT ressponse
            response = magic_box(convo)

            # Read the reply recurrsively
            read_story(response, convo)
            break
        
      
###################################################################
#                                                                 #
#                        PROMPT ENGINEERING                       #
#                                                                 #
###################################################################


def generate_prompt(user_input):

    # Grab parental settings
    with open("parental_controls.json", 'r') as file:
        data = json.load(file)
        topics_to_avoid = data['topics_to_avoid']
        rating = data["rating"]
        word_count = data['word_count']
        reading_level = data['reading_level']

    # Create the guidelines for the AI
    guidelines = f"Write it as a {word_count}-word {rating}-rated kids bedtime story with a happy ending for a {reading_level} reading level. Avoid {topics_to_avoid}."

    # Add guidelines to the prompt
    full_prompt = f"{user_input}\n{guidelines}"

    return (full_prompt)


def interrupt_prompt(user_input):

    # Grab parental settings
    with open("parental_controls.json", 'r') as file:
        data = json.load(file)
        topics_to_avoid = data['topics_to_avoid']
        rating = data["rating"]
        word_count = data['word_count']
        reading_level = data['reading_level']

    # Craft full prompt
    full_prompt = f"Continue the previous {rating}-rated kids bedtime story, but {user_input}. Avoid {topics_to_avoid}."

    return (full_prompt)