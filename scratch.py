from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dateutil.parser import parse
import json

US_BANK_DATA_URL = 'https://www.nasdaq.com/market-activity/funds-and-etfs/spffx/historical'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver


def get_latest_date_value(driver):
  driver.get(US_BANK_DATA_URL)
  print('Driver: ', driver)
  title = driver.title
  print('Title: ',title)
  latest_date = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[4]/div[2]/div/table/tbody[2]/tr[1]/th').text
  latest_value = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[4]/div[2]/div/table/tbody[2]/tr[1]/td[1]').text
  return {
    'currentDate' : latest_date,
    'currentValue' : latest_value
  }

if __name__ == "__main__":
  print('Creating driver')
  driver = get_driver()

  print('Fetching US Bank Data Page')
  latest_date_value = get_latest_date_value(driver)
  
  print(f'Found {len(latest_date_value)} data points')
  
  print('currentDate:', latest_date_value['currentDate'])
  print('currentValue:', latest_date_value['currentValue'])

  # Convert Date to YYYY-MM-DD format
  format_date = str(parse(latest_date_value['currentDate'])).split()[0]
  print(format_date)

  # Append date to JSON file.
  data = {
               "Date": format_date,
               "Close": float(latest_date_value['currentValue'])
          }


  with open('usbank-sphere.json', 'r') as outfile:
    next(outfile)
    data_file = outfile.readlines()

  with open('usbank-sphere.json', 'w+') as outfile:
    outfile.write("[")
    outfile.write("\n")
    outfile.write(json.dumps(data, indent=4))
    outfile.write(",")
    outfile.write("\n")
    
    for line in data_file:
      outfile.write(line)

    outfile.close()

  print('Finished.')
