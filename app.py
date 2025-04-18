from flask import Flask, request, send_from_directory
import os
from process_audio import process_full_audio

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "🔥 AI Audio Cleaner is live!"

@app.route('/clean-audio', methods=['POST'])
def clean_audio():
    file = request.files['audio']
    filename = file.filename
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, 'cleaned_output.wav')

    file.save(input_path)
    process_full_audio(input_path, output_path)

    return send_from_directory(OUTPUT_FOLDER, 'cleaned_output.wav', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
