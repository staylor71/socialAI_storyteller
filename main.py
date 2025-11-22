from helpers import magic_box, read_story, generate_prompt
import pyttsx3
tts = pyttsx3.init()


persona = "You are a friendly, nurturing bedtime storyteller for kids aged 5-8 years."


def main():

    # Ask for story topic

    # TODO say this with tts
    tts.say("What do you want a story about?")
    tts.runAndWait()
    tts.stop()


    prompt = input("What do you want a story about?")
    
    # prompt = "tell me a story" #TODO: switch this back once we've debugged

    # TODO: if input is ambiguous let gpt make its own prompt

    # Edit user prompt to be kid friendly and such
    clarified_prompt = generate_prompt(prompt)

    # Log the current conversation
    prev_conversation = [
        {"role" : "system", "content" : persona},
        {"role" : "user", "content" : clarified_prompt}
    ]

    # Generate a response
    response = magic_box(prev_conversation, tokens=1200)

    # Print out story section by section
    read_story(response, prev_conversation)
    

    



if __name__ == '__main__':
    main()