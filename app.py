from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chat():
    response = ""

    if request.method == "POST":
        prompt = request.form.get("prompt", "")

        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        if r.status_code == 200:
            response = r.json()["response"]
        else:
            response = f"Error: {r.text}"

    return f"""
    <html>
    <body>
        <h1>Vulnerable AI Chat App</h1>
        <form method="post">
            <input type="text" name="prompt" style="width:400px">
            <input type="submit" value="Send">
        </form>
        <p>{response}</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
