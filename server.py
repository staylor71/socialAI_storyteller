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
async def my_link():
    print ('I got clicked!')

    #TODO code

    return render_template('story.html')



@app.route('/next/')
def next():
    print ('next page')


    return render_template('story.html')



if __name__ == '__main__':
    app.run(debug=True)