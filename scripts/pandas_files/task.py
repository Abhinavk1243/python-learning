import pandas as pd 

from lib import csvfileprocessing

# MAIN FUNCTION
def main():
    l=[]
    set_list=[]
    df=pd.DataFrame()
    id_vars=["datetime","datetime_friendly","prop28","prop31","prop16","prop8"]
    metric_name="event_name"
    metric_value="event_number"
    try:
        csvfileprocessing.readcsv(l,set_list)
        df=csvfileprocessing.merge_df(l,set_list)
        df=csvfileprocessing.filter(df)
        df=csvfileprocessing.meltdf(df,id_vars,metric_name,metric_value)
        print(df)
        #csvfileprocessing.savecsv(df4)
    except Exception as error:
        print(f"Excepttion occurs : {error}")

if __name__=='__main__':
    main()



