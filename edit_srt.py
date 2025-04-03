from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'transcript'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'srt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return redirect(url_for('edit_file', filename=filename))

    # Get list of existing SRT files
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.srt')]
    return render_template('upload.html', files=files)

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if request.method == 'POST':
        content = request.form['content'].strip()
        content = '\n'.join([line.strip() for line in content.splitlines() if line.strip()])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content + '\n')
        return redirect(url_for('upload_file'))

    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    return render_template('edit.html', filename=filename, content=content)

if __name__ == '__main__':
    app.run(debug=True)
