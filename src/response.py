def evaluate_action(risk_score):
    if risk_score < 0.2:
        return {
            "action": "ALLOW", 
            "message": "Transaction verified and allowed",
            "code": 200
        }
    elif 0.2 <= risk_score < 0.5:
        return {
            "action": "CHALLENGE_MFA", 
            "message": "Multi-factor authentication required",
            "code": 202
        }
    else:
        return {
            "action": "BLOCK", 
            "message": "High risk detected. Transaction declined",
            "code": 403
        }