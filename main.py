# -*- coding: utf-8 -*-
from automation import Automation

def main():
    a = Automation(username='tester1@spincar.com', password='password')
    a.run_test()

main()
