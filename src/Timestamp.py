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

import json, time

from datetime import datetime, date

class Timestamp:
'''
Timestamp - utility class to format posix timestamps based in seconds or miliseconds
and convert to human readable timestamp
'''
    def __init__(self):
        pass

    def posix_timestamp(self, timestamp : datetime) -> str:
                '''
        @TODO: format timestamp to automatically set posix time to 13 digits
        @param: timestamp (str) - datetime object
        @return: timestamp (str) - unix milisecond timestamp
        '''
        return str( int( time.mktime(timestamp.timetuple()) * 1e3) )pass

    def format_timestamp(self, timestamp : datetime) -> str:
        '''
        format_timestamp - converts datetime object to unix milisecond timestamp
        @param: timestamp (datetime)
        @return: timestamp (str) - unix milisecond timestamp
        '''

        if type(timestamp) is datetime:
            timestamp = self.posix_timestamp(timestamp)
        return timestamp

    def human_readable_timestamp(self, timestamp : str) -> str:
        '''
        human_readable_timestamp - accepts as string posix timestamp and converts to human readable datetime string
        @TODO: modify to check for seconds or miliseconds and convert accordingly
        @param: timestamp (str) - posix timestamp
        @return: (str) human readable format
        '''
        human_readable = ""
        if len(timestamp) == 13: #miliseconds
            human_readable = datetime.fromtimestamp( int(timestamp) / 1e3)
        elif len(timestamp) == 10: #seconds
            human_readable = datetime.fromtimestamp( int(timestamp) )

        return str( human_readable.strftime('%Y-%m-%d %H:%M:%S') )