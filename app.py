from flask import Flask, request, render_template, send_from_directory
import os
from pydub import AudioSegment
import noisereduce as nr
import tempfile

app = Flask(__name__)

# Folder to store uploaded and processed files
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Route to render the upload form
@app.route('/')
def index():
    return render_template('upload.html')

# Route to handle the uploaded audio, process it, and save the cleaned version
@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio_file' not in request.files:
        return 'No file part', 400

    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return 'No selected file', 400

    # Save the uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    audio_file.save(temp_file.name)
    temp_file_path = temp_file.name

    # Process the audio (noise reduction)
    audio = AudioSegment.from_file(temp_file_path)
    audio_samples = audio.get_array_of_samples()
    cleaned_audio = nr.reduce_noise(y=audio_samples)

    # Save the cleaned audio
    processed_path = os.path.join(PROCESSED_FOLDER, 'processed_audio.wav')
    cleaned_audio.export(processed_path, format='wav')

    # Return the download link for the cleaned file
    return render_template('download.html', processed_file=processed_path)

# Route to allow the user to download the processed audio file
@app.route('/processed_files/<filename>')
def download_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
