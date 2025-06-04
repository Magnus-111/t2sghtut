from flask import Flask, request, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/qrcode')
def generate_qrcode():
    url = request.args.get('url')
    if not url:
        return 'Brak parametru url', 400
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')
