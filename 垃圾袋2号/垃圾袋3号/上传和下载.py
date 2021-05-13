from flask import redirect, url_for
from werkzeug.utils import secure_filename  # 使用这个是为了确保filename是安全的
from os import path

from flask import Flask, render_template, request
from flask import send_from_directory
import os

app = Flask(__name__)


# 用于测试的模板
@app.route('/')
def front_test():
    # 踩坑，这里是要在和这个py文件同一级目录下创建templates
    return render_template('front.html')


# 这个路由，用来请求，前端发来的，下载请求.
# 下载的资源，存储在当前文件下的 static下。
@app.route('/download')
def download():
    # os.path.realpath(__file__)打印出来的是当前路径————上传和下载.py所在的位置。
    # os.path.dirname(os.path.realpath(__file__))打印出来的是上面的文件所在的文件夹的位置。
    print(os.path.dirname(os.path.realpath(__file__)))
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(current_dir + "/static/download", "flask_download.txt", as_attachment=True)

# 这个是为了处理文件上传的
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files["file"]
        base_path = path.abspath(path.dirname(__file__))
        upload_path = path.join(base_path, 'static/uploads/')
        file_name = upload_path + secure_filename(f.filename)
        f.save(file_name)
        return redirect(url_for('upload'))
    return render_template('front.html', tip='上传成功')


if __name__ == '__main__':
    app.run(debug=True)

