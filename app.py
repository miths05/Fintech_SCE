import os
import fitz                       # PyMuPDF
from flask import Flask, render_template
import google.generativeai as genai

# 1️⃣ Configure Gemini once
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyA7DrzBgrZkW-Za7itPE8VneZDCM69_L-Y"))

# 2️⃣ Extract all PDF text on startup
def extract_text_from_pdfs(folder_path=r"C:\Users\Mithilesh\Downloads\financial_advisory_bot-main\financial_advisory_bot-main\database"):
    text = ""
    for fname in os.listdir(folder_path):
        if fname.lower().endswith(".pdf"):
            with fitz.open(os.path.join(folder_path, fname)) as doc:
                for page in doc:
                    text += page.get_text() + "\n"
    return text

financial_data = extract_text_from_pdfs()

app = Flask(__name__)

# 3️⃣ Expose financial_data to services
app.config["FINANCIAL_DATA"] = financial_data

# 4️⃣ Register each blueprint
from services.investment_advice import investment_bp
from services.insurance_advice import insurance_bp
from services.loan_advice import loan_bp

app.register_blueprint(investment_bp, url_prefix="/investment")
app.register_blueprint(insurance_bp, url_prefix="/insurance")
app.register_blueprint(loan_bp,       url_prefix="/loan")

@app.route("/")
def index():
    return render_template("index.html")   # links to /investment, /insurance, /loan

if __name__ == "__main__":
    app.run(debug=True)
