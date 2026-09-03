import modal

image = (
    modal.Image.debian_slim()
    .pip_install("fastapi", "uvicorn", "scikit-learn", "pandas", "numpy", "joblib")
)

app = modal.App("blood-cell-anomaly-detector")

# Backend folder se files ko /root mein add karein
image = image.add_local_file("backend/blood_cell_anomaly_detection.csv", "/root/blood_cell_anomaly_detection.csv")
image = image.add_local_file("backend/Blood-Cell-Anomaly-Detection.pkl", "/root/Blood-Cell-Anomaly-Detection.pkl")
image = image.add_local_file("backend/Blood-Cell-Anomaly-Detection-Scaler.pkl", "/root/Blood-Cell-Anomaly-Detection-Scaler.pkl")
image = image.add_local_file("backend/Blood-Cell-Anomaly-Detection-Encoded.pkl", "/root/Blood-Cell-Anomaly-Detection-Encoded.pkl")
image = image.add_local_file("backend/main.py", "/root/main.py")

# Naya — static folder (HTML/CSS/JS) ko bhi add karo
image = image.add_local_dir("backend/static", "/root/static")

@app.function(image=image)
@modal.asgi_app()
def fastapi_app():
    import sys
    import os
    sys.path.append("/root")
    from main import app as web_app
    return web_app
