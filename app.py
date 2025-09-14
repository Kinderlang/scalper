from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class MultibaggerPredictor:
    def __init__(self):
        self.target_stocks = [
            'BMBL.JK', 'GIAA.JK', 'GMFI.JK', 'HADE.JK',
            'HRTA.JK', 'IRSX.JK', 'BUMI.JK', 'TINS.JK',
            'BYAN.JK', 'DOID.JK', 'ELSA.JK', 'IMAS.JK',
            'KAEF.JK', 'LPPF.JK', 'MAPI.JK', 'IOTF.JK',
            'PBSA.JK', 'SMSM.JK', 'TARA.JK', 'WIKA.JK',
            'WINS.JK', 'YULE.JK', 'ZBRA.JK', 'ACES.JK',
            'AGRS.JK', 'AKSI.JK', 'APIC.JK', 'ASGR.JK',
            'BSBK.JK', 'KBLV.JK', 'MPXL.JK', 'MLPL.JK',
            'PTRO.JK', 'GZCO.JK', 'TPIA.JK', 'CUAN.JK',
            'CDIA.JK', 'BRMS.JK', 'GOTO.JK', 'HRTA.JK'
        ]
        
        # Tanggal prediksi (besok)
        self.prediction_date = datetime.now() + timedelta(days=1)

    # ... (semua method Anda yang lain tetap sama) ...

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
            'prediction_date': self.prediction_date.strftime('%Y-%m-%d'),
            'predictions': predictions,
            'sector_analysis': sector_analysis,
            'top_details': top_details,
            'last_updated': datetime.now().isoformat()
        }

# Buat instance predictor
predictor = MultibaggerPredictor()

@app.route('/')
def home():
    return "Multibagger Prediction API - Gunakan endpoint /predictions"

@app.route('/predictions')
def get_predictions():
    try:
        results = predictor.run_analysis()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
