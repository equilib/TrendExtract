'''
@author: gevans
@date: 2018-08-17
@update: 2019-06-17


Copyright 2018 Evans, Gregory
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


import re
import json
import time

from src.Login import Login
from datetime import datetime, date

class TrendExtract:

    def __init__(self, uname : str, pword : str):
        '''

        '''
        self.__login = Login(uname, pword)

    def posix_timestamp(self, timestamp : datetime) -> str:
        '''
        @TODO: format timestamp to automatically set posix time to 13 digits
        @param: timestamp (str) - datetime object
        @return: timestamp (str) - unix milisecond timestamp
        '''
        return str( int( time.mktime(timestamp.timetuple()) * 1e3) )

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

    def format_base_url(self,
                        base_url : str,
                        dbid : str,
                        trend_name : str,
                        timestamp : str
                        ) -> str:
        '''
        '''
        # "http://63.227.116.65/_trendgraph/servlets/trenddata?sources=DBID%3A1%3A2289%3Achwr_temp&start=1534614000000&resolution=20093&withField=true"
        #
        # base_url = http://63.227.116.65 or something similar; complete url will be formatted as above
        timestamp = self.format_timestamp(timestamp)
        return "{0}/_trendgraph/servlets/trenddata?sources=DBID:1:{1}:{2}&start={3}&resolution=20093&withField=true".format(base_url, dbid, trend_name, timestamp)

    def format_raw_url(self,
                       raw_url : str,
                       dbid : str,
                       trend_name : str,
                       timestamp : str
                       ) -> str:
        '''
        format_raw_url: formats the raw url and populates with correct dbid and timestamp
                      - timestamp requires RH padding of three zeros to format correct url
                      - currently unk as to why (milliseconds?)
        @TODO: Rewrite to be generic for base class
        @param: raw_url (str) - raw url; example "http://63.227.116.65/_trendgraph/servlets/trenddata?sources=DBID:1:2289:chwr_temp&start=1534614000000&resolution=20093&withField=true"
        @param: dbid (str) - database id for trend
        @param: trend_name (str) - name of trend log associated with the database id
        @param: timestamp (str) - timestamp in unix time
        '''

        return self.format_url_trend_name(self.format_url_dbid(self.format_url_timestamp(raw_url, timestamp), dbid), trend_name)

    def format_url_timestamp(self, raw_url : str, timestamp : datetime) -> str:
        '''
        format_url_timestamp - returns raw_url formatted with new posix timestamp inserted
        @TODO: Rewrite to be generic for supperclass; keep for ALC class
        @param: raw_url (str) - raw url format for trend
        @param: timestamp (str) - datetime timestamp
        @return: (str) formatted url
        '''
        # convert timestamp to unix microsecond timestamp str
        if type(timestamp) is datetime:
            timestamp = self.format_timestamp(timestamp)

        # replace existing timestamp in raw_url string
        return raw_url.replace(re.search(r'(?<=\=)(?:\w+)(?=\&)', raw_url).group(0), timestamp)

    def format_url_dbid(self, raw_url : str, dbid : str) -> str:
        '''
        format_url_dbid - formats raw_url with new database id (dbid)
        @param: raw_url (str) - raw url format for trend
        @param: dbid (str) - database id string
        @return: (str) formatted url
        '''
        # replace dbid 4 digit number in url
        return raw_url.replace( re.search(r'(?<=\:)(?:\w{4})(?=\:)', raw_url).group(0), dbid)

    def format_url_trend_name(self, raw_url : str, trend_name : str) -> str:
        '''
        format_url_dbid - formats raw_url with new database id (dbid)
        @param: raw_url (str) - raw url format for trend
        @param: trend_name (str) - string containing the trend name
        @return: (str) formatted url
        '''
        # replace trend_name in url
        return raw_url.replace( re.search(r'(?<=\:)(?:\w+)(?=\&)', raw_url).group(0), trend_name)

    def open_url(self,
                 url : str
                 ) -> bool:
        '''
        open - returns True if response from webpage is 200\n
        @param: url (str) - formatted trend url containing proper dbid, trend_name, and posix timetamp (miliseconds)
        @returns: True if response == 200, False otherwise
        '''
        # initialize browser
        response = self.__login.init_browser(url)
        self.__json_data = response

    def get_trend_data(self) -> json:
        '''
        get_trend_data - returns a tuple of (json data, database ID, trend name)\n
        @param: None\n
        @returns: (json_data, DBID, trend_name)
        '''
        return self.__json_data

    def write_json_data(self, mode : str):
        '''
        write_json_data - writes json data, from GET request, to .json data file
                          data file name is formatted as <trend_name> <datetime>.json
        @TODO: Rewrite to be generic for superclass, but keep for ALC subclass
        @param: mode (str) - write 'w' or append 'a'
        @return: None
        '''
        try:
            # get filename from json data
            DBID = self.__json_data[0]['source'].split(':')[2]
            trend_name = self.__json_data[0]['source'].split(':')[3]
            # get current date and time
            datetime_now = str(datetime.now().strftime("%Y-%m-%d"))

            file_name = "DBID-{0}-{1}-{2}".format(DBID, trend_name, datetime_now)

            json.dump(self.__json_data, open(file_name + ".json", mode))
        except:
            print("Unable to write json datafile {}".format(trend_name))



class ALCTrendExtract( TrendExtract ):
    
    def __init__(self, uname, pword):
        '''
        '''
        super().__init__(uname, pword)


    def format_url_timestamp(self, raw_url : str, timestamp : datetime) -> str:
        '''
        format_url_timestamp - returns raw_url formatted with new posix timestamp inserted
        @TODO: Rewrite to be generic for supperclass; keep for ALC class
        @param: raw_url (str) - raw url format for trend
        @param: timestamp (str) - datetime timestamp
        @return: (str) formatted url
        '''
        # convert timestamp to unix microsecond timestamp str
        if type(timestamp) is datetime:
            timestamp = self.format_timestamp(timestamp)

        # replace existing timestamp in raw_url string
        return raw_url.replace(re.search(r'(?<=\=)(?:\w+)(?=\&)', raw_url).group(0), timestamp)

    def format_url_dbid(self, raw_url : str, dbid : str) -> str:
        '''
        format_url_dbid - formats raw_url with new database id (dbid)
        @param: raw_url (str) - raw url format for trend
        @param: dbid (str) - database id string
        @return: (str) formatted url
        '''
        # replace dbid 4 digit number in url
        return raw_url.replace( re.search(r'(?<=\:)(?:\w{4})(?=\:)', raw_url).group(0), dbid)

    def format_url_trend_name(self, raw_url : str, trend_name : str) -> str:
        '''
        format_url_dbid - formats raw_url with new database id (dbid)
        @param: raw_url (str) - raw url format for trend
        @param: trend_name (str) - string containing the trend name
        @return: (str) formatted url
        '''
        # replace trend_name in url
        return raw_url.replace( re.search(r'(?<=\:)(?:\w+)(?=\&)', raw_url).group(0), trend_name)

    def write_json_data(self, mode : str):
        '''
        write_json_data - writes json data, from GET request, to .json data file
                          data file name is formatted as <trend_name> <datetime>.json
        @TODO: Rewrite to be generic for superclass, but keep for ALC subclass
        @param: mode (str) - write 'w' or append 'a'
        @return: None
        '''
        try:
            # get filename from json data
            DBID = self.__json_data[0]['source'].split(':')[2]
            trend_name = self.__json_data[0]['source'].split(':')[3]
            # get current date and time
            datetime_now = str(datetime.now().strftime("%Y-%m-%d"))

            file_name = "DBID-{0}-{1}-{2}".format(DBID, trend_name, datetime_now)

            json.dump(self.__json_data, open(file_name + ".json", mode))
        except:
            print("Unable to write json datafile {}".format(trend_name))