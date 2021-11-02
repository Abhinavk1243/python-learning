from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pandas.core.indexes.datetimes import date_range
from lib import read_config
from datetime import datetime 
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'analytics2.json'
# VIEW_ID = '254152598'
# VIEW_ID = '254343815'
VIEW_ID = '254152598'

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


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  startdate = datetime(2021,11,2).date()
  enddate = datetime(2021,11,2).date()
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': str(startdate), 'endDate': str(enddate)}],
            'dimensions': [
                            {'name':'ga:date'},
                        #    {'name': 'ga:dimension1' },
                        #    {"name":"ga:Users"},
                          
                        
                        #    {"name":"ga:eventLabel"},
                           {"name":"ga:pageTitle"},
                        # {"name":"ga:city"}
                        #    {"name":"ga:eventCategory"}
                           ],
          'metrics': [
                      {"expression": "ga:pageviews"}
                    #   {"expression": "ga:totalEvents"},
    
                    ],

        
        }]
      }
  ).execute()


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
        response: An Analytics Reporting API V4 response.
    """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])


def ga_response_dataframe(response):
    row_list = []
    # Get each collected report
    for report in response.get('reports', []):
        # Set column headers
        column_header = report.get('columnHeader', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])
    
        # Get each row in the report
        for row in report.get('data', {}).get('rows', []):
            # create dict for each row
            row_dict = {}
            dimensions = row.get('dimensions', [])
            date_range_values = row.get('metrics', [])

            # Fill dict with dimension header (key) and dimension value (value)
            for header, dimension in zip(dimension_headers, dimensions):
                row_dict[header] = dimension

            # Fill dict with metric header (key) and metric value (value)
            for i, values in enumerate(date_range_values):
                for metric, value in zip(metric_headers, values.get('values')):
                # Set int as int, float a float
                    if ',' in value or '.' in value:
                        row_dict[metric.get('name')] = float(value)
                    else:
                        row_dict[metric.get('name')] = int(value)

            row_list.append(row_dict)
    return pd.DataFrame(row_list)



def main():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    df = ga_response_dataframe(response)
    # df = read_config.mapping(df,"etl_rule.map")
    # df= pd.melt(df, id_vars =['ga:date','ga:dimension1'], value_vars =['ga:pageTitle'])
    print(df)


if __name__ == '__main__':
    main()
