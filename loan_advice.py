# services/loan_advice.py

import google.generativeai as genai
from flask import Blueprint, current_app, render_template, request, jsonify

loan_bp = Blueprint('loan', __name__)

# Prompt template for loan advice
prompt_template = """You are an AI assistant that helps people with financial advice. The answer should be descriptive.

User Information:
- Age: {age}
- Occupation: {occupation}
- Monthly Income: ₹{monthly_income}
- Monthly Expenses: ₹{monthly_expenses}
- Current Savings: ₹{current_saving}
- Investment Goals: {investment_goals}
- Risk Tolerance: {risk_tolerance}
- Loan Term: {loan_term}
- Interest Rate: {interest_rate}
- Credit Score: {credit_score}

Financial Knowledge:
{financial_data}

Provide personalized loan advice based on the user's financial status and best financial practices.
"""

@loan_bp.route('/', methods=['GET'])
def show_form():
    # Renders a form that POSTs to /loan/advice
    return render_template('loan_advice.html')

@loan_bp.route('/advice', methods=['POST'])
def get_advice():
    user_data = request.form.to_dict()
    # Include PDF‐extracted text
    user_data['financial_data'] = current_app.config.get('FINANCIAL_DATA', '')[:2000]
    prompt = prompt_template.format(**user_data)

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt])

    advice = (
        response.text.strip()
        if response and response.text
        else "Sorry, I couldn't generate loan advice. Please try again."
    )
    return jsonify({'advice': advice})
