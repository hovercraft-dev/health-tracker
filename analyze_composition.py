import pandas as pd
import numpy as np

def analyze_composition_change():
    """
    Analyzes the hypothesis that the user has more muscle mass now due to kettlebells.
    Metric: Waist circumference at equivalent body weights.
    If waist is smaller at the same weight, it implies more lean mass / higher density.
    """
    df = pd.read_csv('consolidated_health_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    # Define Eras
    # Era 1: The First Cut (2012 - 2013)
    era1_start = pd.to_datetime('2012-04-01')
    era1_end = pd.to_datetime('2013-12-31')
    
    # Era 2: The Recent Cut (Nov 2025 - Present)
    era2_start = pd.to_datetime('2025-11-01')
    era2_end = pd.to_datetime('2026-03-01')
    
    df_era1 = df[(df['date'] >= era1_start) & (df['date'] <= era1_end) & df['weight'].notnull() & df['waist_cm'].notnull()].copy()
    df_era2 = df[(df['date'] >= era2_start) & (df['date'] <= era2_end) & df['weight'].notnull() & df['waist_cm'].notnull()].copy()
    
    df_era1['Era'] = '2012-2013'
    df_era2['Era'] = '2025-2026'
    
    print(f"Era 1 Data Points: {len(df_era1)}")
    print(f"Era 2 Data Points: {len(df_era2)}")
    
    # Compare matching weights
    # We'll create bins or rounds to matching weights
    comparison_data = []
    
    # Iterate through current era weights and find closest matches in old era
    print("\n--- Direct Comparisons (Waist size at same Weight) ---")
    print(f"{'Weight (kg)':<12} | {'2012-13 Waist':<15} | {'2025-26 Waist':<15} | {'Difference':<10}")
    print("-" * 60)
    
    comparison_rows = []
    
    # Use bins of 2kg to find overlaps
    # Bins: 100-102, 102-104, 104-106, etc.
    min_w = min(df_era1['weight'].min(), df_era2['weight'].min())
    max_w = max(df_era1['weight'].max(), df_era2['weight'].max())
    
    bins = np.arange(int(min_w), int(max_w) + 2, 2)
    
    valid_comparisons = 0
    total_diff = 0
    
    for i in range(len(bins)-1):
        low = bins[i]
        high = bins[i+1]
        mid = (low + high) / 2
        
        # Get avg waist for this bin
        w1 = df_era1[(df_era1['weight'] >= low) & (df_era1['weight'] < high)]['waist_cm'].mean()
        w2 = df_era2[(df_era2['weight'] >= low) & (df_era2['weight'] < high)]['waist_cm'].mean()
        
        if pd.notnull(w1) and pd.notnull(w2):
            diff = w2 - w1
            print(f"{mid:<12.1f} | {w1:<15.1f} | {w2:<15.1f} | {diff:<10.1f}")
            valid_comparisons += 1
            total_diff += diff

    avg_diff = total_diff / valid_comparisons if valid_comparisons > 0 else 0
    print("-" * 60)
    print(f"Average Difference: {avg_diff:.1f} cm")
    
    # 4. Waist to Weight Ratio Analysis
    # Lower is better (less waist per kg of bodyweight)
    ratio1 = (df_era1['waist_cm'] / df_era1['weight']).mean()
    ratio2 = (df_era2['waist_cm'] / df_era2['weight']).mean()
    
    print("\n--- Waist-to-Weight Ratio (cm/kg) ---")
    print(f"2012-2013 Average: {ratio1:.3f}")
    print(f"2025-2026 Average: {ratio2:.3f}")
    
    diff_ratio = ratio2 - ratio1
    if diff_ratio < 0:
         print(f"Improvement: Your waist is {abs(diff_ratio):.3f} cm/kg smaller now.")
    else:
         print(f"Change: Your waist is {diff_ratio:.3f} cm/kg larger/similar now.")

    # 5. Specific Reference Point (104-105kg)
    # User is currently ~104.7. Closest 2012 data?
    target_weight = 104.7
    tolerance = 2.0
    
    closest_2012 = df_era1[
        (df_era1['weight'] >= target_weight - tolerance) & 
        (df_era1['weight'] <= target_weight + tolerance)
    ]
    
    if not closest_2012.empty:
        avg_waist_2012 = closest_2012['waist_cm'].mean()
        print(f"\n--- Specific Check at ~{target_weight}kg ---")
        print(f"Now (2026): ~100.5 cm")
        print(f"Then (2012): ~{avg_waist_2012:.1f} cm (based on matched weights)")
        print(f"Difference: {100.5 - avg_waist_2012:.1f} cm")

    # Save comparison to sorted DF for detailed report
    comp_df = pd.DataFrame(comparison_rows)
    # comp_df.to_csv('waist_comparison.csv', index=False)

if __name__ == "__main__":
    analyze_composition_change()
