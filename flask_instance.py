from flask import Flask, request, render_template
import sys
import transcriber

app = Flask(__name__, template_folder='.')

def get_transcription(word: str) -> str:
    """
    Obtiene la transcripción fonológica de la palabra indicada
    """
    return transcriber.transcriber(word)

@app.route('/healtCheck')
def index():
    return "true"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    
    if 'word' in request.form:
        word = request.form['word']
        transcription_result = get_transcription(word)
        return render_template('index.html', transcriptionResult=transcription_result)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    debug = 'debug' in sys.argv
    app.run(debug=debug)
