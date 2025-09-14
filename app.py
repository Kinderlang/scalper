from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class MultibaggerPredictor:
    # ... (sama dengan class yang sudah Anda miliki sebelumnya) ...
    
    def run_analysis(self):
        """Jalankan analisis dan return hasilnya"""
        results = self.analyze_stocks()
        predictions = self.generate_predictions(results)
        
        # Siapkan data sector analysis
        sector_analysis = {}
        for stock in results:
            sector = stock['Sector']
            if sector not in sector_analysis:
                sector_analysis[sector] = {'count': 0, 'avg_gain': 0, 'stocks': []}
            
            sector_analysis[sector]['count'] += 1
            sector_analysis[sector]['avg_gain'] += stock['Potential_Gain']
            sector_analysis[sector]['stocks'].append(stock['Symbol'])
        
        for sector in sector_analysis:
            if sector_analysis[sector]['count'] > 0:
                sector_analysis[sector]['avg_gain'] = sector_analysis[sector]['avg_gain'] / sector_analysis[sector]['count']
        
        # Siapkan top 5 details
        top_details = []
        for i, pred in enumerate(predictions[:5], 1):
            top_details.append({
                'Symbol': pred['Symbol'],
                'Recommendation': pred['Recommendation'],
                'Confidence': pred['Confidence'],
                'Current_Price': pred['Current_Price'],
                'Predicted_Price': pred['Predicted_Price'],
                'Potential_Gain': pred['Potential_Gain'],
                'Entry_Price': pred['Entry_Price'],
                'Stop_Loss': pred['Stop_Loss'],
                'Risk_Reward': pred['Risk_Reward']
            })
        
        return {
            'predictions': predictions,
            'sector_analysis': sector_analysis,
            'top_details': top_details,
            'last_updated': datetime.now().isoformat()
        }

# Buat instance predictor
predictor = MultibaggerPredictor()

@app.route('/predictions/<date>')
def get_predictions(date):
    try:
        # Jika tanggal yang diminta adalah besok, kita perlu menghitung prediksi
        # Untuk simplicity, kita akan selalu mengembalikan prediksi terbaru
        results = predictor.run_analysis()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Multibagger Prediction API - Gunakan endpoint /predictions/YYYY-MM-DD"

if __name__ == '__main__':
    app.run(debug=True)
