# 🩸 Blood Cell Anomaly Detector

An end-to-end machine learning application that automates the detection of abnormal blood cells from morphological and cellular feature data, using an unsupervised **Isolation Forest** model served through a **FastAPI** backend and an interactive **Streamlit** dashboard.

**Live Application:** [https://gulsherali381--blood-cell-anomaly-detector-fastapi-app.modal.run/)

---

## 🔍 Problem

Manual inspection of blood cell samples under a microscope is a core part of diagnosing conditions such as anemia, leukemia, and infections. However, this process has several limitations:

- It is **time-consuming**, requiring a trained lab technician to visually inspect each cell for irregularities in shape, size, texture, and staining.
- It is **subjective**, meaning results can vary between technicians, especially for borderline or ambiguous cases.
- It **does not scale well** — as sample volumes grow, manual screening becomes a bottleneck in diagnostic workflows.
- There is a lack of **accessible, automated tools** that allow quick screening of individual cells or entire batches of data, with the flexibility to adjust sensitivity based on clinical context.

There was a need for a lightweight, automated system that could take quantifiable cell measurements — already extractable from microscopy image analysis — and flag anomalies consistently and instantly, without requiring the reviewer to re-examine every single sample manually.

---

## 💡 Solution

This project addresses the problem by building a complete anomaly detection pipeline, from raw data to a deployed, usable application:

1. **Unsupervised Model Training** — An Isolation Forest model was trained on a dataset of 5,880 blood cell samples, using 16 morphological and image-derived features (cell shape, texture, color, and size measurements). The model learns what a "normal" cell looks like without ever being shown the labels during training, and identifies anomalies based on how easily a sample can be isolated from the rest of the data — a hallmark of outlier detection.

2. **REST API Backend** — The trained model, along with its preprocessing pipeline (encoding and scaling), is served through a FastAPI backend. This exposes endpoints for single-sample prediction, dynamic threshold adjustment, and random-sample retrieval, all validated using strict Pydantic schemas to ensure only well-formed data reaches the model.

3. **Interactive Dashboard** — A Streamlit frontend consumes this API to give users a complete, no-code interface:
   - **Scan** — Submit a single cell's features manually and get an instant classification with an anomaly score.
   - **Insights** — View dataset-level statistics and distributions to understand the underlying data the model was trained on.
   - **Bulk Scan** — Upload a CSV of multiple samples and receive predictions for the entire batch in one go, with results downloadable as a CSV.
   - **Log** — Track a running history of every scan performed in the session, with summary metrics and trend charts.
   - **Adjustable Sensitivity** — A live threshold slider lets the user tune how conservative or sensitive the anomaly flagging should be, without retraining the model.

4. **Cloud Deployment** — The backend is deployed serverlessly on **Modal**, and the frontend is hosted on **Streamlit Community Cloud**, making the entire tool accessible from any browser with no local setup required.

The result is a tool that takes what was previously a manual, inconsistent process and turns it into a fast, repeatable, and accessible screening step — while being transparent about its role as a research/educational aid rather than a diagnostic replacement.

---

## 🚀 Live Application

**Access the deployed app here:** [https://blood-cell-anomaly-detector.streamlit.app/](https://blood-cell-anomaly-detector.streamlit.app/)

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Core language used across data processing, model training, and both backend/frontend application logic |
| **Scikit-learn** | Used to train and apply the Isolation Forest anomaly detection model, along with feature scaling and encoding |
| **Pandas & NumPy** | Data manipulation, feature engineering, and numerical operations across the training dataset and incoming requests |
| **FastAPI** | Backend REST API framework, handling prediction requests, input validation (via Pydantic), and threshold management |
| **Pydantic** | Strict schema validation for all incoming API requests, ensuring data integrity before it reaches the model |
| **Streamlit** | Frontend framework used to build the interactive, multi-tab dashboard interface |
| **Modal** | Serverless cloud platform used to deploy and host the FastAPI backend |
| **Streamlit Community Cloud** | Hosting platform for the Streamlit frontend dashboard |
| **Joblib** | Serialization of the trained model, scaler, and feature schema for use outside the training environment |
| **Git & GitHub** | Version control and source code management |

---

## 📊 Model Overview

- **Algorithm:** Isolation Forest (unsupervised anomaly detection)
- **Dataset:** 5,880 blood cell samples across 19 cell types, with a natural anomaly rate of ~32%
- **Features used:** 16 morphological and image-derived measurements, including cell diameter, circularity, eccentricity, chromatin density, granularity, and RGB color intensity
- **Evaluation:** ~80% accuracy and 0.776 ROC-AUC against ground-truth labels held out during training

---

## 📁 Project Structure

```
├── backend/
│   ├── main.py                                  # FastAPI application and prediction endpoints
│   ├── Blood-Cell-Anomaly-Detection.pkl         # Trained Isolation Forest model
│   ├── Blood-Cell-Anomaly-Detection-Scaler.pkl  # Fitted feature scaler
│   ├── Blood-Cell-Anomaly-Detection-Encoded.pkl # Saved feature schema/column order
│   └── blood_cell_anomaly_detection.csv          # Training dataset
│
└── frontend/
    └── dashboard.py                              # Streamlit dashboard application
```

---

## ⚠️ Disclaimer

This tool is built for research and educational purposes only. It is **not a certified medical diagnostic device** and should not be used as a substitute for professional laboratory analysis or clinical judgment.
