def evaluate_action(risk_score):
    # Cấu hình lại các ngưỡng (Tùy chỉnh dựa trên thực tế test)
    if risk_score < 0.2:  
        return {"action": "ALLOW", "code": 200}
    
    elif 0.2 <= risk_score < 0.5: # Hạ trần xuống 0.5 (trước đây là 0.75)
        return {"action": "CHALLENGE_MFA", "message": "Yêu cầu mã OTP bổ sung", "code": 202}
    
    else: # Mọi score >= 0.5 sẽ bị BLOCK
        return {"action": "BLOCK", "message": "Giao dịch rủi ro cao. Tài khoản đã bị khóa tạm thời.", "code": 403}