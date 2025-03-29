from create_app import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Align with Render’s default
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=port, debug=debug)