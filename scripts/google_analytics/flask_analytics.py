from inspect import _empty
from typing_extensions import final
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pandas.core.indexes.datetimes import date_range
from lib import read_config
from datetime import datetime 
import logging

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'analytics-329707-cc4a4b4967b5.json'
VIEW_ID = '253803495'
# def save_csv(filename):
    
def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
        An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = discovery.build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics,definition):
    """Queries the Analytics Reporting API V4.

    Args:
        analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
        The Analytics Reporting API V4 response.
    """
    return analytics.reports().batchGet(
        body={
            'reportRequests':definition}).execute()




def ga_response_dataframe(response):
    row_list = []
    # Get each collected report
    for report in response.get('reports', []):

        column_header = report.get('columnHeader', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])
    

        for row in report.get('data', {}).get('rows', []):
            row_dict = {}
            dimensions = row.get('dimensions', [])
            date_range_values = row.get('metrics', [])

            for header, dimension in zip(dimension_headers, dimensions):
                row_dict[header] = dimension

            for i, values in enumerate(date_range_values):
                for metric, value in zip(metric_headers, values.get('values')):
       
                    if ',' in value or '.' in value:
                        row_dict[metric.get('name')] = float(value)
                    else:
                        row_dict[metric.get('name')] = int(value)

            row_list.append(row_dict)
    return pd.DataFrame(row_list)


def generate_reports(area,startdate="yesterday",enddate="today"):
    req_json = []
    dimension = area["dimensions"]
    # print(dimension)
    metrics = area["metrics"]
    if area["iterate"]:
        if area["iterate"]=="event":
            for event in area["event"]:
                # print("hello")
                definition =[
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': str(startdate), 'endDate': str(enddate)}],
                        'dimensions': dimension,
                        'metrics' : metrics,
                        "dimensionFilterClauses": [
                            {
                                "filters": [
                                    {
                                        "dimensionName": "ga:eventCategory",
                                        "operator": "EXACT",
                                        "expressions": [event]
                                    }
                                ]
                            }
                                        ]
                    }]
                # print(definition)
                req_json.append(definition)
    else:
        definition =[
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': str(startdate), 'endDate': str(enddate)}],
                        'dimensions': dimension,
                        'metrics' : metrics,
                    }]
        req_json.append(definition)
    return req_json
        
        
def download_reports(reports):
    list_df = []
    for report in reports:
        analytics = initialize_analyticsreporting()
        response = get_report(analytics,report)
        df = ga_response_dataframe(response)
        list_df.append(df)
    return list_df

def main(area):
    data_config = read_config.read_json_file("config")
    startdate = datetime(2021,11,12).date()
    enddate = datetime(2021,11,12).date()
    reports = generate_reports(data_config[area],startdate=startdate,enddate=enddate)
    list_df = download_reports(reports)
    final_df = pd.DataFrame()
    
    # list_df = read_config.mapping(list_df,f"mappings/{area}_map/{area}_mapping.map")
    for data_df in list_df:
        final_df = final_df.append(data_df,sort=False).fillna(0)  
  
    # final_df = read_config.mapping(final_df,f"mappings/{area}_map/{area}_transform.map")
    print(final_df)
    # final_df.to_csv("google_analytics_csv.files/pageviews.csv",sep="|",index=False)
   
if __name__ == '__main__':
    
    area = input("enter the area")
    main(area)

    
    
