from datetime import date, datetime, timedelta, timezone
import pandas
import singer
import urllib.request
import json
import requests
import pytz
from dateutil import parser
from config import *

#Generates list of dates from 1st Jan 2020 to yesterday
def list_of_dates():
    start_date = date(2020,1,1)   # start date
    today = date.today()
    end_date = today - timedelta(days = 1)
    date_list = pandas.date_range(start_date,end_date,freq ='d').strftime("%Y-%m-%d").tolist()
    return date_list

#Converts UTC to IST
def convert_utc_to_ist(date_string,time_string):
    date_time = parser.parse(date_string+" "+time_string)
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_time = date_time.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
    return ist_time.strftime("%I:%M:%S %p")

#Receives data from API endpoint
def receive_api_response(target_date):
    with requests.get(BASE_URL + "?lat=" + SOURCE_LATITUDE + "&lng=" + SOURCE_LONGITUDE + "&date=" + target_date) as response:

        sun_rise_set_data = response.content.decode('utf-8')
        sun_rise_set_data = json.loads(json.dumps(sun_rise_set_data))
        sun_rise_set_data = json.loads(sun_rise_set_data)

    return sun_rise_set_data
    
#Loads sunrise-sunset data from https://sunrise-sunset.org/api
def collect_sunrise_sunset_data():
    sunrise_set_records = []
    date_list = list_of_dates()
    for i in range(len(date_list)):
        sun_rise_set_data=receive_api_response(date_list[i])
        sunrise_set_records.append({"sunrise":convert_utc_to_ist(date_list[i],sun_rise_set_data["results"]["sunrise"]),
                            "sunset":convert_utc_to_ist(date_list[i],sun_rise_set_data["results"]["sunset"]),
                            "timestamp":date_list[i]})
    #Append todays data
    today = date.today().strftime("%Y-%m-%d")
    sunrise_sunset_data_today = receive_api_response(today)
    sunrise_set_records.append({"sunrise":convert_utc_to_ist(today,sunrise_sunset_data_today["results"]["sunrise"]),
                            "sunset":convert_utc_to_ist(today,sunrise_sunset_data_today["results"]["sunset"]),
                            "timestamp":today})
    return sunrise_set_records
    
#Writes to the target
def write_to_target(sunrise_set_records):
    singer.write_schema('sunrise_sunset', SCHEMA, 'timestamp')
    singer.write_records('sunrise_sunset', records = sunrise_set_records)

#Driver 
if __name__=="__main__":
    sunrise_set_records = collect_sunrise_sunset_data()
    write_to_target(sunrise_set_records)