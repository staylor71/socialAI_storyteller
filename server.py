from flask import Flask, render_template
from main import main
from helpers import edit_story_html
app = Flask(__name__)


PAGE_NUM = 1


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tell-story/')
def my_link():
    global PAGE_NUM

    print ('[INFO] Listening...')

    #TODO add audio listener
    title, story = main()
    PAGE_NUM = 1

    edit_story_html(PAGE_NUM)

    return render_template('story.html')


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






if __name__ == '__main__':
    app.run(debug=True)