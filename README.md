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
```

---

## 🚀 Getting Started

1. Installation
```bash
# Clone the project
git clone [https://github.com/ahnguyen24/frade-system.git](https://github.com/ahnguyen24/frade-system.git)
cd frade-system

# Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```
2. Running the System
The system operates in a 3-step lifecycle:

    1. Generate Synthetic Data:
    ```bash
    python src/data_generator.py
    ```
    2. Train the Model:
    ```bash
    python src/train_pipeline.py
    ```
    3. Start the API Server:
    ```bash
    python app.py
    ```

---

## 🧪 Testing
The system includes 8 pre-defined test cases in test.http covering:

* Normal Transactions: Low Score (< 0.2) -> ALLOW.

* New Device/Location: Medium Score (0.2 - 0.5) -> CHALLENGE_MFA.

* Velocity Attacks/Impossible Travel: High Score (> 0.5) -> BLOCK.

---

## 🛠️ Tech Stack
* Language: Python 3.x

* AI/ML: Scikit-learn (Isolation Forest), Pandas, Numpy

* Backend: Flask (RESTful API)

* Security: HMAC-SHA256 for Device Fingerprinting

* Geospatial: Haversine Mathematics