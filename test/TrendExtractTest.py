'''
@author: gevans
@date: 2018-09-04


Copyright 2018 Evans, Gregory

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

'''
@TODO: add tests for Timestamp, Extract, Login, and TrendExtract classes
'''

import sys

sys.path.append('../')

from TrendExtract.src.TrendExtract import TrendExtract
from datetime import date
from getpass import getpass

import os
import time

def list_dir_files(directory : str, suffix : str) -> list:
    '''
    '''
    return [el for el in os.listdir(directory) if el.endswith("txt")]
    

def get_trend_urls(directory : str, file_name : str) -> list:
    '''
    '''
    with open(directory + "/" + file_name) as f:
        return [el for el in f]

def main():

    usr = input("Enter username: ")

    pwd = getpass("Enter password: ")

    trend_date = input("Enter start date for trend (YYYY-MM-DD): ")

    year, month, day = [ int(v) for v in trend_date.split("-") ]

    alcTrend = TrendExtract(usr, pwd)
    
    ip_addr = "127.0.0.1"
    
    base_url = "http://" + ip_addr + "/_trendgraph/servlets/"
    # dbid = "3262"
    # trend_name = "ahu_flo_err_tn"

    posix_timestamp = alcTrend.posix_timestamp( date(year, month, day) )

    files = list_dir_files("./urls", "txt")
        
    for file in files:
        # get list of trend_urls
        trend_urls = get_trend_urls("./urls", file)

        for url in trend_urls:
            url = alcTrend.format_url_timestamp(base_url + url, posix_timestamp)
            try:
                alcTrend.open_url(url)
                time.sleep(1)
                alcTrend.write_json_data('w')
            except: 
                print("Issue opening url {0}".format(url))


if __name__ == "__main__":
    main()
