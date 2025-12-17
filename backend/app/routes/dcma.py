from flask import Blueprint, request, jsonify
import smtplib
from email.message import EmailMessage
import os

dcma_bp = Blueprint("dcma", __name__)

DCMA_RECIPIENT = os.environ.get("host_email", "dmca@website.com")
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.example.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "your_email@example.com")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "your_email_password")

@dcma_bp.route("/send", methods=["POST"])
def send_dcma():
    data = request.json
    content_url = data.get("content_url")
    infringing_url = data.get("infringing_url")
    copyright_owner_name = data.get("owner_name", "Copyright Owner")
    copyright_owner_email = data.get("owner_email", "owner@example.com")
    description = data.get("description", "Unauthorized copying of copyrighted material.")

    if not content_url or not infringing_url:
        return jsonify({"status": "error", "message": "content_url and infringing_url are required"}), 400

    subject = f"DMCA Takedown Notice: Infringement Detected"
    body = f"""
To Whom It May Concern,

I, {username}, am the owner of the copyrighted work at:
{content_url}

I have discovered that the following URL is infringing my copyright:
{infringing_url}

Description:
{description}

I hereby request that you remove or disable access to the infringing material pursuant to the Digital Millennium Copyright Act.

Sincerely,
{copyright_owner_name}
Email: {copyright_owner_email}
"""

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = DCMA_RECIPIENT

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        return jsonify({"status": "success", "message": "DMCA notice sent successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
