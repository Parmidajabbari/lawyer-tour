from flask import Flask, request, redirect, render_template, send_from_directory
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'storage'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '<h2>Upload your 360° image via POST /upload</h2>'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return '''
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">Upload</button>
        </form>
        '''
    file = request.files['image']
    if not file:
        return 'No image uploaded', 400
    unique_id = str(uuid.uuid4())[:8]
    filename = f"{unique_id}.jpg"
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(f"/view?id={unique_id}")

@app.route('/view')
def view():
    image_id = request.args.get("id")
    if not image_id:
        return "Missing ID", 400
    return render_template("view.html", image_id=image_id)

@app.route('/file/<filename>')
def file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
