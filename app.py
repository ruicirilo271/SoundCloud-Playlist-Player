from flask import Flask, render_template, request, jsonify
from api import SoundCloud

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    sc = SoundCloud()
    playlist = sc.search_playlist(query)
    if not playlist:
        return jsonify({"error": "No playlist found"}), 404

    return jsonify(playlist)

if __name__ == "__main__":
    app.run(debug=True)
