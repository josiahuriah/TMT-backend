from create_app import create_app
import os

app = create_app()

# with app.app_context():
#     db.create_all()  # Creates tables based on models

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "True") == "True")