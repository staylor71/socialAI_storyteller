import threading
from flask import Flask, jsonify, render_template, request
from helpers import *
import sounddevice as sd
from scipy.io.wavfile import write as wr
import speech_recognition as sr



app = Flask(__name__)


PAGE_NUM = 1
PROMPT = ""
EDIT_PROMPT = ""
recording_state = {"status": "stopped"}


###################################################################
#                                                                 #
#                            HOME PAGE                            #
#                                                                 #
###################################################################

@app.route('/', methods = ["GET", "POST"])
def home():
    print("[RENDERER] home page rendered")

    if request.method == "POST":
        topics = request.form.get("negative_topics")
        level = request.form.get("level")
        rating = request.form.get("rating")
        length = request.form.get("length")
        
        edit_parental_settings(topics, level, rating, length)
    

    return render_template('home.html')


@app.route('/generating/', methods=["GET", "POST"])
def generate_prompt():
    print("[RENDERER] waiting page rendered")

    # global PROMPT

    # if request.method == "POST":
    #    # getting input with name = fname in HTML form
    #    user_text_input = request.form.get("userinput")
    # else:
    #     user_text_input = "Tell me a story"

    # PROMPT = user_text_input

    return render_template('waiting.html')


@app.route('/write')
def write():
    print("[INFO] writing story")
    
    global PROMPT

    filename = "16-122828-0002.wav"

    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        PROMPT = r.recognize_google(audio_data) # WORKS - NO ERRORORRORORR VSCODE IS MALDING
        
        print(f"[INFO] audio retrieved as - '{PROMPT}'")


    write_story(PROMPT)

    return "doneso!"


@app.route('/tell-story/')
def tell_story():
    print("[RENDERER] story page 1 rendered")

    global PAGE_NUM

    PAGE_NUM = 0

    edit_story_html(PAGE_NUM)

    return render_template('story.html')


###################################################################
#                                                                 #
#                            STORY PAGE                           #
#                                                                 #
###################################################################

@app.route('/next/')
def next():
    print ('[RENDERER] next page')
    global PAGE_NUM

    PAGE_NUM = PAGE_NUM + 1

    edit_story_html(PAGE_NUM)

    return render_template('story.html')


@app.route('/prev/')
def prev():
    print ('[RENDERER] prev page')
    global PAGE_NUM

    PAGE_NUM = PAGE_NUM - 1

    edit_story_html(PAGE_NUM)

    return render_template('story.html')


@app.route('/talk/', methods=['GET', 'POST'])
def edit_story():
    print('[RENDERER] Loading page rendered')
    global EDIT_PROMPT

    if request.method == 'POST':
        user_input_prompt = request.form.get('input')
    else: 
        user_input_prompt = ""

    EDIT_PROMPT = user_input_prompt

    return render_template('loading.html')


@app.route('/edit/')
def talk():
    print("[INFO] Editing story")
    global PAGE_NUM, EDIT_PROMPT

    interrupt_story(EDIT_PROMPT, PAGE_NUM)

    return "doneso!"


###################################################################
#                                                                 #
#                          SETTINGS PAGE                          #
#                                                                 #
###################################################################
@app.route('/settings/')
def settings():
    open_settings_html()

    return render_template("settings.html")

# ============================
# 🔹 Audio & Recording
# ============================
@app.route("/toggle_recording", methods=["GET"])
def toggle_recording():
    recording_state["status"] = "started" if recording_state["status"] == "stopped" else "stopped"
    print(f"[INFO] Recording status changed to: {recording_state['status']}")

    if recording_state["status"] == "started":

        threading.Thread(target=record).start()
        return "working"

    else:
        print("stopped?")
        sd.stop()
        
        return render_template('waiting.html')


def record():
    freq = 44100
    duration = 10

    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

    sd.wait()

    wr("prompt.wav", freq, recording)



@app.route("/get_recording_state", methods=["GET"])
def get_recording_state():
    return jsonify(recording_state)

# @app.route('/receive_audio', methods=['POST'])
# def receive_audio():
#     file_path = request.json.get("file_path")
#     if file_path:
#         print(f"[INFO] Audio file ready at: {file_path}")
#         threading.Thread(target=transfer_file_from_robot).start()
#         return jsonify({"status": "Audio transfer started"}), 200
#     return jsonify({"error": "No file path provided."}), 400

@app.route('/download/', methods=['GET', 'POST'])
def uploadAudio():

    # Get params
    freq = 44100

    # Recording duration
    duration = 5

    # Start recorder with the given values 
    # of duration and sample frequency
    recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=2)

    # Record audio for the given number of seconds
    sd.wait()

    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    wr("recording0.wav", freq, recording)

    return "done"
  


if __name__ == '__main__':
    app.run(debug=True)