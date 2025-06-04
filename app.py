from flask import Flask, request, render_template_string, send_file, url_for
import qrcode
import io

app = Flask(__name__)

# Prosta baza piw z przykładowymi wartościami IBU
beers = [
    {"name": "Pilsner", "ibu": 30},
    {"name": "IPA", "ibu": 60},
    {"name": "Stout", "ibu": 40},
    {"name": "Lager", "ibu": 20},
    {"name": "Porter", "ibu": 35},
]

@app.route('/', methods=['GET', 'POST'])
def home():
    recommended = None
    qrcode_url = None
    if request.method == 'POST':
        try:
            user_ibu = int(request.form.get('ibu', 0))
            # Znajdź piwo o najbliższym IBU
            recommended = min(beers, key=lambda b: abs(b['ibu'] - user_ibu))
            if recommended:
                google_url = f"https://www.google.com/search?tbm=isch&q={recommended['name']}+beer"
                # Generowanie lokalnego linku do QR code
                qrcode_url = url_for('beer_qrcode', beer_name=recommended['name'])
        except (ValueError, TypeError):
            recommended = None
    return render_template_string('''
        <h1>Wybierz preferowaną wartość IBU</h1>
        <p><strong>Legenda IBU:</strong> <br>
        0-20: bardzo niska goryczka<br>
        21-40: umiarkowana goryczka<br>
        41-60: wyraźna goryczka<br>
        61+: bardzo wysoka goryczka</p>
        <form method="post">
            <label for="ibu">IBU (goryczka):</label>
            <input type="number" id="ibu" name="ibu" min="0" max="120" required>
            <button type="submit">Znajdź piwo</button>
        </form>
        {% if recommended %}
            <h2>Rekomendowane piwo: {{ recommended.name }} (IBU: {{ recommended.ibu }})</h2>
            <p>Otwórz w Google Images: <a href="https://www.google.com/search?tbm=isch&q={{ recommended.name }}+beer" target="_blank">Zobacz zdjęcia</a></p>
            {% if qrcode_url %}
                <p>QR Code do wyszukiwarki Google Images:</p>
                <img src="{{ qrcode_url }}" alt="QR Code">
            {% endif %}
        {% endif %}
    ''', recommended=recommended, qrcode_url=qrcode_url)

@app.route('/beer_qrcode/<beer_name>')
def beer_qrcode(beer_name):
    google_url = f"https://www.google.com/search?tbm=isch&q={beer_name}+beer"
    img = qrcode.make(google_url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)