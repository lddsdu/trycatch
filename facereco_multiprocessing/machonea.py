#-*- coding:utf-8 -*-

import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import requests
import cStringIO
from cStringIO import StringIO
import Image
UPLOAD_FOLDER = 'c:\uploads_1'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
else:
    pass
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        upload_files = request.files.getlist('file[]')
        filenames = []
        for file in upload_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #使用StringIO时，请注释掉此行,因为我不需要保存图片在此服务器上。
                filenames.append(filename)

                data = {'file[]': open(os.path.join(app.config['UPLOAD_FOLDER'],filename), 'rb')}

                #buf = cStringIO.StringIO(file)
                #buf.seek(0)
                #buf_img = buf.read()
                #data = {'file[]': files=buf_img}
                r = requests.post('http://127.0.0.1:5000/',files=data)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file multiple="" name="file[]">
         <input type=submit value=Upload>
    </form>
    '''
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
