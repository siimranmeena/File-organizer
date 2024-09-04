from flask import Flask, request, jsonify
import os
import shutil
from datetime import datetime

app = Flask(__name__)

# Set up the directory where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to write logs
def write_log(message):
    with open('file_organizer_log.txt', 'a') as log:
        log.write(f"{datetime.now()}: {message}\n")

# Function to organize files
def organize_files(directory):
    try:
        # Create or clear the log file
        open('file_organizer_log.txt', 'w').close()
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                file_extension = filename.split('.')[-1]
                
                if file_extension == filename:  # No extension found
                    file_extension = 'No_Extension'
                
                # Create a folder for the file extension if it doesn't exist
                folder = os.path.join(directory, file_extension)
                if not os.path.exists(folder):
                    os.makedirs(folder)
                
                # Move the file to the appropriate folder
                new_file_path = os.path.join(folder, filename)
                shutil.move(file_path, new_file_path)
                
                # Write to the log file
                write_log(f"Moved '{filename}' to '{folder}'")
    
    except Exception as e:
        write_log(f"Error: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('directory')
        for file in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
        organize_files(UPLOAD_FOLDER)
        return "File organization complete. Check 'file_organizer_log.txt' for details."
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
