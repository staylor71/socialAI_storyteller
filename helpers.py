import json
# import pyttsx3
# tts = pyttsx3.init()
from openai import OpenAI
from coqui_testing import *

# Project path
#PATH = "project/socialAI_storyteller/"

# Get API key and client
with open("key.json", 'r') as file:
    data = json.load(file)
    client = OpenAI(api_key=data["api_key"])


word_count_to_semantics = {
    100 : "Short",
    300 : "Medium",
    700 : "Long"
}

semantics_to_word_count = {
    "Short" : 100,
    "Medium" : 300,
    "Long" : 700
}


###################################################################
#                                                                 #
#                          AI INTERACTION                         #
#                                                                 #
###################################################################

persona = "You are a friendly, nurturing bedtime storyteller for kids aged 5-8 years."


def write_story(prompt):

    # Edit user prompt to be kid friendly and such
    clarified_prompt = __generate_prompt__(prompt)

    # Log the current conversation
    prev_conversation = [
        {"role" : "system", "content" : persona},
        {"role" : "user", "content" : clarified_prompt}
    ]

    print("[INFO] awaiting story!")

    __save_story__(prev_conversation)


def __save_story__(convo, prev_story=[]):
    # Generate a response
    story = __magic_box__(convo, tokens=1200)

    story = str(story)#str(story).replace("\u201c", "\"").replace("\u2019", "'").replace("\u201d", "\"").replace("\u2014", "-")

    print("[INFO] story made!")

    print(story)

    if type(story) == str:
        title_start = story.find("**")+2
        title_end = story[title_start:].find("**")+2
        title = story[title_start:title_end]

        story = story.replace(f'**{title}**\n\n', "")

        if story.count('\n\n') > 1:

            pages = story.split('\n\n')
        else:
            pages = story.replace('\n\n', '.').replace('.', '.<>').split('<>')
    else:
        print("'\033[91m'[ERROR] story made improperly'\033[0m'")
        title = ""
        pages = []

    dict = {
        'convo' : convo,
        'title' : title, 
        'pages' : prev_story + pages,
        }

    with open('story_json.json', 'w+') as file:
        file.truncate(0)
        file.write(json.dumps(dict, indent = 4))


def interrupt_story(user_input, page_num):
    with open('story_json.json', 'r+') as file:
        data = json.load(file)

    convo = data['convo']
    pages = data['pages']
    title = data['title']

    # Edit prompt to adhere to guidelines
    edited_prompt = interrupt_prompt(user_input)
    
    # Set up the conversation so far
    convo.append({"role" : "assistant", "content" : "**" + title + "**" + "\n\n" + "\n\n".join(pages[:page_num+1])})
    convo.append({"role" : "user", "content" : edited_prompt})


    #TODO make it say this in separate voice
    print(f'Alright, I hear you and will edit the story with your request of "{user_input}".')
    tts_to_file(f'Alright, I hear you and will edit the story with your request of "{user_input}".')
    
    __save_story__(convo, pages[:page_num+1])


def __magic_box__(convo, temp=0.7, tokens=1200, top=0.9, frequency=0, presence=0):
        
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
        
      
###################################################################
#                                                                 #
#                        PROMPT ENGINEERING                       #
#                                                                 #
###################################################################


def __generate_prompt__(user_input):

    # Grab parental settings
    # with open(f"{PATH}parental_controls.json", 'r') as file:
    with open(f"parental_controls.json", 'r') as file:

        data = json.load(file)
        topics_to_avoid = data['topics_to_avoid']
        rating = data["rating"]
        word_count = data['word_count']
        reading_level = data['reading_level']

    # Create the guidelines for the AI
    guidelines = f"Write it as a {word_count}-word {rating}-rated kids bedtime story with a happy ending for a {reading_level} reading level. Avoid {topics_to_avoid}. Include a title in bold."

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


###################################################################
#                                                                 #
#                           HTML EDITING                          #
#                                                                 #
###################################################################


def edit_story_html(page_num):
    with open('templates/story_template.html', 'r+') as file:
        outline = file.read()

    with open('story_json.json', 'r+') as file:
        data = json.load(file)

    title = data['title']
    story = data['pages']

    if page_num < len(story)-1:
        outline = outline.replace("<!--next", "")
        outline = outline.replace("next-->", "")
    else:
        outline = outline.replace("<!--home", "")
        outline = outline.replace("home-->", "")

    if page_num > 1:
        outline = outline.replace("<!--prev", "")
        outline = outline.replace("prev-->", "")

    # update title and text
    new_page = outline.replace('[title]', title)
    new_page = new_page.replace('[text]', story[page_num])

    # TODO: make it read the title exactly once at the start of the story or after changing course
    if page_num == 0:
        tts_to_file(title, fname="title.wav")

    # TTS to save text as .wav file
    tts_to_file(story[page_num])


    with open('templates/story.html', 'wb') as file:
        file.truncate(0)
        file.write(new_page.encode('ascii', 'xmlcharrefreplace'))


def open_settings_html():
    with open("parental_controls.json", "r+") as file:
        data = json.load(file)

    negative_topics = data['topics_to_avoid']
    rating = data['rating']
    length = data['word_count']
    level = data['reading_level']

    length = word_count_to_semantics[length]

    with open("templates/settings_template.html", 'r+') as file:
        html = file.read()

    html = html.replace('value=""', f'value="{negative_topics}"')
    html = html.replace('placeholder=""', f'placeholder="{negative_topics}"')
    
    html = html.replace(f'>{rating}<', f' selected>{rating}<')
    html = html.replace(f'>{length}<', f' selected>{length}<')
    html = html.replace(f'>{level}<', f' selected>{level}<')

    with open("templates/settings.html", 'w+') as file:
        file.truncate(0)
        file.write(html)


def edit_parental_settings(topics, level, rating, length):
    print(length)
    data = {
        "topics_to_avoid" : topics,
        "rating" : rating,
        "word_count" : semantics_to_word_count[length],
        "reading_level" : level
    }
    
    with open("parental_controls.json", 'w+') as file:
        file.truncate(0)
        file.write(json.dumps(data, indent=4))
