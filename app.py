from flask import Flask, render_template, request, jsonify
import openai
import sqlite3

# =======================
# iRecipe App – Backend
# =======================

app = Flask(__name__)

# 🔑 Your OpenAI API key (replace with your own)
openai.api_key = "YOUR_OPENAI_API_KEY"

# =======================
# Database Setup (SQLite for hackathon)
# =======================
def init_db():
    conn = sqlite3.connect("irecipe.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ingredients TEXT,
                    recipe TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# =======================
# Routes
# =======================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_recipe", methods=["POST"])
def get_recipe():
    data = request.get_json()
    ingredients = data.get("ingredients")

    # Generate recipe using OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful recipe assistant."},
                {"role": "user", "content": f"Suggest 3 simple recipes using {ingredients}. Keep instructions short and clear."}
            ],
            max_tokens=300,
            temperature=0.7
        )
        recipe_text = response["choices"][0]["message"]["content"].strip()

        # Save to DB
        conn = sqlite3.connect("irecipe.db")
        c = conn.cursor()
        c.execute("INSERT INTO recipes (ingredients, recipe) VALUES (?, ?)", (ingredients, recipe_text))
        conn.commit()
        conn.close()

        return jsonify({"recipe": recipe_text})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/history")
def history():
    conn = sqlite3.connect("irecipe.db")
    c = conn.cursor()
    c.execute("SELECT ingredients, recipe FROM recipes ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()

    history_data = [{"ingredients": row[0], "recipe": row[1]} for row in rows]
    return jsonify(history_data)

# =======================
# Run Server
# =======================
if __name__ == "__main__":
    app.run(debug=True)
