from flask import Flask, render_template, url_for, redirect,request
import json
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

def load_cafes():
    with open('cafes.json', 'r') as f:
        return json.load(f)


@app.route('/')
def home():
    cafes = load_cafes()
    return render_template('home.html', cafes=cafes)

@app.route('/cafe/<int:cafe_id>')
def view_cafe(cafe_id):
    cafes = [
        {'id': 1, 'name': 'Latte Lounge', 'desc': 'Cozy cafe with fast wifi...', 'image': 'latte.jpg'},
        {'id': 2, 'name': 'Java Junction', 'desc': 'Open late, great coffee...', 'image': 'java.jpg'},
        {'id': 3, 'name': 'Brew Base', 'desc': 'Quiet and strong wifi...', 'image': 'brew.avif'}
    ]
    cafe = None
    for c in cafes:
        if c['id'] == cafe_id:
            cafe = c
            break

    if cafe:
        return render_template('cafe_detail.html', cafe=cafe)
    else:
        return "Cafe not found", 404

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        name = request.form["name"]
        desc = request.form["desc"]
        image = request.files["image"]

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            with open("cafes.json", "r") as f:
                cafes = json.load(f)

            new_id = max([c["id"] for c in cafes]) + 1 if cafes else 1
            cafes.append({
                "id": new_id,
                "name": name,
                "desc": desc,
                "image": filename
            })

            with open("cafes.json", "w") as f:
                json.dump(cafes, f, indent=2)

        return redirect(url_for("home"))

    return render_template("add_cafe.html")
if __name__ == '__main__':
    app.run(debug=True)

