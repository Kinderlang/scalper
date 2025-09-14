import json
from datetime import datetime, timedelta
from app import predictor
import os

def update_predictions():
    # Jalankan analisis
    results = predictor.run_analysis()
    
    # Buat direktori data jika belum ada
    os.makedirs('data', exist_ok=True)
    
    # Simpan hasil ke file JSON
    with open('data/predictions.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Predictions updated at {datetime.now()}")

if __name__ == '__main__':
    update_predictions()
