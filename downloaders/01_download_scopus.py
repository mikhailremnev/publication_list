#!/usr/bin/env python3

################################################
# NOTE: This has to be done through institution network (or through a proxy)
# Otherwise, full scopus data will not be available
# See WEBDRIVER OPTIONS section below to set up a proxy
################################################

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# https://www.browserstack.com/guide/selenium-wait-for-page-to-load
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By

import time

# For saving CSV file
import tempfile
from pathlib import Path

################################################
# GENERAL PARAMETERS

scopus_id = 57219793453
url = f'https://www.scopus.com/authid/detail.uri?authorId={scopus_id}'

################################################
# WEBDRIVER OPTIONS
################################################

# https://www.selenium.dev/documentation/webdriver/capabilities/
options = Options()
# options.add_argument('-headless')

#=== Proxy setup
# options.set_preference('network.proxy.type', 1)
# options.set_preference("network.proxy.socks", "localhost");     
# options.set_preference("network.proxy.socks_port", 9200);

tmp_dir = tempfile.TemporaryDirectory()
options.set_preference('browser.download.folderList', 2) # custom location
options.set_preference('browser.download.manager.showWhenStarting', False)
options.set_preference('browser.download.dir', tmp_dir.name)
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')

s = Service('./geckodriver')
driver = Firefox(service=s, options=options)
wait = WebDriverWait(driver, timeout=15)

################################################
# LOADING PAGE
################################################

driver.get(url)

wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
print('Page loaded')
time.sleep(2)

driver.execute_script("window.scrollBy(0, document.body.scrollHeight)");
print('Scrolled to the bottom of webpage')

# Looks like it takes some time to scroll to the bottom
time.sleep(2)

selector = (By.XPATH, "//button/span[contains(text(), 'Export all')]")
wait.until(expected.element_to_be_clickable(selector)).click()
print('Clicked to export all publications')

selector = (By.XPATH, "//button/span[contains(text(), 'Plain text')]")
wait.until(expected.element_to_be_clickable(selector)).click()
print('Selected TXT format')

selector = (By.XPATH, '//button/span/div[text() = "Export"]')
driver.find_element(*selector).click()
print('Initiated file saving')

time.sleep(5)

def is_download_finished(download_path):
    """Check if download has been finished.
    Source: https://stackoverflow.com/a/53602937
    """
    firefox_temp_file = sorted(Path(download_path).glob('*.part'))
    if len(firefox_temp_file) > 0: return False
    # chrome_temp_file = sorted(Path(temp_folder).glob('*.crdownload'))
    # if len(chrome_temp_file) == 0: return False
    # downloaded_files = sorted(Path(temp_folder).glob('*.*'))
    # if len(downloaded_files) >= 1: return False

    return True

while not is_download_finished(tmp_dir.name):
    time.sleep(0.1)

scopus = open(f'{tmp_dir.name}/scopus.txt').read()
open('scopus.txt', 'w').write(scopus)
print('Results have been saved to scopus.txt')

driver.quit()

