from flask import Flask, render_template
from main import main
app = Flask(__name__)


def_title = "" 
def_story = []
def_num = 1


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tell-story/')
def my_link():
    print ('[INFO] Listening...')

    #TODO add audio listener
    title, story = main()

    with open('templates/story_template.html', 'r+') as file:
        outline = file.read()

    new_page = outline.replace('[title]', title)
    new_page = new_page.replace('[story]', story[1])

    with open('templates/story.html', 'w+') as file:
        file.truncate(0)
        file.write(new_page)

    return render_template('story.html')



@app.route('/next/')
def next():
    print ('next page')


    return render_template('story.html')



if __name__ == '__main__':
    app.run(debug=True)