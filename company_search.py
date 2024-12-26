import requests
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
import os
import base64

class CompaniesHouseAPI:
    def __init__(self, api_key: str):
        self.base_url = "https://api.company-information.service.gov.uk"
        
        auth_bytes = f"{api_key}:".encode('ascii')
        encoded_auth = base64.b64encode(auth_bytes).decode('ascii')
        
        self.headers = {
            'Authorization': f'Basic {encoded_auth}',
            'Accept': 'application/json'
        }
        
        self.test_auth()
    
    def test_auth(self):
        """Test authentication with a simple request"""
        test_url = f"{self.base_url}/company/00000006"
        print("Testing authentication...")
        print(f"Authorization header: {self.headers['Authorization']}")
        
        response = requests.get(test_url, headers=self.headers)
        print(f"Test response status: {response.status_code}")
        print(f"Test response: {response.text[:200]}\n")

    def search_companies(self, sic_codes: List[str], location: str, items_per_page: int = 150) -> List[Dict]:
        """
        Search for companies with specific SIC codes and location
        
        Args:
            sic_codes: List of SIC codes to search for
            location: Location to search in (e.g., 'Middlesbrough')
            items_per_page: Number of results per page
        """
        all_companies = []
        
        for sic_code in sic_codes:
            try:
                endpoint = f"{self.base_url}/advanced-search/companies"
                params = {
                    "sic_codes": sic_code,
                    "company_status": "active",
                    "location": location,  # Add location parameter
                    "size": items_per_page
                }
                
                print(f"Searching for SIC code: {sic_code} in {location}")
                response = requests.get(
                    endpoint,
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    companies = data.get("items", [])
                    print(f"Found {len(companies)} companies")
                    
                    # Filter companies to ensure they match the location
                    filtered_companies = [
                        company for company in companies
                        if location.lower() in str(company.get('registered_office_address', {})).lower()
                    ]
                    
                    print(f"After location filtering: {len(filtered_companies)} companies")
                    all_companies.extend(filtered_companies)
                else:
                    print(f"Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"Error processing SIC code {sic_code}: {str(e)}")
                continue
                
        return all_companies

def process_companies(companies: List[Dict]) -> pd.DataFrame:
    """Process and clean company data"""
    processed_data = []
    
    for company in companies:
        address = company.get("registered_office_address", {})
        company_info = {
            "Company Name": company.get("company_name"),
            "Company Number": company.get("company_number"),
            "Status": company.get("company_status"),
            "Company Type": company.get("company_type"),
            "Incorporation Date": company.get("date_of_creation"),
            "SIC Codes": ", ".join(company.get("sic_codes", [])),
            "Address Line 1": address.get("address_line_1"),
            "Address Line 2": address.get("address_line_2"),
            "City": address.get("locality"),
            "Postal Code": address.get("postal_code"),
            "Region": address.get("region"),
            "Country": address.get("country")
        }
        processed_data.append(company_info)
    
    return pd.DataFrame(processed_data)

def main():
    # Configuration
    LOCATION = "Birmingham"  # Set the location
    sic_codes = [
        "78200",  # Temporary employment agency activities
        "78109",  # Activities of employment placement agencies
        "87100",  # Residential nursing care activities
        "87300"   # Residential care activities for the elderly and disabled
    ]
    
    # Get API key
    api_key = os.getenv("COMPANIES_HOUSE_API_KEY", "your_api_key_here")
    
    print(f"Using API key: {api_key[:8]}...{api_key[-4:]}")
    print(f"Searching in location: {LOCATION}")
    
    # Initialize API client
    api = CompaniesHouseAPI(api_key)
    
    # Search for companies
    companies = api.search_companies(sic_codes, LOCATION)
    
    if companies:
        # Process the data
        df = process_companies(companies)
        
        # Save to CSV with timestamp and location in the "data" folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/healthcare_agencies_{LOCATION.lower()}_{timestamp}.csv"
        
        df.to_csv(filename, index=False)
        
        print(f"\nResults Summary:")
        print(f"Total companies found: {len(companies)}")
        print(f"Data saved to: {filename}")
        
        # Display first few results
        print("\nFirst few entries:")
        print(df[["Company Name", "City", "Postal Code"]].head())
    else:
        print("\nNo companies found or error occurred during search")

if __name__ == "__main__":
    main()