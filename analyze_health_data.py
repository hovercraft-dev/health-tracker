import pandas as pd
import numpy as np

def analyze_health_data():
    # Load data
    df = pd.read_csv('consolidated_health_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    # User constants
    HEIGHT_M = 1.83
    AGE = 44
    GENDER = 'M'
    
    # Calculate derived metrics
    df['bmi'] = df['weight'] / (HEIGHT_M ** 2)
    df['whr'] = df['waist_cm'] / df['hips_cm']
    df['year'] = df['date'].dt.year
    
    # 1. Overall Statistics
    print("--- General Statistics ---")
    print(f"Date Range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Weight Range: {df['weight'].min()}kg - {df['weight'].max()}kg")
    print(f"Waist Range: {df['waist_cm'].min()}cm - {df['waist_cm'].max()}cm")
    
    # 2. Key Milestones (Best/Worst)
    lowest_weight = df.loc[df['weight'].idxmin()]
    highest_weight = df.loc[df['weight'].idxmax()]
    lowest_waist = df.loc[df['waist_cm'].idxmin()] if df['waist_cm'].notnull().any() else None
    
    print("\n--- Key Milestones ---")
    print(f"Lowest Weight: {lowest_weight['weight']}kg on {lowest_weight['date'].date()}")
    print(f"Highest Weight: {highest_weight['weight']}kg on {highest_weight['date'].date()}")
    if lowest_waist is not None:
        print(f"Smallest Waist: {lowest_waist['waist_cm']}cm on {lowest_waist['date'].date()}")

    # 3. Recent Context (Last 12 months vs Historical)
    current_state = df.iloc[-1]
    print("\n--- Current Status (Feb 2026) ---")
    print(f"Weight: {current_state['weight']}kg")
    print(f"Waist: {current_state['waist_cm']}cm")
    print(f"BMI: {current_state['bmi']:.1f}")
    if pd.notnull(current_state['whr']):
        print(f"Waist-to-Hip Ratio: {current_state['whr']:.2f}")
    
    # 4. Pattern Recognition (Yearly Averages)
    print("\n--- Yearly Averages ---")
    yearly = df.groupby('year')[['weight', 'waist_cm', 'bmi']].mean().round(1)
    print(yearly)
    
    # 5. Health Risk Indicators
    # WHR > 0.9 for men indicates abdominal obesity
    # BMI > 30 is obese, 25-30 overweight
    print("\n--- Health Markers ---")
    latest_whr = df['whr'].dropna().iloc[-1] if not df['whr'].dropna().empty else None
    latest_bmi = df['bmi'].dropna().iloc[-1] if not df['bmi'].dropna().empty else None
    
    print(f"Latest BMI: {latest_bmi:.1f} ({'Obese' if latest_bmi >= 30 else 'Overweight' if latest_bmi >= 25 else 'Normal'})")
    
    if latest_whr:
        print(f"Latest WHR: {latest_whr:.2f} ({'High Risk' if latest_whr > 0.9 else 'Low Risk'})")
        
    # Check for Yo-Yo patterns
    # Define a 'cycle' as a swing of more than 5kg followed by a reversal
    # Simple heuristic: calculate rolling variations
    
    # 6. Trends
    # Calculate simple trends
    df = df.sort_values('date')
    
    # Identify major phases
    print("\n--- Major Phases Detected ---")
    # Simple low points detection (local minima with window)
    # We can just look at weights min/max per year to see the fluctuation
    annual_ranges = df.groupby('year')['weight'].agg(['min', 'max', 'mean'])
    annual_ranges['swing'] = annual_ranges['max'] - annual_ranges['min']
    print("Annual Swings (>5kg years):")
    print(annual_ranges[annual_ranges['swing'] > 5])

if __name__ == "__main__":
    analyze_health_data()
