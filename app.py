from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Configure API keys (store in environment variables for security)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# API route: generate itinerary using AI
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    destination = data.get("destination")
    days = data.get("days")
    budget = data.get("budget")

    prompt = f"Create a {days}-day travel itinerary for {destination} with a budget of {budget}."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Free tier alternative
            messages=[{"role": "system", "content": "You are a travel planner."},
                      {"role": "user", "content": prompt}],
            max_tokens=400
        )
        itinerary = response.choices[0].message["content"].strip()
        return jsonify({"itinerary": itinerary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
