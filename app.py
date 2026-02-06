from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

# CREATE REQUIRED FOLDERS
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        weights_input = request.form["weights"]
        impacts_input = request.form["impacts"]
        email = request.form["email"]

        # SAVE UPLOADED FILE
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # READ DATA
        data = pd.read_csv(input_path)
        matrix = data.iloc[:, 1:].astype(float).values

        weights = list(map(float, weights_input.split(",")))
        impacts = impacts_input.split(",")

        # -------- TOPSIS --------
        norm = np.sqrt((matrix ** 2).sum(axis=0))
        normalized = matrix / norm
        weighted = normalized * weights

        ideal_best = []
        ideal_worst = []

        for i in range(len(impacts)):
            if impacts[i] == "+":
                ideal_best.append(weighted[:, i].max())
                ideal_worst.append(weighted[:, i].min())
            else:
                ideal_best.append(weighted[:, i].min())
                ideal_worst.append(weighted[:, i].max())

        ideal_best = np.array(ideal_best)
        ideal_worst = np.array(ideal_worst)

        dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
        dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

        scores = dist_worst / (dist_best + dist_worst)

        data["Topsis Score"] = scores
        data["Rank"] = data["Topsis Score"].rank(ascending=False).astype(int)

        # SAVE RESULT
        result_path = os.path.join(RESULT_FOLDER, "result.csv")
        data.to_csv(result_path, index=False)

        # -------- SEND EMAIL --------
        msg = EmailMessage()
        msg["Subject"] = "TOPSIS Result"
        msg["From"] = "your@gmail.com"
        msg["To"] = email
        msg.set_content("Please find attached TOPSIS result.")

        with open(result_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename="result.csv"
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("your@gmail.com", "yourpassword")# REPLACE WITH YOUR EMAIL AND PASSWORD(generated APP PASSWORD)
            server.send_message(msg)

        return "Result sent to your email!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
