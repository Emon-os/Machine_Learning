from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load model and data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'LinearRegressionModel.pkl'), 'rb') as f:
    model = pickle.load(f)

df = pd.read_csv(os.path.join(BASE_DIR, 'Cleaned Car.csv'))

# Build company -> car names mapping
names_by_company = {}
for company in sorted(df['company'].unique()):
    names_by_company[company] = sorted(df[df['company'] == company]['name'].unique().tolist())

companies = sorted(df['company'].unique().tolist())
fuel_types = df['fuel_type'].unique().tolist()
years = sorted(df['year'].unique().tolist(), reverse=True)


@app.route('/')
def index():
    return render_template(
        'index.html',
        companies=companies,
        names_by_company=names_by_company,
        fuel_types=fuel_types,
        years=years
    )


@app.route('/predict', methods=['POST'])
def predict():
    try:
        name = request.form.get('name')
        company = request.form.get('company')
        year = int(request.form.get('year'))
        kms_driven = int(request.form.get('kms_driven'))
        fuel_type = request.form.get('fuel_type')

        input_df = pd.DataFrame(
            [[name, company, year, kms_driven, fuel_type]],
            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']
        )

        prediction = model.predict(input_df)
        price = round(float(prediction[0]), 2)

        return jsonify({'success': True, 'price': price})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
