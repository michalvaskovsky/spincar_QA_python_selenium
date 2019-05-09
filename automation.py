# -*- coding: utf-8 -*-

# imports
import string
import random
import exception_handler
from downloader_selenium import DownloaderSelenium
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# switches
HEADLESS_MODE = False

class Automation():

    def __init__(self, username, password, objectid=0):
        self.objectid = objectid
        self.loginurl = 'https://test-selenium-manager.spincar.com'
        self.username = username
        self.password = password
        self.init_driver()

    def __del__(self):
        self.driver.quit()

    def is_visible_by_x(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))

    def is_visible_by_no_raise_by_x(self, locator, timeout=10):
        try:
            return self.is_visible_by_x(locator, timeout)
        except Exception:
            return None

    def is_visible_by_id(self, id, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, id)))

    def is_visible_by_name(self, name, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.NAME, name)))

    def is_checked_by_name(self, name):
        return self.driver.find_element_by_name(name).is_selected()

    def click_javascript_by_x(self, locator):
        '''
        Click by executing a javascript when normal element.click() doesn't work
        :param locator: element locator 
        :return: None
        '''
        elem = self.driver.find_element_by_xpath(locator)
        self.driver.execute_script("arguments[0].click();", elem)

    def init_driver(self):
        ds = DownloaderSelenium()
        self.driver = ds.driverInitChrome()
        '''
        self.driver = ds.driverInitEx(
            headless=HEADLESS_MODE,
            images=True,
            download_dir=None
        )
        '''

    def generate_user(self, size=10, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def handle_login(self):

        try:
            self.driver.get(self.loginurl)

            # wait for the site
            e_user = self.is_visible_by_id('email', 30)
            e_pass = self.driver.find_element_by_id('password')
            e_user.send_keys(self.username)
            e_pass.send_keys(self.password)
            e_pass.submit()

            # wait for login operation to finish and check if was successfull
            self.is_visible_by_id('navbar-customer-menu', 30)

            return True

        except Exception as e:
            print ('Login error. Message={}'.format(e))
            return False

    "TEST 3.B"
    def register_test_blank(self):
        '''
        3.b. Test the form’s validation by leaving each required field (indicated by an asterisk) blank 
            and verifying that the expected error message is displayed.
        :return: True/False -> Test succeeded/failed, error_message 
        '''

        result = False
        message = ''
        try:
            # click admin in top menu
            self.driver.find_element_by_xpath('//*/a[contains(text(), "Admin")]').click()

            # click onboard section
            self.driver.find_element_by_xpath('//*/a[contains(text(), "Onboard")]').click()

            # click the create customer button
            button = self.is_visible_by_x('//*/input[contains(@value, "Create")]', 20)
            button.click()

            # check errors
            '''
            <ul id="errors" style="display: block;">
            <li>Customer name required</li>
            <li>S3 folder required</li>
            <li>Invalid email address</li></ul>
            '''
            lis = self.driver.find_element_by_id('errors').find_elements_by_tag_name('li')
            if len(lis) != 3:
                raise Exception("expected error message is missing")

            error_messages = [li.text for li in lis]
            expected_messages = [
                'Customer name required', 'S3 folder required', 'Invalid email address'
            ]
            for e in expected_messages:
                if not e in error_messages:
                    raise Exception("expected error message is missing. missing={}".format(e))

            result = True

        except Exception as e:
            message = exception_handler.generic_exception_handler_s(e, exception_handler.func_name())

        return result, message

    # TEST 3.C
    def register_test_normal(self):
        '''
        c. Fill out all fields with valid values and submit the form. This will create a Customer record.
          Upon submitting the form, you’ll be taken to a new page with the option to Select an existing config.
          Disregard this page, it is not relevant to the test.
        :return: status, error_message
        '''

        self.test_username = 'user_{}'.format(self.generate_user())

        result = False
        message = ''
        try:
            # click admin in top menu
            self.driver.find_element_by_xpath('//*/a[contains(text(), "Admin")]').click()

            # open onboard section
            self.driver.find_element_by_xpath('//*/a[contains(text(), "Onboard")]').click()

            # set username and userdir
            self.driver.find_element_by_id('lastpass-disable-search-u').send_keys(self.test_username) # customer name
            self.driver.find_element_by_id('lastpass-disable-search-s').send_keys(self.test_username) # s3 folder

            # click the create customer button
            button = self.is_visible_by_x('//*/input[contains(@value, "Create")]', 20)
            button.click()

            # did we proceed to the create config page ?
            self.is_visible_by_x('//*/input[contains(@value, "Config")]', 20)

            result = True
        except Exception as e:
            message = exception_handler.generic_exception_handler_s(e, exception_handler.func_name())

        return result, message

    # TEST 4 a,b,c
    def verify_customer_created(self):
        '''
        c. Locate the Customer you added in step 3.
          Tip: The most recently added Customer will have the largest ID.
          You can sort the list of users in ascending or descending order by clicking the column header Id.
        :return: status, error_message/url to customer edit section on success
        '''

        status = False
        try:
            # click admin in top menu
            self.driver.find_element_by_xpath('//*/a[contains(text(), "Customers")]').click()

            # customers list
            self.driver.find_element_by_xpath('//*/ul/li/a[contains(text(), "List")]').click()

            # wait for table to load
            table = self.is_visible_by_x('//*/table', 20)

            # check if user was created
            #names = [tr.get_attribute('data-name') for tr in table.find_elements_by_tag_name('tr')]
            #status = self.test_username in names

            elems = self.driver.find_elements_by_xpath('//*/tr[@data-name="{}"]'.format(self.test_username))
            if len(elems) == 0:
                raise Exception('Username={} missing in user list'.format(self.test_username))

            # get the user edit url
            message = elems[0].find_element_by_tag_name('a').get_attribute('href')
            status = True

        except Exception as e:
            message = exception_handler.generic_exception_handler_s(e, exception_handler.func_name())

        return status, message

    def verify_customer_data(self, customer_url):
        '''
        e. Verify that the fields of the Customer record have the values you entered in step
            3. These fields should have the expected values:
                i. Name     
                ii. S3 folder
            f. These fields should have default values:
            f.i. Max Size should have the value 640.
            f.ii. Pano Max Size should have the value 1712.
            f.iii. The Spin customer checkbox should be checked.
        :param customer_url: url to customer edit section 
        :return: status, error_message
        '''

        message = ''
        status = False
        try:
            # open customer edit section
            self.driver.get(customer_url)

            name = self.is_visible_by_name('name', 20)

            # check name.text and self.test_username
            n = name.get_attribute('value')
            if n != self.test_username:
                raise Exception("Name field is not equal to test_username. Name={} test_username={}"
                                .format(n, self.test_username))

            # check S3 folder max size 640
            check = self.driver.find_element_by_name('max_size').get_attribute('value')
            if check != '640':
                raise Exception("Improper Max Size value. value={} Supposed to be=640".format(check))

            # check if pano_max_size is 1712
            check = self.driver.find_element_by_name('pano_max_size').get_attribute('value')
            if check != '1712':
                raise Exception("Improper Pano max size value. value={} Supposed to be=1712".format(check))

            # check checkbox is_spin_customer is checked
            checked = self.is_checked_by_name('is_spin_customer')
            if not checked:
                raise Exception("Spin customer is NOT Checked")

            status = True

        except Exception as e:
            message = 'Exception. e={}'.format(e)

        return status, message

    def run_test(self):

        status = self.handle_login()
        print ("handle_login() status={}".format(status))
        if not status:
            return

        # 3.B
        result, error_message = self.register_test_blank()
        print ("Test 3.B. status={} message={}".format(result, error_message))

        # 3.C
        result, error_message = self.register_test_normal()
        print ("Test 3.C. status={} message={}".format(result, error_message))
        if not result:
            return

        # if OK 3C
        print ('Added customer. customer name={}'.format(self.test_username))

        # 4.B
        result, error_message = self.verify_customer_created()
        print ("Test 4.B. status={} message={}".format(result, error_message))
        if not result:
            return

        # 4.C
        # error_message contains url to the customer information section
        result, error_message = self.verify_customer_data(error_message)
        print ("Test 4.B. status={} message={}".format(result, error_message))
        if not result:
            return

        print ("Finished")

