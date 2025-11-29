from flask import Flask, render_template
from helpers import edit_story_html, write_story, interrupt_story
app = Flask(__name__)


PAGE_NUM = 1

###################################################################
#                                                                 #
#                            HOME PAGE                            #
#                                                                 #
###################################################################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tell-story/')
def tell_story():
    global PAGE_NUM

    print ('[INFO] Listening...')

    #TODO add audio listener
    prompt = "Tell me a story"

    write_story(prompt)

    PAGE_NUM = 1

    edit_story_html(PAGE_NUM)

    return render_template('story.html')


###################################################################
#                                                                 #
#                            STORY PAGE                           #
#                                                                 #
###################################################################

@app.route('/next/')
def next():
    print ('[INFO] next page')
    global PAGE_NUM

    PAGE_NUM = PAGE_NUM + 1

    edit_story_html(PAGE_NUM)

    return render_template('story.html')


@app.route('/prev/')
def prev():
    print ('[INFO] prev page')
    global PAGE_NUM

    PAGE_NUM = PAGE_NUM - 1

    edit_story_html(PAGE_NUM)

    return render_template('story.html')


@app.route('/talk/')
def talk():
    print("[INFO] Editing story")
    global PAGE_NUM

    #TODO audio input
    prompt = "Add zilly, the wizard with a perm, into the story"

    interrupt_story(prompt, PAGE_NUM)

    return next()


###################################################################
#                                                                 #
#                          SETTINGS PAGE                          #
#                                                                 #
###################################################################
@app.route('/settings/')
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    app.run(debug=True)