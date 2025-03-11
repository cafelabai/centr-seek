import requests
from bs4 import BeautifulSoup
import json

# Fetch the webpage
def fetch_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching URL: {url}, Error: {e}")
        return None

# Parse the HTML
def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup


# Dynamic data extraction
def extract_data(soup):
    data = {}

    # Iterate through all parent containers
    for section in soup.find_all("div"):
        # Extract label and value from children dynamically
        children = section.find_all(recursive=False) 
        if len(children) >= 2: 
            label = children[0]
            value = children[1]

            # Normalize and store
            field_name = label.get_text(strip=True).lower().replace(" ", "_")
            field_value = value.get_text(strip=True)
            data[field_name] = field_value

    return data


# Save to JSON file
def save_to_json(data, output_file):
    with open(output_file, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {output_file}")


# Main scraping function
def scrape_to_json(url, output_file):
    html_content = fetch_page(url)
    if not html_content:
        return

    soup = parse_html(html_content)
    extracted_data = extract_data(soup)
    save_to_json(extracted_data, output_file)

# Testing the function
url = "https://scholarworks.indianapolis.iu.edu/items/c6ef0000-3a19-4377-b1ba-91cb8b5ed456" 
output_file = "dynamic_extracted_data.json"
scrape_to_json(url, output_file)





import requests
from bs4 import BeautifulSoup
import json
import os

# Fetch the webpage
def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching URL: {url}, Error: {e}")
        return None

# Parse the HTML content
def parse_html(html_content):
    return BeautifulSoup(html_content, "html.parser")

# Extract specific fields
def extract_data(soup):
    """Extract only the required fields from the HTML."""
    data = {}

    # Map fields to keywords or labels to search
    field_mapping = {
        "Title": ["title", "h1"],
        "Abstract": ["abstract"],
        "Date": ["date", "published"],
        "Authors": ["author", "authors"],
        "Keywords": ["keywords", "key words"],
        "DOI": ["doi"],
        "Permanent Link": ["permanent link", "permalink"]
    }

    # Extract data dynamically based on mapping
    for field, keywords in field_mapping.items():
        found_value = None
        for keyword in keywords:
            # Look for elements that contain the keyword
            found_element = soup.find(lambda tag: tag.name in ["div", "span", "p", "meta", "h1"] 
                                      and keyword in tag.get_text(strip=True).lower())
            if found_element:
                found_value = found_element.get_text(strip=True)
                break
        if found_value:
            data[field] = found_value

    return data

# Save extracted data to a JSON file
def save_to_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {output_file}")

# Process all HTML files in a folder
def process_html_folder(input_folder, output_folder):
    """Load all HTML files, extract required fields, and save to JSON."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".html"):  # Process only .html files
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.json")

            with open(input_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            soup = parse_html(html_content)
            extracted_data = extract_data(soup)

            # Save the extracted data to a JSON file
            save_to_json(extracted_data, output_file_path)

# Main function
def main():
    input_folder = "input_html_folder"  # Replace with the folder containing HTML files
    output_folder = "output_json_folder"  # Replace with the folder to save JSON files

    print("Starting HTML processing...")
    process_html_folder(input_folder, output_folder)
    print("Processing completed!")

if __name__ == "__main__":
    main()
