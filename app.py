from create_app import create_app
import os
from dotenv import load_dotenv

if os.getenv("FLASK_ENV") != "production":
    load_dotenv()

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("FLASK_DEBUG", "False") == "True"

    if os.getenv("FLASK_ENV") == "production":
        debug = False
    
    app.run(host="0.0.0.0", port=port, debug=debug)