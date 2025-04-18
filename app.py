from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Increase file upload size (if you haven't already)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024  # 1 GB limit

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to display the upload form
@app.route('/')
def index():
    return render_template('upload.html')

# Route to handle file uploads
@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        if 'audio_file' not in request.files:
            raise ValueError("No file part")
        
        file = request.files['audio_file']
        
        if file.filename == '':
            raise ValueError("No selected file")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            app.logger.info(f"File saved successfully at {file_path}")
            
            # Process the audio file here (add your audio processing logic)
            app.logger.info(f"Processing file: {filename}")
            
            return render_template('download.html', filename=filename)
        
        else:
            raise ValueError("Invalid file type")
    
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return f"Error: {str(e)}", 500

# Route to serve the processed file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)  # Ensure debug=True is set
