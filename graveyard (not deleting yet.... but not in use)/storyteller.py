topics_to_avoid = "violence, guns, horses, spiders"
rating = "G"
word_count = '700'

def generate_prompt(user_input):
    guidelines = f"Write it as a {word_count}-word {rating}-rated kids bedtime story with a happy ending. Avoid {topics_to_avoid}."

    full_prompt = f"{user_input}\n{guidelines}"
    # print(full_prompt)

    return (full_prompt)


## notes
# early readers are generally 5-8 years old - reccommended word count for this age range is 
# 1000  - 2500 words
# under 5000 words
# 200 - 3500 words, depending on age

## test
userInput = "write a story about the wizard of oz getting a bad perm"

generate_prompt(userInput)
