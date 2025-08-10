# Court Inquiry System

A Django-based web application for scraping and displaying case information from the Delhi High Court website.

## Project Overview

This application allows users to search for court case information by entering case type, case number, and filing year. It automatically scrapes data from the Delhi High Court website and presents it in a user-friendly format.

## Features

- **Case Search**: Search by case type, case number, and filing year
- **Automated CAPTCHA Handling**: Automatically extracts and enters CAPTCHA values
- **Data Extraction**: Retrieves case status, petitioner/respondent details, hearing dates, and court numbers
- **Order Information**: Extracts order download links and order dates
- **Error Handling**: Comprehensive error pages for invalid inputs or no data found
- **Bootstrap UI**: Modern, responsive user interface

## Technology Stack

- **Backend**: Django (Python)
- **Web Scraping**: Selenium WebDriver with Chrome
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
- **Driver**: ChromeDriver for automated browsing

## How I Built It

### 1. Project Setup
- Created Django project with `django-admin startproject`
- Set up virtual environment for dependency management
- Configured Django app structure

### 2. Web Scraping Implementation
- Implemented Selenium WebDriver for automated browser control
- Used headless Chrome for efficient scraping
- Configured XPath selectors for precise element targeting
- Added automatic CAPTCHA extraction and input

### 3. Data Processing
- Structured data extraction from court website tables
- Implemented data parsing for multiple information fields
- Added error handling for missing or malformed data

### 4. User Interface
- Created Django templates with Bootstrap styling
- Implemented form validation and user input handling
- Added error pages for better user experience

### 5. Database Integration
- Used Django ORM for data persistence
- Created models for query logging
- Implemented data storage for scraped information

## Challenges Faced & Solutions

### 1. Element Click Intercepted Error
**Challenge**: Selenium couldn't click the "Orders" link in headless mode
```
Error: element click intercepted: Element is not clickable at point (251, 469)
```
**Solution**: 
- Used JavaScript to scroll element into viewport center
- Implemented JavaScript click instead of Selenium click
- Added proper element visibility checks

```python
# Scroll to element and click using JavaScript
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", orders_link)
driver.execute_script("arguments[0].click();", orders_link)
```

### 2. CAPTCHA Handling
**Challenge**: Automatically handling dynamic CAPTCHA on the website
**Solution**: 
- Extracted CAPTCHA text from HTML element
- Automated CAPTCHA input submission
- Implemented proper timing for CAPTCHA processing

### 3. Timing and Synchronization
**Challenge**: Page loading and element availability timing issues
**Solution**:
- Added strategic delays for page loads (3 seconds)
- Implemented WebDriverWait for element availability
- Balanced speed vs. reliability for demo purposes

### 4. Data Structure Parsing
**Challenge**: Extracting structured data from unformatted table cells
**Solution**:
- Used string splitting and indexing for data extraction
- Implemented fallback values for missing data
- Added robust error handling for malformed content

### 5. Headless Mode Issues
**Challenge**: Different behavior between headless and visible browser modes
**Solution**:
- Optimized viewport and window sizing
- Used JavaScript interactions instead of direct clicks
- Added element centering for better interaction

### 6. Error Handling and User Experience
**Challenge**: Providing meaningful feedback for various error conditions
**Solution**:
- Created comprehensive error page template
- Implemented different error messages for different scenarios
- Added proper exception handling throughout the application

## Installation & Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Court_enqiry
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install django selenium
```

4. **Download ChromeDriver**
- Download ChromeDriver matching your Chrome version
- Place in `Driver/chromedriver-win64/` directory

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Start the server**
```bash
python manage.py runserver
```

## Usage

1. Navigate to the application homepage
2. Select case type from dropdown
3. Enter case number and filing year
4. Submit the form
5. View extracted case information and order details

## Project Structure

```
Court_enqiry/
├── court_fetcher/          # Main Django app
│   ├── templates/          # HTML templates
│   ├── models.py          # Database models
│   ├── views.py           # Application logic
│   └── urls.py            # URL routing
├── Driver/                # ChromeDriver location
├── .venv/                 # Virtual environment
├── manage.py              # Django management script
└── .gitignore            # Git ignore rules
```

## Key Learnings

- **Selenium Best Practices**: Learned proper element interaction techniques for headless browsers
- **Django Development**: Gained experience with Django forms, templates, and ORM
- **Web Scraping Ethics**: Implemented respectful scraping with appropriate delays
- **Error Handling**: Developed comprehensive error management strategies
- **User Experience**: Created intuitive interfaces with proper feedback mechanisms

## Future Enhancements

- Add support for multiple court websites
- Implement caching for faster repeated searches
- Add export functionality for case data
- Implement user authentication and search history
- Add API endpoints for programmatic access

## Author

Built as a demonstration of web scraping and Django development capabilities.
