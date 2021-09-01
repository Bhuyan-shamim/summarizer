from flask import Flask
import datetime
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

# define a variable to hold you app
app = Flask(__name__)

def get_transcript(video_id):
    #video_id = url.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = ""
    for i in transcript:
        transcript_text += ' ' + i['text']
    summarizer = pipeline('summarization')
    num_iters = int(len(transcript_text)/1000)
    print(num_iters)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        out = summarizer(transcript_text[start:end])
        out = out[0]
        out = out['summary_text']
        print( "start time ", str(datetime.datetime.now()))
        print(i, out)
        print( "end time ", str(datetime.datetime.now()))
        summarized_text.append(out)
    print(summarized_text)
    return transcript_text


# define your resource endpoints
@app.route('/')
def index_page():
    print("Home")
    return "<h1>Hello world</h1>"

@app.route('/api/get_summary/<url>', methods=['GET'])
def get_summary(url):
    transcript_text = get_transcript(url)
    return transcript_text

# server the app when this file is run
if __name__ == '__main__':
    app.run(debug= True)