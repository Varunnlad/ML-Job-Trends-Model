import requests
from pytrends.request import TrendReq
import json
import time

def google_trends():
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))  

    trending_keywords = ["Python", "JavaScript", "Machine Learning", "SQL", "React"]
    
    max_retries = 3  # Retry up to 3 times
    for attempt in range(max_retries):
        try:
            pytrends.build_payload(trending_keywords, timeframe="today 1-m", geo="IN")
            trends_data = pytrends.interest_over_time()

            if not trends_data.empty:
                trends_dict = {keyword: int(trends_data[keyword].iloc[-1]) for keyword in trending_keywords}
            else:
                trends_dict = {keyword: 0 for keyword in trending_keywords}

            with open("trends_data.json", "w") as f:
                json.dump(trends_dict, f, indent=4)
            
            print("Google trends data stored successfully!")
            break  # Exit loop if successful

        except requests.exceptions.ReadTimeout:
            print(f"Attempt {attempt + 1}: Read timeout occurred. Retrying...")
            time.sleep(2)  # Wait 2 seconds before retrying
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break  # Stop retrying if a critical error occurs

if __name__ == "__main__":
    google_trends()
