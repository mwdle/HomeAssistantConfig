"""
Native Python module for Selenium operations.
This runs outside the Pyscript interpreter to avoid Selenium import issues, but remains accessible for import within Pyscripts for interacting with HA
See:
 - https://hacs-pyscript.readthedocs.io/en/latest/reference.html#avoiding-event-loop-i-o
 - https://hacs-pyscript.readthedocs.io/en/latest/reference.html#importing
"""
import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_chrome_options():
    """Get configured Chrome options for headless browsing"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors") # Some routers enable https with self signed certificates on the web interface -- this will allow such connections
    return chrome_options


def create_webdriver():
    """Create and return a configured WebDriver instance"""
    chrome_options = get_chrome_options()
    return webdriver.Remote(
        command_executor="http://Chrome:4444/wd/hub", # Connect to selenium/standalone-chrome container via Docker network -- See `compose.yaml`
        options=chrome_options
    )


def find_extender_ip():
    """Scans the local network to find the TP-Link extender web interface."""
    for i in range(2, 255):
        address = f"http://192.168.0.{i}"
        try:
            response = requests.get(address, timeout=0.5)
            if response.status_code == 200 and "tp-link" in response.text.lower():
                return address
        except requests.exceptions.RequestException:
            continue
    return None


# Compatible with Arris SURFboard G54 router, but can be easily adapted to work for the web interface on your router if you are familiar with inspecting webpages using developer tools.
def reboot_router():
    """
    Performs the router reboot using selenium.
    Returns a tuple: (success: bool, message: str)
    """
    # Get router password from environment -- see `compose.yaml`
    router_password = os.getenv("ROUTER_PASSWORD")
    if not router_password:
        return False, "ROUTER_PASSWORD environment variable not set"

    driver = None
    try:
        driver = create_webdriver()
        wait = WebDriverWait(driver, 10)
        driver.get("https://192.168.0.1/cgi-bin/luci/admin/troubleshooting/restart")
        password_field = wait.until(EC.element_to_be_clickable((By.NAME, "luci_password")))
        password_field.send_keys(router_password)
        login_button = driver.find_element(By.ID, "loginbtn")
        login_button.click()
        reboot_button = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "RESTART GATEWAY")))
        reboot_button.click()
        wait.until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        time.sleep(5) # Give some time for it to process
        return True, "Router reboot command sent successfully"

    except Exception as e:
        return False, f"Failed to reboot router: {str(e)}"

    finally:
        if driver:
            driver.quit()


# Compatible with TP-Link RE650 extender, but can be easily adapted to work for the web interface on your router if you are familiar with inspecting webpages using developer tools.
def reboot_extender():
    """
    Performs the extender reboot using selenium.
    Returns a tuple: (success: bool, message: str)
    """
    # Get extender password from environment -- see `compose.yaml`
    extender_password = os.getenv("EXTENDER_PASSWORD")
    if not extender_password:
        return False, "EXTENDER_PASSWORD environment variable not set"
    
    extender_ip = find_extender_ip()
    if not extender_ip:
        return False, "Could not find extender IP"
    
    driver = None
    try:
        driver = create_webdriver()
        wait = WebDriverWait(driver, 10)
        driver.get(extender_ip)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "password-text"))).send_keys(extender_password)
        driver.find_element(By.ID, "login-btn").click()
        wait.until(EC.element_to_be_clickable((By.ID, "top-control-reboot"))).click()
        ok_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".msg-btn-container .btn-msg-ok")))
        ok_button.click()
        return True, "Extender reboot command sent successfully"
    
    except Exception as e:
        return False, f"Failed to reboot extender: {str(e)}"

    finally:
        if driver:
            driver.quit()
