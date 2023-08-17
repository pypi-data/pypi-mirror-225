#!/usr/bin/env python

import sys
import random

sys.path.append('..')


def get_random_user_agent():
    """Generates random user agent."""

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.64 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.34',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.34',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    ]

    return random.choice(user_agents)


def get_driver_dict(driver_path, 
                    options, 
                    args):
    """Gets the driver parameters dictionary.
    
    Args:
        driver_path (str): path to the driver.
        options (dict): options of the driver.
        args (dict): parsed arguments.

    Returns:
        dict, Driver parameters dictionary.
    """

    return {
        'driver_path': driver_path,
        'options': options,
        'headless': args.headless,
        'delete_cookies': args.delete_cookies,
    }


def quit_driver(driver, 
                delete_cookies):
    """Quit the driver.

    Args:
        driver (WebDriver): selenium webdriver.
        delete_cookies (bool): to delete cookies or not.
    """
    
    try:
        driver.quit()
        if delete_cookies:
            driver.delete_all_cookies()
    except Exception as e:
        print(f"[LOG] [EXCEPTION]\n{e}")
