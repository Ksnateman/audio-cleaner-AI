from flask import Flask, render_template, request, send_file
import os
from pydub import AudioSegment
import tempfile

app = Flask(__name__)

# Create the necessary directories for uploaded and processed files
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Configuring the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')  # Render the upload page

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio_file' not in request.files:
        return "No file part", 400
    
    audio_file = request.files['audio_file']
    
    if audio_file.filename == '':
        return "No selected file", 400
    
    if audio_file:
        # Save the uploaded file to the uploads folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(file_path)

        # Now process the audio (this is where the magic happens, like noise removal, enhancement)
        processed_audio_path = process_audio_file(file_path)

        # Render the download page and pass the processed file's path
        return render_template('download.html', filename=processed_audio_path)

def process_audio_file(file_path):
    """Process the uploaded audio file and save the cleaned file."""
    try:
        # Open the uploaded audio file using PyDub
        audio = AudioSegment.from_file(file_path)

        # Here you can add audio processing (like noise removal, volume enhancement, etc.)
        # For this example, let's just export the same file with no changes (you can add more processing here)
        processed_file_path = os.path.join(PROCESSED_FOLDER, 'processed_audio.wav')
        
        # Export the audio as a WAV file (you can also change the format to mp3, etc.)
        audio.export(processed_file_path, format="wav")

        return processed_file_path
    except Exception as e:
        return f"An error occurred during audio processing: {str(e)}"

@app.route('/download/<filename>')
def download_file(filename):
    """Allow the user to download the processed audio file."""
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
