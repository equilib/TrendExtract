'''
@author: gevans
@date: 2019-06-19


Copyright 2018 Evans, Gregory
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import mechanicalsoup
import json

class Login:

    def __init__(self, uname : str, pword : str):
        '''
        __init__

        @param: uname (str) - username
        @param: pword (str) - password
        '''
        self.__set_uname(uname)
        self.__set_pword(pword)
        self.__uname_form_field = "j_username"
        self.__pword_form_field = "j_password"
        self.__json_data = None
        self.__browser = mechanicalsoup.StatefulBrowser()

        self.__count = 0


    def __set_uname(self, uname : str): self.__uname = uname

    def __set_pword(self, pword : str): self.__pword = pword

    def init_browser(self, url : str) -> json:

        '''
        __init_browser - initalizes browser with url, uname, and pword

        @param: url (str) - formatted url
        '''
        try:
            response = self.__browser.open(url)
        except:
            print("Error opening url {0}".format(url))

        # if the initialization count = 0 or the response is not OK -> AUTH
        if self.__count == 0 or not response.ok:

            self.__browser.select_form()
            # print(self.__browser.get_current_page())
            # init browser login form fields with uname / pword data
            self.__browser[self.__uname_form_field] = self.__uname
            self.__browser[self.__pword_form_field] = self.__pword
            response = self.__browser.submit_selected()

            self.__count += 1

        return response.json()


    def update_uname(self, uname : str): self.__set_uname(uname)

    def update_pword(self, pword : str): self.__set_pword(pword)