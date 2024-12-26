import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

class HealthcareAnalyzer:
    def __init__(self, location: str):
        self.location = location.lower()
        self.output_dir = self._create_output_directories()
        
    def _create_output_directories(self) -> str:
        """Create organized directory structure for outputs"""
        # Create base directories
        base_dir = "healthcare_analysis"
        location_dir = os.path.join(base_dir, self.location)
        timestamp = datetime.now().strftime("%Y%m%d")
        output_dir = os.path.join(location_dir, timestamp)
        
        # Create directory structure
        for dir_path in [
            base_dir,
            location_dir,
            output_dir,
            os.path.join(output_dir, "visualizations"),
            os.path.join(output_dir, "reports"),
            os.path.join(output_dir, "data")
        ]:
            os.makedirs(dir_path, exist_ok=True)
            
        return output_dir
    
    def load_and_clean_data(self, file_path: str) -> pd.DataFrame:
        """Load and prepare the data for visualization"""
        try:
            df = pd.read_csv(file_path)
            print(f"Data loaded successfully. Shape: {df.shape}")
            
            # Save a copy of the cleaned data
            cleaned_file_path = os.path.join(self.output_dir, "data", f"{self.location}_cleaned_data.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to: {cleaned_file_path}")
            
            # Convert incorporation date to datetime
            df['Incorporation Date'] = pd.to_datetime(df['Incorporation Date'])
            df['Incorporation Year'] = df['Incorporation Date'].dt.year
            df['SIC Codes'] = df['SIC Codes'].str.split(',').fillna('')
            
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def create_visualizations(self, df: pd.DataFrame):
        """Create various visualizations of the data"""
        viz_dir = os.path.join(self.output_dir, "visualizations")
        plt.style.use('default')
        
        # 1. Companies by Incorporation Year (Modern Style)
        plt.figure(figsize=(12, 6))
        year_counts = df['Incorporation Year'].value_counts().sort_index()
        
        # Filter years to start from 2000
        year_counts = year_counts[year_counts.index >= 2000]
        
        # Create modern bar chart with gradient color
        bars = plt.bar(year_counts.index, year_counts.values, 
                      color='skyblue', alpha=0.7, 
                      edgecolor='white', linewidth=1.5)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        # Display label for each year
        plt.xticks(year_counts.index, year_counts.index, rotation=45)
        
        plt.title(f'Company Formations by Year - {self.location.title()}', 
                 pad=20, fontsize=12, fontweight='bold')
        plt.xlabel('Year', fontsize=10)
        plt.ylabel('Number of Companies', fontsize=10)
        plt.grid(True, alpha=0.2, linestyle='--')
        
        # Set y-axis to start from zero
        plt.ylim(bottom=0)
        
        # Add trend line
        z = np.polyfit(year_counts.index, year_counts.values, 1)
        p = np.poly1d(z)
        plt.plot(year_counts.index, p(year_counts.index), 
                "r--", alpha=0.8, label='Trend')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f"{self.location}_companies_by_year.png"), 
                    dpi=300, bbox_inches='tight')
        plt.close()

        # 2. Postal Code Distribution
        plt.figure(figsize=(15, 6))
        postal_counts = df['Postal Code'].str[:4].value_counts().head(10)
        postal_counts.plot(kind='bar', color='lightgreen')
        plt.title(f'Top 10 Postal Code Areas - {self.location.title()}', pad=20)
        plt.xlabel('Postal Code Area')
        plt.ylabel('Number of Companies')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f"{self.location}_postal_distribution.png"))
        plt.close()

        # 3. Company Types Distribution
        plt.figure(figsize=(10, 6))
        company_types = df['Company Type'].value_counts()
        plt.pie(company_types, labels=company_types.index, autopct='%1.1f%%', 
                colors=['lightblue', 'lightgreen', 'lightcoral', 'wheat'])
        plt.title(f'Distribution of Company Types - {self.location.title()}', pad=20)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f"{self.location}_company_types.png"))
        plt.close()

        # 4. SIC Code Analysis
        all_sic_codes = [code.strip() for codes in df['SIC Codes'] for code in codes]
        sic_counts = pd.Series(all_sic_codes).value_counts().head(10)

        plt.figure(figsize=(12, 6))
        sic_counts.plot(kind='bar', color='lightcoral')
        plt.title(f'Top 10 Most Common SIC Codes - {self.location.title()}', pad=20)
        plt.xlabel('SIC Code')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f"{self.location}_sic_codes.png"))
        plt.close()

        # 5. Company Status Over Time (Modern Style)
        plt.figure(figsize=(12, 6))
        df_yearly = df.groupby(['Incorporation Year', 'Status']).size().unstack(fill_value=0)

        # Create modern stacked bar chart with better spacing
        ax = plt.gca()
        bars = df_yearly.plot(kind='bar', stacked=True, 
                             color=['skyblue', 'lightgreen', 'lightcoral', 'wheat'],
                             alpha=0.7, edgecolor='white', linewidth=1.5,
                             width=0.8,  # Adjust bar width
                             ax=ax)

        # Add value labels on top of bars
        for c in bars.containers:
            # Only show label if value > 0
            bars.bar_label(c, 
                          fmt='%d',  # Integer format
                          label_type='edge')  # Place label on top of each bar

        plt.title(f'Company Status by Incorporation Year - {self.location.title()}', 
                 pad=20, fontsize=12, fontweight='bold')
        plt.xlabel('Year', fontsize=10)
        plt.ylabel('Number of Companies', fontsize=10)

        # Improve grid appearance
        plt.grid(True, axis='y', alpha=0.2, linestyle='--')
        plt.grid(False, axis='x')  # Remove vertical gridlines

        # Adjust axis
        plt.ylim(bottom=0)
        ax.spines['top'].set_visible(False)  # Remove top border
        ax.spines['right'].set_visible(False)  # Remove right border

        # Add trend line for total companies per year
        yearly_totals = df_yearly.sum(axis=1)
        z = np.polyfit(range(len(yearly_totals)), yearly_totals.values, 1)
        p = np.poly1d(z)
        plt.plot(range(len(yearly_totals)), p(range(len(yearly_totals))), 
                "r--", alpha=0.8, label='Trend', linewidth=1.5)

        # Improve legend
        plt.legend(title='Status', bbox_to_anchor=(1.02, 1), 
                  loc='upper left', frameon=True, 
                  facecolor='white', framealpha=1)

        # Slant x-labels
        plt.xticks(rotation=45)

        # Adjust layout and save
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f"{self.location}_status_by_year.png"), 
                    dpi=300, bbox_inches='tight')
        plt.close()

        # New Healthcare-Specific Visualizations:
        
        # 6. Healthcare Service Type Distribution
        healthcare_sic_mapping = {
            '86101': 'General Medical Practice',
            '86102': 'Specialist Medical Practice',
            '86210': 'General Dental Practice',
            '86220': 'Specialist Dental Practice',
            '86230': 'Dental Practice Activities',
            '86900': 'Other Healthcare Activities',
            '87100': 'Residential Nursing Care',
            '87200': 'Residential Care (Learning Disabilities)',
            '87300': 'Residential Care (Elderly)',
            '87900': 'Other Residential Care',
            '88100': 'Social Work (Elderly)',
            '88910': 'Child Day-care',
            '88990': 'Other Social Work'
        }
        
        # Filter and count healthcare SIC codes
        healthcare_sics = [code.strip() for codes in df['SIC Codes'] 
                         for code in codes if code.strip() in healthcare_sic_mapping]
        
        if healthcare_sics:
            plt.figure(figsize=(12, 6))
            
            # Create and sort the series in ascending order
            sic_counts = pd.Series(healthcare_sics).map(healthcare_sic_mapping).value_counts().sort_values(ascending=True)
            
            # Create horizontal bar chart
            bars = plt.barh(sic_counts.index, sic_counts.values, 
                          color='lightgreen', alpha=0.7)
            
            plt.title(f'Healthcare Service Types - {self.location.title()}', 
                     pad=20, fontsize=12, fontweight='bold')
            plt.xlabel('Number of Services')  # Added the x-axis title as per instruction
            
            # Add value labels
            for i, v in enumerate(sic_counts.values):
                plt.text(v, i, f' {v}', va='center')
                
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, f"{self.location}_healthcare_services.png"))
            plt.close()

        # 7. Company Age Distribution
        company_ages = datetime.now().year - df['Incorporation Year']
        
        plt.figure(figsize=(10, 6))
        plt.hist(company_ages, bins=20, color='lightblue', 
                edgecolor='white', alpha=0.7)
        plt.title(f'Company Age Distribution - {self.location.title()}', 
                 pad=20, fontsize=12, fontweight='bold')
        plt.xlabel('Company Age (Years)')
        plt.ylabel('Number of Companies')
        plt.grid(True, alpha=0.2, linestyle='--')
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f"{self.location}_age_distribution.png"))
        plt.close()

        # 8. Geographic Concentration
        plt.figure(figsize=(12, 6))
        area_counts = df['City'].value_counts()
        
        # Create pie chart with percentage and absolute values
        plt.pie(area_counts, labels=[f'{idx}\n({val} companies)' 
                for idx, val in zip(area_counts.index, area_counts.values)],
                autopct='%1.1f%%', colors=plt.cm.Pastel1(np.linspace(0, 1, len(area_counts))))
        
        plt.title(f'Geographic Distribution - {self.location.title()}', 
                 pad=20, fontsize=12, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, f"{self.location}_geographic_distribution.png"))
        plt.close()

        print(f"Visualizations saved in: {viz_dir}")
        print("Generated visualizations:")
        print(f"1. {self.location}_companies_by_year.png (Improved)")
        print(f"2. {self.location}_postal_distribution.png")
        print(f"3. {self.location}_company_types.png")
        print(f"4. {self.location}_sic_codes.png")
        print(f"5. {self.location}_status_by_year.png")
        print(f"6. {self.location}_healthcare_services.png")
        print(f"7. {self.location}_age_distribution.png")
        print(f"8. {self.location}_geographic_distribution.png (New)")
    
    def generate_summary_report(self, df: pd.DataFrame):
        """Generate a summary report of the data"""
        try:
            print("Generating summary report...")
            print("DataFrame content before generating report:")
            print(df.head())  # Display the first few rows of the DataFrame

            total_companies = len(df)
            if total_companies == 0:
                print("No companies found in the DataFrame.")
                return
        
            active_companies = len(df[df['Status'] == 'active'])
            inactive_companies = total_companies - active_companies
            average_age = datetime.now().year - df['Incorporation Year'].mean()
        
            summary = {
                "Location": self.location.title(),
                "Analysis Date": datetime.now().strftime("%Y-%m-%d"),
                "Total Companies": total_companies,
                "Total Active Companies": active_companies,
                "Total Inactive Companies": inactive_companies,
                "Date Range": f"{df['Incorporation Year'].min()} - {df['Incorporation Year'].max()}",
                "Average Company Age": round(average_age, 2),
                "Most Common Company Type": df['Company Type'].mode()[0],
                "Top 5 Company Types": df['Company Type'].value_counts().head(5).to_dict(),
                "Most Common Postal Code Area": df['Postal Code'].str[:4].mode()[0],
                "Top 5 Postal Code Areas": df['Postal Code'].str[:4].value_counts().head(5).to_dict(),
                "Recent Incorporations (Last 2 Years)": len(df[df['Incorporation Year'] >= datetime.now().year - 2]),
                "Growth Rate (Last 5 Years)": self.calculate_growth_rate(df)
            }
        
            # Save summary to file
            report_path = os.path.join(self.output_dir, "reports", f"{self.location}_summary_report.txt")
            print(f"Saving report to: {report_path}")
            
            with open(report_path, 'w') as f:
                f.write(f"Healthcare Agencies Analysis Summary - {self.location.title()}\n")
                f.write("="* 50 + "\n\n")
                for key, value in summary.items():
                    f.write(f"{key}: {value}\n")
            
            print(f"Summary report saved to: {report_path}")
        except Exception as e:
            print(f"Error generating report: {e}")
            print("Check if the DataFrame has the required data and structure.")

    def calculate_growth_rate(self, df: pd.DataFrame) -> float:
        """Calculate the growth rate of companies over the last 5 years"""
        recent_years = df['Incorporation Year'].value_counts().sort_index()
        if len(recent_years) < 5:
            return 0.0  # Not enough data to calculate growth rate
        growth = (recent_years[-1] - recent_years[-5]) / recent_years[-5] * 100
        return round(growth, 2)

def main():
    # Configuration
    LOCATION = "birmingham"  # Can be changed for different locations
    
    # Initialize analyzer
    analyzer = HealthcareAnalyzer(LOCATION)
    
    # Find the most recent CSV file for the location
    data_dir = "data"  # Your raw data directory
    csv_pattern = f"healthcare_agencies_{LOCATION}_*.csv"
    
    try:
        # Find the most recent CSV file
        csv_files = [f for f in os.listdir(data_dir) if f.startswith(f"healthcare_agencies_{LOCATION}")]
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found for {LOCATION}")
        
        latest_csv = max(csv_files)  # Get most recent file
        file_path = os.path.join(data_dir, latest_csv)
        
        print(f"Processing data for {LOCATION.title()}...")
        print(f"Using file: {latest_csv}")
        
        # Process the data
        df = analyzer.load_and_clean_data(file_path)
        analyzer.create_visualizations(df)
        analyzer.generate_summary_report(df)
        
        print("\nAnalysis complete! Files are organized in the following structure:")
        print(f"healthcare_analysis/")
        print(f"└── {LOCATION}/")
        print(f"    └── {datetime.now().strftime('%Y%m%d')}/")
        print(f"        ├── data/")
        print(f"        ├── reports/")
        print(f"        └── visualizations/")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 