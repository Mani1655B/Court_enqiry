from django.shortcuts import render
from .models import QueryLog
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Define the local path for the WebDriver
WEBDRIVER_PATH = 'Driver/chromedriver-win64/chromedriver.exe'

# Create your views here.

def scrape_court_data(case_type, case_number, filing_year):
    # Set up Selenium WebDriver with headless mode
    options = Options()
    options.add_argument('--headless')  # Enable headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
    options.add_argument('--no-sandbox')  # Bypass OS security model (optional)
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems in containers (optional)
    options.add_argument('--start-maximized')  # Start browser in full-screen mode

    # Use the locally downloaded WebDriver
    service = Service(WEBDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to the Delhi High Court website
        url = "https://delhihighcourt.nic.in/app/get-case-type-status"
        driver.get(url)
        sleep(3)  # Wait for the page to load

        # Extract CAPTCHA value
        captcha_value = driver.find_element(By.XPATH, "//*[@id='captcha-code']").text.strip()
        driver.find_element(By.XPATH, "//*[@name='captchaInput']").send_keys(captcha_value)

        # Fill out the form fields
        driver.find_element(By.XPATH, "//*[@name='case_type']").send_keys(case_type)
        driver.find_element(By.XPATH, "//*[@name='case_number']").send_keys(case_number)
        driver.find_element(By.XPATH, "//*[@name='case_year']").send_keys(filing_year)
        sleep(2)  # Wait for the form to be ready
        driver.find_element(By.XPATH, "//*[@id='search']").click()
        sleep(3)  # Wait for the search results to load


        # Extract relevant data from the table
        case_table = driver.find_element(By.XPATH, "//*[@id='caseTable']")
        rows = case_table.find_elements(By.TAG_NAME, 'tr')

        extracted_data = []
        row = rows[1]  # Skip the header row
        columns = row.find_elements(By.TAG_NAME, 'td')
        
        row1 = columns[1].text.strip().split("\n")  # Split multiple data by newline
        row2 = columns[2].text.strip().split("\n")
        row3 = columns[3].text.strip().split("\n")
        
        # Scroll to the 'Orders' link and center it in the viewport
        orders_link = columns[1].find_element(By.XPATH, "//*[@id='caseTable']/tbody/tr/td[2]/a[2]")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", orders_link)
        sleep(1)  # Small delay to ensure the element is in view

        # Use JavaScript to click the element
        driver.execute_script("arguments[0].click();", orders_link)
        sleep(3)  # Wait for the orders page to load

        # Extract the order download link and order date
        order_download_link = driver.find_element(By.XPATH, "//table[@id='caseTable']//a").get_attribute("href")
        order_date = driver.find_element(By.XPATH, "//*[@id='caseTable']/tbody/tr[1]/td[3]").text.strip()

        extracted_data.append({
            'case_no': case_number,
            'case_type': case_type,
            'filing_year': filing_year,
            'case_status': row1[1] if len(row1) > 1 else "N/A",
            'petitioner': row2[0] if len(row2) > 0 else "N/A",
            'respondent': row2[2] if len(row2) > 1 else "N/A",
            'last_hearing': (row3[1] if len(row3) > 0 else "N/A").split(':')[-1],
            'next_hearing': (row3[0] if len(row3) > 1 else "N/A").split(':')[-1],
            'court_number': (row3[2] if len(row3) > 2 else "N/A").split(':')[-1],
            'order_download_link': order_download_link,
            'order_date': order_date
        })

        return extracted_data

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        driver.quit()

def case_query_form(request):
    years = list(range(2025, 1960, -1))

    if request.method == 'POST':
        case_type = request.POST.get('case_type')
        case_number = request.POST.get('case_number')
        filing_year = request.POST.get('filing_year')

        # Use the scraping logic
        raw_response = scrape_court_data(case_type, case_number, filing_year)

        # Check for errors or no data
        if isinstance(raw_response, str) and raw_response.startswith("Error"):
            return render(request, 'court_fetcher/error.html', {'error_message': raw_response})
        elif not raw_response:
            return render(request, 'court_fetcher/error.html', {'error_message': 'No data found for the given inputs.'})
        
        # Log the query
        query_log = QueryLog.objects.create(
            case_type=case_type,
            case_number=case_number,
            filing_year=filing_year,
            raw_response=raw_response
        )

        return render(request, 'court_fetcher/results.html', {'query_log': query_log})

    return render(request, 'court_fetcher/form.html', {'years': years})
