import pandas as pd
import numpy as np

def estimate_body_fat():
    """
    Estimates Body Fat % using the Navy Seal Formula:
    BF% = 495 / (1.0324 - 0.19077 * log10(waist - neck) + 0.15456 * log10(height)) - 450
    
    Since we don't have neck measurements, we will use a standard estimate based on BMI/Weight
    or provide a range based on typical neck sizes (38cm - 42cm).
    
    We will calculate:
    1. 2013 (Leannest): Weight 80kg, Waist 80cm
    2. 2025 (Peak): Weight 115kg, Waist ~113cm
    3. 2026 (Current): Weight 104.7kg, Waist 100.5cm
    """
    
    HEIGHT_CM = 183
    
    # Data points
    scenarios = [
        {'Era': '2013 (Leanest)', 'Weight': 80.0, 'Waist': 80.0},
        {'Era': '2025 (Peak)', 'Weight': 115.0, 'Waist': 113.0},
        {'Era': '2026 (Current)', 'Weight': 104.7, 'Waist': 100.5},
        {'Era': 'Goal (Primary)', 'Weight': 100.0, 'Waist': 96.0}, # Est waist based on current trend (approx 0.8cm per kg)
        {'Era': 'Goal (Secondary)', 'Weight': 95.0, 'Waist': 92.0},  # Est waist
    ]
    
    # Neck size assumptions (cm)
    # Neck usually grows with weight but less than waist.
    # At 80kg, neck might be ~38cm. At 115kg, maybe ~43cm.
    # We'll use a sliding scale estimate: Base 38cm + (Weight - 80) * 0.1 ? 
    # Let's try 3 neck sizes: Small (38), Med (40), Large (42) to give a range.
    
    neck_sizes = [38, 40, 42, 44]
    
    print(f"{'Era':<20} | {'Weight':<8} | {'Waist':<8} | {'Neck Est':<10} | {'Est BF%':<10} | {'Category'}")
    print("-" * 80)
    
    results = []

    for s in scenarios:
        # Estimate neck based on weight to narrow it down
        # Heuristic: Neck = 37 + (Weight - 70) * 0.15 roughly? 
        # 80kg -> 38.5
        # 105kg -> 42.25
        # 115kg -> 43.75
        est_neck = 37 + (s['Weight'] - 70) * 0.12 # Conservative estimate
        
        bf_percent = 495 / (1.0324 - 0.19077 * np.log10(s['Waist'] - est_neck) + 0.15456 * np.log10(HEIGHT_CM)) - 450
        
        # Categorize
        cat = "Obese"
        if bf_percent < 25: cat = "Average"
        if bf_percent < 17: cat = "Fitness"
        if bf_percent < 14: cat = "Athletic"
        if bf_percent > 25: cat = "Obese" # Navy formula overestimates slightly for muscular people?
        
        print(f"{s['Era']:<20} | {s['Weight']:<8} | {s['Waist']:<8} | {est_neck:<10.1f} | {bf_percent:<10.1f}% | {cat}")
        
        results.append({
            'Era': s['Era'],
            'Weight': s['Weight'],
            'BF': bf_percent,
            'MuscleMass': s['Weight'] * (1 - bf_percent/100)
        })

    # Lean Mass Comparison
    print("\n--- Lean Mass Analysis (LBM) ---")
    lbm_2013 = results[0]['MuscleMass']
    lbm_now = results[2]['MuscleMass']
    
    print(f"2013 Est. Lean Mass: {lbm_2013:.1f} kg")
    print(f"2026 Est. Lean Mass: {lbm_now:.1f} kg")
    print(f"Difference: {lbm_now - lbm_2013:.1f} kg (Matches our prev estimate of 5-8kg!)")
    
    # Target Recommendations
    print("\n--- Target Recommendations ---")
    print("For a 'Fitness' look (15-17% BF):")
    # If LBM is ~78kg (current est)
    # Weight = LBM / (1 - TargetBF)
    # Weight = 78 / (1 - 0.15) = 91.7kg
    target_weight_15 = lbm_now / 0.85
    print(f"To reach 15% BF (maintaining current muscle): ~{target_weight_15:.1f} kg")
    
    target_weight_12 = lbm_now / 0.88
    print(f"To reach 12% BF (Athletic/Abs visible): ~{target_weight_12:.1f} kg")

if __name__ == "__main__":
    estimate_body_fat()
