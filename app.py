from flask import Flask, request, render_template_string

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
    if request.method == 'POST':
        try:
            user_ibu = int(request.form.get('ibu', 0))
            # Znajdź piwo o najbliższym IBU
            recommended = min(beers, key=lambda b: abs(b['ibu'] - user_ibu))
        except (ValueError, TypeError):
            recommended = None
    return render_template_string('''
        <h1>Wybierz preferowaną wartość IBU</h1>
        <form method="post">
            <label for="ibu">IBU (goryczka):</label>
            <input type="number" id="ibu" name="ibu" min="0" max="120" required>
            <button type="submit">Znajdź piwo</button>
        </form>
        {% if recommended %}
            <h2>Rekomendowane piwo: {{ recommended.name }} (IBU: {{ recommended.ibu }})</h2>
        {% endif %}
    ''', recommended=recommended)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)