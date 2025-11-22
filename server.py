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
    print ('I got clicked!')

    #TODO code
    title, story = main()

    while(story == None):
        pass

    make_page(title=title, story=story, page_num=1)

    return render_template('story.html')



@app.route('/next/')
def next():
    print ('next page')

    make_page()

    return render_template('story.html')


def make_page(title=def_title, story=def_story, page_num=def_num):
    def_title = title
    def_story = story
    def_num = page_num+1

    page = story[page_num]

    with open('templates/story_template.html', 'w+') as file:
        base_page = file.read()

    new_text = page

    new_page = base_page.replace("[text]", new_text)
    new_page = new_page.replace("[title]", title)

    with open('templates/story.html', 'w+') as file:
        file.truncate(0)
        file.write(new_page)



if __name__ == '__main__':
    app.run(debug=True)