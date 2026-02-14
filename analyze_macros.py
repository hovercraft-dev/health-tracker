import pandas as pd
import numpy as np

def analyze_macros():
    # Load data
    df = pd.read_csv('consolidated_health_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    # Filter for data with macros (Recent era)
    # Ensure numeric types
    for col in ['calories', 'protein_g']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # We only have macros in the recent logs
    macro_df = df.dropna(subset=['calories']).copy()
    
    if macro_df.empty:
        print("No macro data found.")
        return

    # Targets
    TARGET_CALORIES = 2400
    TARGET_PROTEIN = 180
    
    # 1. Adherence Stats
    avg_cals = macro_df['calories'].mean()
    avg_protein = macro_df['protein_g'].mean()
    
    days_tracked = len(macro_df)
    days_under_cals = len(macro_df[macro_df['calories'] <= TARGET_CALORIES])
    days_over_protein = len(macro_df[macro_df['protein_g'] >= TARGET_PROTEIN])
    
    print("--- Adherence (Nov 2025 - Present) ---")
    print(f"Days Tracked: {days_tracked}")
    print(f"Average Calories: {avg_cals:.0f} (Target: {TARGET_CALORIES})")
    print(f"Average Protein: {avg_protein:.0f}g (Target: >{TARGET_PROTEIN}g)")
    
    print(f"Calorie Adherence (<= {TARGET_CALORIES}): {days_under_cals}/{days_tracked} ({days_under_cals/days_tracked*100:.1f}%)")
    print(f"Protein Adherence (>= {TARGET_PROTEIN}g): {days_over_protein}/{days_tracked} ({days_over_protein/days_tracked*100:.1f}%)")
    
    # 2. Perfect Days (Hit both)
    perfect_days = macro_df[
        (macro_df['calories'] <= TARGET_CALORIES) & 
        (macro_df['protein_g'] >= TARGET_PROTEIN)
    ]
    print(f"Perfect Days (Hit Both): {len(perfect_days)} ({len(perfect_days)/days_tracked*100:.1f}%)")
    
    # 3. Impact Analysis
    # We want to see if weeks with better adherence had better weight results.
    # Weight tracking isn't daily in recent logs (some gaps), so we'll resample to weekly.
    
    # First, ensure we have a continuous date range for the recent period
    start_date = macro_df['date'].min()
    end_date = macro_df['date'].max()
    
    # Resample to weekly
    # Set date as index
    macro_df.set_index('date', inplace=True)
    
    weekly = macro_df.resample('W').agg({
        'calories': 'mean',
        'protein_g': 'mean',
        'weight': 'last' # Weight at end of week
    })
    
    # Calculate weekly weight change
    weekly['weight_change'] = weekly['weight'].diff()
    
    print("\n--- Weekly Trends ---")
    print(weekly[['calories', 'protein_g', 'weight', 'weight_change']].round(1))
    
    # 4. Protein vs Calories correlation
    corr = macro_df['protein_g'].corr(macro_df['calories'])
    print(f"\nCorrelation between Protein and Calories: {corr:.2f}")
    # If high positive, eating more protein usually comes with more calories.
    # If low/negative, you are finding lean sources effectively.

    # 5. Protein Density (Protein/Cals * 100) -> % of cals from protein ideally? 
    # Or just g/100kcal.
    macro_df['protein_density'] = macro_df['protein_g'] / (macro_df['calories'] / 100)
    print(f"Avg Protein Density: {macro_df['protein_density'].mean():.1f}g per 100kcal")

if __name__ == "__main__":
    analyze_macros()
