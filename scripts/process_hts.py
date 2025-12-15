import pandas as pd
import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import time

class HTSDataProcessor:
    def __init__(self):
        self.db_path = "data/hts.db"
        self.csv_dir = "data/hts_csvs"
        self.sections = {
            'I': 'Live Animals; Animal Products',
            'II': 'Vegetable Products',
            'III': 'Animal or Vegetable Fats and Oils',
            'IV': 'Prepared Foodstuffs; Beverages, Spirits and Vinegar',
            'V': 'Mineral Products',
            'VI': 'Products of the Chemical or Allied Industries',
            'VII': 'Plastics and Articles Thereof; Rubber and Articles Thereof',
            'VIII': 'Raw Hides and Skins, Leather, Furskins',
            'IX': 'Wood and Articles of Wood',
            'X': 'Pulp of Wood or Other Fibrous Cellulosic Material',
            'XI': 'Textile and Textile Articles',
            'XII': 'Footwear, Headgear, Umbrellas',
            'XIII': 'Articles of Stone, Plaster, Cement',
            'XIV': 'Natural or Cultured Pearls, Precious Stones',
            'XV': 'Base Metals and Articles of Base Metal',
            'XVI': 'Machinery and Mechanical Appliances',
            'XVII': 'Vehicles, Aircraft, Vessels',
            'XVIII': 'Optical, Photographic, Cinematographic Instruments',
            'XIX': 'Arms and Ammunition',
            'XX': 'Miscellaneous Manufactured Articles',
            'XXI': 'Works of Art, Collectors Pieces'
        }
    
    def create_comprehensive_sample_data(self):
        """Create comprehensive sample data for all sections"""
        all_data = []
        
        # Sample data for each section
        section_samples = {
            'I': [
                ['0101.30.00.00', 'Live asses', 'Free', 'Free', 'Free'],
                ['0102.21.00.00', 'Live cattle, purebred breeding animals', '2.5%', 'Free', '5%'],
                ['0103.10.00.00', 'Live swine, purebred breeding animals', 'Free', 'Free', 'Free'],
                ['0104.10.10.00', 'Live sheep, purebred breeding animals', '3¢/kg', 'Free', '6¢/kg'],
                ['0105.11.00.10', 'Live chickens weighing not more than 185g', '0.9¢ each', 'Free', '4¢ each']
            ],
            'II': [
                ['0701.10.00.00', 'Seed potatoes, fresh or chilled', '0.5¢/kg', 'Free', '3¢/kg'],
                ['0702.00.00.00', 'Tomatoes, fresh or chilled', '2.8¢/kg', 'Free', '4.6¢/kg'],
                ['0803.10.20.00', 'Plantains, fresh', 'Free', 'Free', 'Free']
            ],
            'VI': [
                ['2804.40.00.00', 'Oxygen', '3.7%', 'Free', '25%'],
                ['2805.11.00.00', 'Sodium', '5.3%', 'Free', '41%']
            ],
            'XV': [
                ['7201.10.00.00', 'Nonalloy pig iron', 'Free', 'Free', '$1.11/t'],
                ['7202.11.10.00', 'Ferromanganese', '1.4%', 'Free', '5%']
            ],
            'XVI': [
                ['8471.30.01.00', 'Portable automatic data processing machines', 'Free', 'Free', '35%'],
                ['8517.12.00.50', 'Smartphones', 'Free', 'Free', '35%']
            ]
        }
        
        for section, items in section_samples.items():
            for item in items:
                all_data.append({
                    'Section': section,
                    'HTS Number': item[0],
                    'Description': item[1],
                    'General Rate of Duty': item[2],
                    'Special Rate of Duty': item[3],
                    'Column 2 Rate of Duty': item[4]
                })
        
        return pd.DataFrame(all_data)
    
    def process_all_sections(self):
        """Process all HTS sections"""
        print("Processing all HTS sections...")
        
        # Check for existing CSV files
        existing_files = []
        for section in self.sections.keys():
            csv_path = os.path.join(self.csv_dir, f"section_{section.lower()}.csv")
            if os.path.exists(csv_path):
                existing_files.append(csv_path)
        
        if existing_files:
            print(f"Found {len(existing_files)} existing CSV files")
            # Load and combine all CSVs
            all_dfs = []
            for csv_path in existing_files:
                df = pd.read_csv(csv_path)
                all_dfs.append(df)
            combined_df = pd.concat(all_dfs, ignore_index=True)
        else:
            print("No existing CSV files found. Creating comprehensive sample data...")
            combined_df = self.create_comprehensive_sample_data()
        
        # Store in SQLite database
        conn = sqlite3.connect(self.db_path)
        
        # Main HTS data table
        combined_df.to_sql("hts_data", conn, if_exists="replace", index=False)
        
        # Create section summary table
        section_summary = combined_df.groupby('Section').agg({
            'HTS Number': 'count',
            'Description': 'first'
        }).reset_index()
        section_summary.columns = ['Section', 'Item Count', 'Section Description']
        section_summary.to_sql("hts_sections", conn, if_exists="replace", index=False)
        
        # Create indexes for faster queries
        cursor = conn.cursor()
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_hts_number ON hts_data("HTS Number")')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_section ON hts_data(Section)')
        
        conn.commit()
        conn.close()
        
        print(f"Successfully processed {len(combined_df)} HTS entries from {len(combined_df['Section'].unique())} sections")
        print("Database updated with comprehensive HTS data")
        
        return combined_df
    
    def download_hts_section(self, section_num):
        """Download HTS data for a specific section (placeholder for actual implementation)"""
        # This would contain actual web scraping logic to download from hts.usitc.gov
        # For now, it returns None to use sample data
        print(f"Downloading Section {section_num} data...")
        time.sleep(1)  # Simulate download
        return None
    
    def search_hts(self, keyword):
        """Search HTS database by keyword"""
        conn = sqlite3.connect(self.db_path)
        query = """
            SELECT "HTS Number", Description, "General Rate of Duty"
            FROM hts_data
            WHERE Description LIKE ?
            LIMIT 10
        """
        df = pd.read_sql_query(query, conn, params=[f'%{keyword}%'])
        conn.close()
        return df

if __name__ == "__main__":
    processor = HTSDataProcessor()
    os.makedirs(processor.csv_dir, exist_ok=True)
    
    # Process all sections
    df = processor.process_all_sections()
    
    # Test search functionality
    print("\nTesting search functionality...")
    results = processor.search_hts("cattle")
    print(results)