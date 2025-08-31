from flask import Flask, render_template, request
from google import genai
from google.genai import types
import google.auth
import os

app = Flask(__name__)

creds, project = google.auth.default()

client = genai.Client(
    credentials=creds,
    project=project,
    location="us-central1",
    vertexai=True,
)

MODEL = "gemini-2.5-flash"

@app.route("/", methods=["GET", "POST"])
def index():
    story = None
    if request.method == "POST":
        topic = request.form.get("topic", "monkeys riding bicycles")
        
        prompt = f"Write a short, very silly and funny story about: {topic}"
        
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
)
        story = None
        if response.candidates:
            story = "".join(
                part.text for part in response.candidates[0].content.parts if part.text
            )
        else:
            story = "No story generated."

    return render_template("index.html", story=story)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
