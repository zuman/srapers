import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

date_format = "%d/%m/%Y"

def extract_date(value):
    try:
        date = datetime.strptime(value.split()[-1], date_format)
        return date
    except ValueError:
        return datetime.max

def wait_and_click_element(by, e, time=10):
    wait = WebDriverWait(driver, time)
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//ngx-ui-loader/div")))
    element = wait.until(EC.element_to_be_clickable((by, e)))
    if not element.is_displayed():
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()

# Step 1: Log in to the login page
def login(username, password):
    driver.get("https://visa.vfsglobal.com/ind/en/deu/login")
    wait_and_click_element(By.ID, "onetrust-reject-all-handler")
    driver.find_element(by=By.ID, value='mat-input-0').send_keys(username)
    driver.find_element(by=By.ID, value='mat-input-1').send_keys(password)
    wait_and_click_element(By.CSS_SELECTOR, "form>button", 15)

# Step 2: Click on the button "Start New Booking"
def start_new_booking():
    wait_and_click_element(By.CSS_SELECTOR, "section>div>div>button")

# Step 2.1: Get all Visa Centers
def get_all_visa_centres():
    all_centers=[]
    wait_and_click_element(By.ID, "mat-select-0")
    visa_centers = driver.find_elements(by=By.XPATH, value="//mat-option[@role='option']")
    center = None
    for center in visa_centers:
        if "Visa Application" in center.text:
            all_centers.append(center.text)
    if center:
        driver.execute_script("arguments[0].scrollIntoView();", center)
        center.click()
    return all_centers


# Step 3: Repeat the process for all visa application centers
def booking_process():
    all_centers = get_all_visa_centres()
    values = {}
    # Step 3.1: Select a value which has "Visa Application Centre" substring in it
    for current_center in all_centers:
        try:
            wait_and_click_element(By.ID, "mat-select-0")
            visa_centers = driver.find_elements(by=By.XPATH, value="//mat-option[@role='option']")
            center = None
            for listed_center in visa_centers:
                if listed_center.text == current_center:
                    center = listed_center
                    break
            if center:
                driver.execute_script("arguments[0].scrollIntoView();", center)
                center.click()
            wait_and_click_element(By.ID, "mat-select-value-3")
            select = driver.find_elements(by=By.XPATH, value="//mat-option[@role='option']")

            # Step 3.2: Select the value which has "Schengen Visa" substring in it
            for opt in select:
                if "Schengen Visa" in opt.text:
                    driver.execute_script("arguments[0].scrollIntoView();", opt)
                    opt.click()
                    wait_and_click_element(By.ID, "mat-select-value-5")
                    subcats = driver.find_elements(by=By.XPATH, value="//mat-option[@role='option']")

                    # Step 3.3: Select the value "business"
                    for subcat in subcats:
                        if "business" in subcat.text:
                            driver.execute_script("arguments[0].scrollIntoView();", subcat)
                            subcat.click()
                            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, "//ngx-ui-loader/div")))

                            # Step 3.4: Record the application center and date from the alert
                            alert = driver.find_element(by=By.XPATH, value="//form/div/div[@class='alert alert-info border-0 rounded-0']")
                            key=current_center.split("-")[0].strip()
                            values[key] = alert.text
                            print(key, "=", values[key])
                            break
                    break
        except Exception as e:
            print("Some error occured while checking date for", current_center)
            print(str(e))
            continue   
    return values

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", required=True, help="Email address")
    parser.add_argument("-p", "--password", required=True, help="Password")
    args = parser.parse_args()

    driver = webdriver.Chrome()
    browsers = [webdriver.Firefox, webdriver.Chrome, webdriver.Safari, webdriver.Edge]
    for browser in browsers:
        try:
            driver = browser()
            break
        except:
            continue
    driver.delete_all_cookies()

    login(args.email, args.password)
    start_new_booking()
    print("\nScraping...")
    values = booking_process()

    # Step 4: Print the collected values
    print("\n\nSorted dates:")
    sorted_dict = {k: extract_date(v).strftime(date_format) for k, v in sorted(values.items(), key=lambda item: extract_date(item[1]))}
    for key in sorted_dict:
        print(key, ":", sorted_dict[key])

    driver.quit()
