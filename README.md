# TOPSIS Web Service

A Flask-based web application that implements the **TOPSIS**
(Technique for Order Preference by Similarity to Ideal Solution)
method for multi-criteria decision making.

The application allows users to upload a CSV file, specify weights
and impacts, and receive a ranked result file generated using the
TOPSIS algorithm.

---

## 🚀 Features

- Web-based execution of the TOPSIS algorithm
- CSV file upload through browser
- User-defined weights and impacts
- Automatic ranking of alternatives
- Result generated as a CSV file
- Email delivery of result file using SMTP
- Simple Flask backend with HTML frontend

---

## 🛠 Tech Stack

- **Python**
- **Flask** – Web framework
- **Pandas** – Data processing
- **NumPy** – Numerical computation
- **SMTP (Gmail)** – Email delivery

---


---

## ▶️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/topsis-web-service.git
cd topsis-web-service
```
---

2. Install dependencies
   
```
pip install -r requirements.txt
```
3. Run the Flask application
```
python app.py
```

4. Open in browser
http://127.0.0.1:5000/

Notes:
- Email delivery uses Gmail SMTP and requires an App Password (regular Gmail passwords are not supported).


📊 Input Format
CSV File

First column: Alternatives

Remaining columns: Numeric criteria values

Minimum 3 columns required

Weights

Comma-separated numeric values
Example:
1,1,1,1,1

Impacts
+ for benefit criteria
- for cost criteria
Example:
+,+,+,+,+

📈 Output

CSV file containing:
Topsis Score
Rank
Result file is generated server-side
Email delivery implemented via SMTP



