from flask import Flask, request, render_template, send_file, after_this_request
import os

import tempfile


app = Flask(__name__)

# 替换词典
replace_dict = {
        "他妈的": "他爹的",
        "tmd":"他爹的",
        "操你妈": "骟你爹",
        "cnm":"骟你爹",
        "nm":"你爹",
        "你妈":"你爹",
        "你吗":"你爹",
        "你马":"你爹",
        "你🐴":"你爹",
        "婊子": "屌子",
        "傻逼": "傻屌",
        "婆婆妈妈": "爷们唧唧",
        "女拳": "女权",
        "父母": "母父",
        "爸妈": "妈爸",
        "娘娘腔":"超雄腔"
    # 添加更多的替换词对
}

# 上传页面
@app.route('/')
def upload_page():
    return """
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="/static/style.css">
        <title>辱女词替换工具</title>
        <script>
            function validateFile() {{
                var fileInput = document.getElementById('file-input');
                var filePath = fileInput.value;
                var allowedExtensions = /(\.srt|\.ass|\.txt)$/i;  // 允许的文件类型

                if (!allowedExtensions.exec(filePath)) {{
                    showPopup("不支持的文件类型");
                    fileInput.value = '';  
                    return false;
                }}
                return true;
            }}

            function showPopup(message) {{
                var popup = document.getElementById('popup-message');
                popup.innerHTML = message;
                popup.style.display = 'block';

                setTimeout(function() {{
                    popup.style.display = 'none';
                }}, 2000);
            }}

            /* 动态更新文件名 */
function updateFileName() {
    var input = document.getElementById('file-upload');
    var fileName = input.files.length > 0 ? input.files[0].name : "未选择任何文件";
    document.getElementById('file-name').textContent = fileName;
}
        </script>
        <style>
            #popup-message {{
                display: none;
                background-color: #f44336;
                color: white;
                padding: 10px 20px;
                position: fixed;
                top: 20%;
                left: 50%;
                transform: translate(-50%, -50%);
                border-radius: 5px;
                z-index: 1000;
                text-align: center;
                font-size: 18px;
            }}

            #replace-list {{
                margin-top: 20px;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                font-size: 16px;
                line-height: 1.5;
            }}
        </style>
    </head>
    <body>
        <h1 class="page-title">辱女词替换工具</h1>
        <div class="remarks"> 上传 SRT/ASS/TXT 文件并替换内容 </div>

        <!-- 提示框，默认隐藏 -->
        <div id="popup-message"></div>

        <div class="container">
            <form action="/upload" method="POST" enctype="multipart/form-data">
    <div class="file-upload">
        <label for="file-upload" class="custom-file-upload">选择文件</label>
        <input id="file-upload" type="file" name="file" onchange="updateFileName()" accept=".srt,.ass,.txt" required>
        <span id="file-name">未选择任何文件</span>
    </div>
    <input type="submit" value="上传并替换">
</form>


</form>

            </div>
        </div>
    

 <!-- 添加油猴脚本链接 -->
        <div class="tampermonkey-section">
            <p></p>
             <p> <a href="https://gist.github.com/qeeeem/7074b3267bae5b4893e29561ef26f7d2/raw/ab93118d4106bdfa0307880c3cbe40509ad1dce5/replaceTerms.user.js">点此加载油猴脚本</a>    需要提前安装<a href="https://www.tampermonkey.net/">油猴插件</a></p>
        </div>

        <!-- 页脚部分 -->
        <footer>
            <p>作者: RWsmymommy | 更新日期: 2024-09-10
        </footer>
    </body>
    </html>
    """





# 处理上传和替换
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file_extension = os.path.splitext(filename)[1].lower()

    # 根据文件类型处理 SRT、ASS 或 TXT 文件
    if file_extension == '.srt':
        content = file.read().decode('utf-8')
        new_content = process_srt(content)
    elif file_extension == '.ass':
        content = file.read().decode('utf-8')
        new_content = process_ass(content)
    elif file_extension == '.txt':  # 添加对TXT文件的处理
        content = file.read().decode('utf-8')
        new_content = process_txt(content)
    else:
        return "不支持的文件类型", 400

    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension, mode='w', encoding='utf-8') as temp_file:
        temp_file.write(new_content)
        temp_file_path = temp_file.name

    # 在响应之后删除临时文件
    @after_this_request
    def remove_file(response):
        try:
            os.remove(temp_file_path)
        except Exception as e:
            print(f"Error removing file: {e}")
        return response

    # 返回生成的文件
    return send_file(temp_file_path, as_attachment=True, download_name=filename)

# 处理 SRT 文件
def process_srt(content):
    for original, target in replace_dict.items():
        content = content.replace(original, target)
    return content

# 处理 ASS 文件
def process_ass(content):
    new_content = []
    for line in content.splitlines():
        if line.startswith("Dialogue:"):
            for original, target in replace_dict.items():
                line = line.replace(original, target)
        new_content.append(line)
    return '\n'.join(new_content)

# 处理 TXT 文件
def process_txt(content):
    for original, target in replace_dict.items():
        content = content.replace(original, target)
    return content

if __name__ == "__main__":
    app.run(debug=True)