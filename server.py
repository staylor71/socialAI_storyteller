from flask import Flask, render_template, request
from helpers import *
app = Flask(__name__)


PAGE_NUM = 1

###################################################################
#                                                                 #
#                            HOME PAGE                            #
#                                                                 #
###################################################################

@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        topics = request.form.get("negative_topics")
        level = request.form.get("level")
        rating = request.form.get("rating")
        length = request.form.get("length")
        
        edit_parental_settings(topics, level, rating, length)
    

    return render_template('home.html')

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       user_text_input = request.form.get("userinput")
    #    return user_text_input # didnt like having 2 return statements (why was this in the example)
    return render_template("home.html")


@app.route('/tell-story/')
def tell_story():
    global PAGE_NUM



    print ('[INFO] Listening...')

    #TODO add audio listener
    try: prompt = ""# user_text_input
    except : prompt = "Tell me a story"

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
    open_settings_html()

    return render_template("settings.html")


if __name__ == '__main__':
    app.run(debug=True)