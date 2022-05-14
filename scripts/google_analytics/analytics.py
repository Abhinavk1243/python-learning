from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
# from google.appengine.ext import vendor
import pandas as pd
import urllib.parse
import argparse
import httplib2
import requests
import json
import csv

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'analytics-329707-cc4a4b4967b5.json'
# VIEW_ID = '3009716598'
VIEW_ID = '253803495'
# VIEW_ID ='2198273707'
# VIEW_ID  = '92320289'

def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)
  analytics = discovery.build('analyticsreporting', 'v4', credentials=credentials)
  return analytics


from googleapiclient.discovery import build
from oauth2client import tools, client, file
import json
 
 
def get_access_token():
    with open('analytics.dat') as json_file:
        data = json.load(json_file)
        access_token = data["access_token"]
    return access_token
 
def get_service(api_name, api_version, scope, client_secret):
 
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, parents=[tools.argparser])
    flags = parser.parse_args([])
 
    flow = client.flow_from_clientsecrets(client_secret, scope=scope, message=tools.message_if_missing(client_secret))
 
    storage = file.Storage(api_name + '.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())
 
    service = build(api_name, api_version, http=http)
 
    return service
 
 
def get_first_profile_id(service):
    accounts = service.management().accounts().list().execute()
    if accounts.get('items'):
        account = accounts.get('items')[0].get('id')
 
        properties = service.management().webproperties().list(accountId=account).execute()
 
        if properties.get('items'):
            prop = properties.get('items')[0].get('id')
            profiles = service.management().profiles().list(accountId=account,webPropertyId=prop).execute()
 
            if profiles.get('items'):
                return profiles.get('items')[0].get('id')
 
    return None


def generate_uri(scope, view_id, start_date, end_date, metrics, dimensions, filters):
    access_token = get_access_token()
    max_results = 10000
    query_uri = scope \
                + 'ids=' + urllib.parse.quote_plus(view_id) \
                + '&start-date=' + start_date \
                + '&end-date=' + end_date \
                + '&metrics=' + urllib.parse.quote_plus(','.join(metrics)) \
                + '&dimensions=' + urllib.parse.quote_plus(','.join(dimensions)) \
                + '&filters=' + urllib.parse.quote_plus(','.join(filters)) \
                + '&max-results=' + str(max_results) \
                + '&access_token=' + access_token
    return query_uri
 
 
def return_uri(view_id, start_date, end_date, metrics, dimensions, filters):
    scope = 'https://www.googleapis.com/analytics/v3/data/ga?'
    query_uri = generate_uri(scope, view_id, start_date, end_date, metrics, dimensions, filters)
    return query_uri


 
 
def save_output_file(uri, file_name):
    file_path = '<Enter you file location>' + file_name
    request = requests.get(uri)
    json_data = json.loads(request.text)
    column_header = json_data["columnHeaders"]
    header_list = []
    for header in range(len(column_header)):
        header_list.append(column_header[header]["name"])
    write_file = open(file_path, 'w', newline='')
    csv_writer = csv.writer(write_file)
    csv_writer.writerow(header_list)
    write_file.close()
 
    ga_data = json_data["rows"]
    append_file = open(file_path, 'a', newline='')
    row_write = csv.writer(append_file)
    for i in ga_data:
        row_write.writerow(i)
    append_file.close()
    
    
# from URITemplate import return_uri
# from GoogleAuthentication import get_service, get_first_profile_id
# from SaveCSVFile import save_output_file
 
 
def main():
    scope = ['https://www.googleapis.com/auth/analytics.readonly']
    service = get_service('analytics', 'v3', scope, 'analytics-329707-cc4a4b4967b5.json')
    get_first_profile_id(service)
 
    uri = return_uri('ga:253803495', '2daysAgo', 'today',
                    ['ga:totalEvents'],
                    [ 'ga:eventLabel', 'ga:date'],
                    ['ga:eventCategory==StudentCreate;ga:eventAction==click'])
    file_name = '<enter the file name>'
    save_output_file(uri, file_name)
 
 
if __name__ == '__main__':
    main()