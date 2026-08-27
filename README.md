# Blood-Cell-Anomaly-Detector
## 🔍 Problem

Traditional blood cell anomaly screening and diagnostic workflows often rely on manual, time-consuming inspections that are prone to human bottlenecks and inconsistencies. Healthcare setups and data analysts frequently struggle with a lack of automated, scalable, and readily accessible tools for real-time cellular screening, managing batch datasets, and easily adjusting custom anomaly detection thresholds on the fly.

## 💡 Solution

This project provides a full-stack, cloud-hosted machine learning application that completely automates cellular anomaly screening. It uses an Isolation Forest machine learning model backend powered by FastAPI and deployed via Modal for serverless, high-performance cloud inference. This is paired with an interactive, user-friendly Streamlit frontend dashboard that allows users to perform real-time single-sample predictions, run automated batch processing on uploaded datasets, and interactively customize anomaly detection thresholds with instant visual feedback.

## 🚀 Live Application URL

Access Deployed Application: [suspicious link removed]

## 🛠️ Technologies Used

* **Python:** Core programming language used for data processing, machine learning modeling, and backend/frontend application logic.
* **FastAPI:** High-performance web framework used to build the backend REST API endpoints for handling data inference requests.
* **Streamlit:** Interactive web framework used to design and deploy the frontend user dashboard interface.
* **Modal:** Cloud platform utilized for serverless deployment and hosting of the FastAPI backend.
* **Scikit-learn:** Machine learning library used for building and applying the Isolation Forest anomaly detection model alongside data preprocessing scalers and encoders.
* **Pandas & NumPy:** Data manipulation and numerical computation libraries used for handling tabular blood cell datasets and CSV processing.
* **Git & GitHub:** Version control and code repository management for tracking and storing project files.