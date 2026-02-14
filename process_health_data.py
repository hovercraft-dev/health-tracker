import pandas as pd
import glob
import os
import re

def parse_weight_file(filepath):
    """Parses the weight history file."""
    try:
        # Header is on the first line
        df = pd.read_csv(filepath, sep='\t')
        # Rename columns to be consistent
        df = df.rename(columns={'Date': 'date', 'Weight (kg)': 'weight', 'Notes': 'notes'})
        # Convert date
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
        # Filter out rows with no date
        df = df.dropna(subset=['date'])
        # Select relevant columns
        df = df[['date', 'weight', 'notes']]
        df['type'] = 'weight_history'
        return df
    except Exception as e:
        print(f"Error parsing weight file: {e}")
        return pd.DataFrame()

def parse_measurements_file(filepath):
    """Parses the measurements file."""
    try:
        # Header is on the 3rd line (skip 2 lines: Title, Empty)
        df = pd.read_csv(filepath, sep='\t', skiprows=2)
        
        # Rename columns
        df = df.rename(columns={
            'Date': 'date', 
            'Waist (cm)': 'waist_cm', 
            'Hips (cm)': 'hips_cm',
            'Biceps (L)': 'biceps_l',
            'Biceps (R)': 'biceps_r',
            'Notes': 'notes'
        })
        
        # Convert date
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
        
        # Filter out rows with no date
        df = df.dropna(subset=['date'])
        
        # Select relevant
        cols = ['date', 'waist_cm', 'hips_cm', 'biceps_l', 'biceps_r', 'notes']
        # Only keep columns that exist (in case of naming issues)
        existing_cols = [c for c in cols if c in df.columns]
        df = df[existing_cols]
        df['type'] = 'measurements'
        
        return df
    except Exception as e:
        print(f"Error parsing measurements file: {e}")
        return pd.DataFrame()

def parse_snapshot_file(filepath):
    """Parses the recent snapshot markdown file (heuristic parsing)."""
    data = []
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            
        # Very basic parsing for the table in the markdown
        in_table = False
        for line in lines:
            if line.strip().startswith('| Date'):
                in_table = True
                continue
            if line.strip().startswith('| :---'):
                continue
            
            if in_table and line.strip().startswith('|'):
                parts = [p.strip() for p in line.split('|')]
                # parts[0] is empty string because line starts with |
                if len(parts) >= 5:
                    date_str = parts[1]
                    weight_str = parts[3]
                    waist_str = parts[4]
                    notes_str = parts[5]
                    
                    if date_str == '-': continue

                    entry = {'date': date_str, 'notes': notes_str, 'type': 'snapshot'}
                    
                    # Clean weight
                    if weight_str != '-':
                        try:
                            entry['weight'] = float(weight_str.replace(',', '').replace('~', ''))
                        except: pass
                        
                    # Clean waist
                    if waist_str != '-':
                        try:
                            entry['waist_cm'] = float(waist_str.replace(',', '').replace('~', ''))
                        except: pass
                        
                    data.append(entry)
            elif in_table and not line.strip().startswith('|'):
                 # End of table
                 in_table = False

        df = pd.DataFrame(data)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
        return df
    except Exception as e:
        print(f"Error parsing snapshot file: {e}")
        return pd.DataFrame()


def parse_daily_logs(filepath):
    """Parses the detailed daily logs (Nov 2025 - Feb 2026)."""
    try:
        # Header is on the first line
        df = pd.read_csv(filepath, sep='\t')
        
        # Rename columns to be consistent
        # Date	Calories	Protein (g)	Carbs (g)	Fat (g)	Weight (kg)	Waist (cm)	Hips (cm)
        rename_map = {
            'Date': 'date', 
            'Calories': 'calories',
            'Protein (g)': 'protein_g',
            'Carbs (g)': 'carbs_g',
            'Fat (g)': 'fat_g',
            'Weight (kg)': 'weight', 
            'Waist (cm)': 'waist_cm',
            'Hips (cm)': 'hips_cm'
        }
        df = df.rename(columns=rename_map)
        
        # Convert date
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
        
        # Filter out rows with no date
        df = df.dropna(subset=['date'])
        
        # Clean numeric columns (remove commas, handle non-numeric)
        numeric_cols = ['calories', 'protein_g', 'carbs_g', 'fat_g', 'weight', 'waist_cm', 'hips_cm']
        for col in numeric_cols:
            if col in df.columns:
                if df[col].dtype == 'object':
                     df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
        
        df['type'] = 'daily_log'
        return df
    except Exception as e:
        print(f"Error parsing daily logs file: {e}")
        return pd.DataFrame()

def main():
    # 1. Loading data
    weight_df = parse_weight_file('historical_weight_2012_2026_raw.txt')
    measurements_df = parse_measurements_file('historical_measurements_2012_2026_raw.txt')
    # Prefer the comprehensive logs over the manual snapshot
    # snapshot_df = parse_snapshot_file('health_tracker_snapshot.md') 
    daily_logs_df = parse_daily_logs('recent_daily_log_2025_2026_raw.txt')
    
    # 2. Merging
    # Combine all into one timeline
    # We prioritize daily_logs_df for overlap periods as it has more columns (macros, hips)
    
    all_data = pd.concat([weight_df, measurements_df, daily_logs_df], ignore_index=True)
    
    # Sort by date
    all_data = all_data.sort_values(by='date')
    
    # Consolidate by date.
    # We want to keep non-null values. 
    # If there are duplicates, we generally trust the 'daily_log' most as it's the most recent and detailed.
    # Group by date and take the first non-null. 
    # Since we prioritize daily_logs, let's sort such that daily_log comes first for same dates?
    # Actually, groupby().first() takes the first appearing value.
    # So if we concatenate daily_logs LAST, and then sort by date, 
    # the order within the same date is unstable unless we explicit sort.
    
    # Better approach: Sort by Date, then by some priority? 
    # Or just rely on the fact that daily_logs is dense.
    
    consolidated = all_data.groupby('date').last().reset_index() # using last() might be safer if we append daily_logs last?
    
    # 3. Validation / Basic Stats
    print(f"Total entries: {len(consolidated)}")
    print(f"Date range: {consolidated['date'].min()} to {consolidated['date'].max()}")
    print(f"Rows with weight: {consolidated['weight'].count()}")
    print(f"Rows with waist: {consolidated.get('waist_cm', pd.Series()).count()}")
    print(f"Rows with hip: {consolidated.get('hips_cm', pd.Series()).count()}")
    print(f"Rows with calories: {consolidated.get('calories', pd.Series()).count()}")

    # 4. Save to JSON and CSV
    consolidated.to_json('consolidated_health_data.json', orient='records', date_format='iso')
    consolidated.to_csv('consolidated_health_data.csv', index=False)
    
    # print head
    print("\nSample Data:")
    print(consolidated.tail(10))

if __name__ == "__main__":
    main()
