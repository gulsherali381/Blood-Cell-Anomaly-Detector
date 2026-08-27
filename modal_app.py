import modal

# Modal ka image aur zaroori libraries
image = (
    modal.Image.debian_slim()
    .pip_install("fastapi", "uvicorn", "scikit-learn", "pandas", "numpy", "joblib")
)

app = modal.App("blood-cell-anomaly-detector")

# Aapke backend folder ki files ko Modal container mein add karna
image = image.add_local_file("backend/blood_cell_anomaly_detection.csv", "/root/blood_cell_anomaly_detection.csv")
image = image.add_local_file("backend/Blood-Cell-Anomaly-Detection.pkl", "/root/Blood-Cell-Anomaly-Detection.pkl")
image = image.add_local_file("backend/Blood-Cell-Anomaly-Detection-Scaler.pkl", "/root/Blood-Cell-Anomaly-Detection-Scaler.pkl")
image = image.add_local_file("backend/Blood-Cell-Anomaly-Detection-Encoded.pkl", "/root/Blood-Cell-Anomaly-Detection-Encoded.pkl")

@app.function(image=image)
@modal.asgi_app()
def fastapi_app():
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    from backend.main import app as web_app
    return web_app