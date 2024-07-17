import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from requests.exceptions import RequestException
import time

# Create an Object for ToastNotifier class
n = ToastNotifier()

# Function to fetch data from URL with retries
def get_weather_data(url, retries=3):
    for _ in range(retries):
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an exception for bad response status
            return r.text
        except RequestException as e:
            print(f"Error fetching data: {e}")
            time.sleep(5)  # Wait before retrying
    return None

# Function to parse HTML and extract weather information
def parse_weather_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find elements based on the updated HTML structure
    current_temp_elem = soup.find("span", class_="CurrentConditions--CurrentConditions--1XEyg")
    chances_rain_elem = soup.find("div", class_="Column--column--3tAuz Column--verticalStack--28b4K")
    
    # Extract text from elements if they exist, otherwise set to "N/A"
    current_temp = current_temp_elem.get_text(strip=True) if current_temp_elem else "N/A"
    chances_rain = chances_rain_elem.get_text(strip=True) if chances_rain_elem else "N/A"
    
    return current_temp, chances_rain

# Main function to display weather notification
def display_weather_notification():
    url = "https://weather.com/en-IN/weather/today/l/1f228531ea7af63dc435c8a1ebfeca05828bfc061790eb851fc6c3a81552a436"
    
    html_data = get_weather_data(url)
    if html_data:
        current_temp, chances_rain = parse_weather_data(html_data)
        result = f"Current Temperature: {current_temp} in Patna, Bihar\nChance of Rain: {chances_rain}"
    else:
        result = "Failed to fetch weather data."
    
    # Pass the result to the notification object
    n.show_toast("Weather Update", result, duration=10)

# Execute main function
if __name__ == "__main__":
    display_weather_notification()
