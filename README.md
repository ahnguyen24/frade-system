# 🛡️ FRADE SYSTEM (Fraud Real-time Analysis & Detection Engine)

**FRADE System** is a professional-grade financial fraud detection engine that combines **Rule-based filtering** with **Unsupervised Machine Learning**. The system is designed to identify anomalous behaviors such as Account Takeover (ATO), simulated money laundering, and "Impossible Travel" scenarios.

---

## ✨ Key Features

- **AI-Driven Detection**: Utilizes the `Isolation Forest` algorithm to detect outliers in transaction data without the need for pre-labeled historical fraud data.
- **Impossible Travel Logic**: Implements the **Haversine Formula** to calculate geographical distances between consecutive transactions, flagging suspicious rapid movements.
- **RFM Feature Engineering**: Extracts Recency, Frequency, and Monetary metrics to identify "drain-the-account" patterns and brute-force transaction attempts.
- **Hybrid Response Layer**: A multi-tiered response strategy (**Allow**, **MFA Challenge**, **Block**) to balance user experience with high-level security.
- **Real-time API**: Built with Flask, providing a lightweight and scalable endpoint ready for integration with payment gateways.

---

## 📂 Project Structure

```text
FRADE_SYSTEM/
├── data/               # Data generation scripts and transactions.csv
├── models/             # Trained Isolation Forest models (.pkl)
├── src/                # Core logic source code
│   ├── features.py     # Feature extraction (RFM, Distance)
│   ├── detection.py    # AI Logic & Scoring mechanism
│   ├── response.py     # Risk thresholding and action logic
│   └── utils.py        # Security (Hashing) & Logging utilities
├── app.py              # Main API Gateway (Flask)
├── train_pipeline.py   # Automated training pipeline
└── test.http           # Comprehensive test cases for REST Client