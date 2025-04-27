import logging
import google.generativeai as genai
from flask import Blueprint, render_template, request, jsonify

insurance_bp = Blueprint('insurance', __name__)

# Prompt template for insurance advice
prompt_template = """You are an AI assistant that provides personalized insurance advice. Use the information below to analyze the user's profile and generate a detailed recommendation.

User Information:
- Age: {age}
- Occupation: {occupation}
- Monthly Income: ₹{monthly_income}
- Monthly Expenses: ₹{monthly_expenses}
- Current Savings: ₹{current_saving}
- Investment Goals: {investment_goals}
- Risk Tolerance (1–10): {risk_tolerance}
- Type of Financial Advice Needed: {advice_type}
- Current Financial Products: {current_financial_products}
- Existing Debts/Loans: {debts_loans}
- Details of Debts/Loans: {debts_loans_details}

Please provide insurance advice that fits the user’s financial profile, covering aspects like:
- Type of insurance (life, health, term, etc.)
- Suitable coverage amount
- Premium affordability
- Investment-linked or risk-free plans
"""

@insurance_bp.route('/', methods=['GET'])
def show_form():
    # Renders a form that POSTs to /insurance/advice
    return render_template('insurance_advice.html')

@insurance_bp.route('/advice', methods=['POST'])
def get_advice():
    user_data = request.form.to_dict()
    prompt = prompt_template.format(**user_data)

    model = genai.GenerativeModel("gemini-1.5-pro")
    try:
        response = model.generate_content([prompt])
        advice = response.text.strip() if response and response.text else ""
    except Exception as e:
        logging.error(f"Error generating advice: {e}")
        advice = ""

    if not advice:
        advice = "Sorry, I couldn't generate insurance advice at the moment. Please try again."

    return jsonify({'advice': advice})

# Explicitly export insurance_bp
__all__ = ['insurance_bp']