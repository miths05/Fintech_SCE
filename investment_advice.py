# services/investment_advice.py

import google.generativeai as genai
from flask import Blueprint, current_app, render_template, request, jsonify

investment_bp = Blueprint('investment', __name__)

# Prompt template for investment advice
prompt_template = """You are an AI assistant that helps users with investment advice. Use the provided financial knowledge and user input to give a personalized recommendation.

User Details:
- Age: {age}
- Occupation: {occupation}
- Monthly Income: ₹{monthly_income}
- Monthly Expenses: ₹{monthly_expenses}
- Current Savings: ₹{current_saving}
- Investment Goals: {investment_goals}
- Risk Tolerance: {risk_tolerance}
- Time Horizon: {time_horizon}
- Preferred Investment Type: {investment_type}
- Amount Available for Investment: ₹{investment_amount}
- Other Investments: {other_investments}
- Expected Returns: {expected_returns}

Financial Knowledge:
{financial_data}

Please provide detailed investment advice for this user.
"""

@investment_bp.route('/', methods=['GET'])
def show_form():
    # Renders a form that POSTs to /investment/advice
    return render_template('investment_advice.html')

@investment_bp.route('/advice', methods=['POST'])
def get_advice():
    user_data = request.form.to_dict()
    # Truncate to first 2000 chars to stay within prompt limits
    user_data['financial_data'] = current_app.config.get('FINANCIAL_DATA', '')[:2000]
    prompt = prompt_template.format(**user_data)

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt])

    advice = (
        response.text.strip()
        if response and response.text
        else "Sorry, I couldn't generate an investment recommendation. Please try again."
    )
    return jsonify({'advice': advice})
