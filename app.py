from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/count', methods=['POST'])
def count_pills():
    data = request.get_json()
    img_data = re.sub('^data:image/.+;base64,', '', data['image'])
    img_bytes = base64.b64decode(img_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # นับเม็ดยา
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11,11), 0)
    _, thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    count = len(contours)

    return jsonify({'count': count})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)