#!/usr/bin/env python

# Grade parser: Gets grades from SIS from the most recent semester and prints
# them out.
# Zach Kirsch | December 2016
#
# Dependencies:
#   Selenium (pip install selenium)
#   PhantomJS (http://phantomjs.org/download.html)
#   Firefox
#
# Usage: python parseGrades.py <username> <password file>

###############################################################################
###############################################################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException
import time
import datetime
import sys
import os.path

###############################################################################
###############################################################################

# Constants

delay = 30  # will wait this many seconds before timing out
login_url = ("https://sis.uit.tufts.edu/psp/paprod/EMPLOYEE/EMPL/h/" +
             "?tab=PAPP_GUEST#")
dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
sis_url = ("https://sis.uit.tufts.edu/psp/paprod/EMPLOYEE/EMPL/h/?tab=DEFAULT" +
           "&tm=" + dt + "#1")

path_to_phantomjs_binary = './phantomjs'
path_to_geckodriver_binary = './geckodriver'
path_to_firefox_binary = './firefox'

###############################################################################
###############################################################################


# Fill out forms and login to site
def login(driver):
    username = driver.find_element_by_name('userid')
    password = driver.find_element_by_name('pwd')
    username.send_keys(USER)
    password.send_keys(PASS)
    password.send_keys(Keys.RETURN)

    # see if it worked
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                                              (By.CLASS_NAME, 'tfp_mp_slide')))
    except TimeoutException:
        print "Error logging in"
        sys.exit(1)


# get grades
def get_grades(driver):
    grades_table = driver.find_elements(By.TAG_NAME, "table")[11]
    courses = grades_table.find_elements(By.TAG_NAME, "tr")
    for course in courses:
        details = course.find_elements(By.TAG_NAME, "td")

        # makes sure it's a grade row
        if len(details) != 7:
            continue

        course_name = details[0].text
        prof = details[2].text
        grade = details[3].text
        grading_basis = details[5].text
        graded = grading_basis in ["Graded", "P/NP"]

        # only print graded courses
        if not graded:
            continue

        print grade.ljust(2) + " in " + course_name + " (" + prof + ")"


# waits for element to appear
def wait_for_element(elem):
    try:
        located = EC.presence_of_element_located(elem)
        WebDriverWait(driver, delay).until(located)
    except:
        print "Timeout"
        sys.exit(1)

###############################################################################
###############################################################################

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: {} <username> <password file>".format(sys.argv[0]))
        exit(1)

    USER = sys.argv[1].upper()
    with open(sys.argv[2]) as f:
        PASS = f.readline().rstrip("\n")

    # Initialize and load the web page
    driver = webdriver.PhantomJS(executable_path=path_to_phantomjs_binary,
                                 service_log_path=os.path.devnull,
                                 service_args=['--ignore-ssl-errors=true'])
    driver.set_window_size(2400,2000)

    # firefox_binary = FirefoxBinary(path_to_firefox_binary)
    # driver = webdriver.Firefox(executable_path=path_to_geckodriver_binary,
    #                           firefox_binary=firefox_binary)

    try:
        driver.get(login_url)
        wait_for_element((By.NAME, 'userid'))

        login(driver)

        # after logged in, go to sis grades url
        driver.get(sis_url)

        # go back a semester
        wait_for_element((By.ID, 'tfp_grades_lft_arrow'))
        back_arrow = driver.find_element_by_id('tfp_grades_lft_arrow')
        back_arrow.click()

        # wait for slide transition
        time.sleep(2)

        get_grades(driver)

    finally:
        driver.close()
        driver.quit()
