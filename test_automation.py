# -*- coding: utf-8 -*-

from automation import Automation
import unittest

class Test_Automation(unittest.TestCase):

    def test_login(self):

        # test login with improper credentials
        a = Automation(username='', password='')
        res1 = a.handle_login()
        assert not res1
        print (res1)

        # test login with proper credentials
        a = Automation(username='tester1@spincar.com', password='password')
        res2 = a.handle_login()
        assert res2
        print (res2)

    def test_3b(self):
        a = Automation(username='tester1@spincar.com', password='password')
        res = a.handle_login()
        assert res

        result, error_message = a.register_test_blank()
        print ("Test 3.B. status={} message={}".format(result, error_message))
        assert result

    def test_3c(self):
        a = Automation(username='tester1@spincar.com', password='password')
        res = a.handle_login()
        assert res

        result, error_message = a.register_test_normal()
        print ("Test 3.C. status={} message={}".format(result, error_message))
        assert result
        print ("Added username={}".format(a.test_username))

    def test_4b(self):

        a = Automation(username='tester1@spincar.com', password='password')
        res = a.handle_login()
        assert res

        a.test_username = 'user_2putziwpd4'
        result, error_message = a.verify_customer_created()
        print ("Test 4.B. status={} message={}".format(result, error_message))
        assert result
        assert error_message == 'https://test-selenium-manager.spincar.com/my-customer/edit/4182?_acid=f64'

    def test_4c(self):
        a = Automation(username='tester1@spincar.com', password='password')
        res = a.handle_login()
        assert res

        a.test_username = 'user_2putziwpd4'
        url = 'https://test-selenium-manager.spincar.com/my-customer/edit/4182?_acid=f64'
        result, error_message = a.verify_customer_data(url)
        print ("Test 4.C. status={} message={}".format(result, error_message))
        assert result




