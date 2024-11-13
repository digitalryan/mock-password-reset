from flask import Flask, request, jsonify
import os
import secrets

app = Flask(__name__)

# Mock database for users
users = {
    "user@example.com": {
        "password": "original_password",
        "reset_token": None
    }
}

@app.route("/api/password-reset/request", methods=["POST"])
def request_password_reset():
    data = request.get_json()
    email = data.get("email")

    # Check if the email exists
    if email not in users:
        return jsonify({"error": "User not found"}), 404

    # Generate a reset token
    token = secrets.token_urlsafe(16)
    users[email]["reset_token"] = token

    # In a real setup, you would email the reset link to the user here
    # (e.g., using an email service API)

    return jsonify({"message": "Password reset token generated", "reset_token": token})

@app.route("/api/password-reset/confirm", methods=["POST"])
def confirm_password_reset():
    data = request.get_json()
    email = data.get("email")
    token = data.get("token")
    new_password = data.get("new_password")

    # Validate email and token
    if email not in users or users[email]["reset_token"] != token:
        return jsonify({"error": "Invalid token or email"}), 400

    # Update the password
    users[email]["password"] = new_password
    users[email]["reset_token"] = None  # Clear the token after reset

    return jsonify({"message": "Password reset successful"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))