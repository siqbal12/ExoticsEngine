from flask import Flask
from flask_cors import CORS  # You'll need to install flask-cors: pip install flask-cors
from pricing_routes import pricing_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for React requests

# Register the pricing blueprint
app.register_blueprint(pricing_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)