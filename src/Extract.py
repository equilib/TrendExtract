'''
@author: gevans
@date: 2020-07-16


Copyright 2020 Evans, Gregory
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import json, time, requests


class Extract:
'''
'''

    def __init__(self,
                 url = None
                 ):

        self.__url = url if (url != None) else ""

        self.__login = Login


    def open_url(self, 
                url : str
                ) -> bool:
        '''
        open_url - returns True if response from webpage is 200\n
        @param: url (str) - url where json data is located
        @returns: True if response == 200, False otherwise
        '''

        try:
            request = requests.get(url)


        
    def write_json_data(self,
                        mode : str):
        pass

    
