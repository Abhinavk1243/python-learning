import pandas as pd 

from lib import csvfileprocessing

# MAIN FUNCTION
def main():
    l=[]
    set_list=[]
    df4=pd.DataFrame()
    try:
        csvfileprocessing.readcsv(l,set_list)
        df4=csvfileprocessing.merge_df(l,set_list)
        #df4=csvfileprocessing.filter(df4)
        #df4=csvfileprocessing.meltdf(df4)
        #print(df4)
        csvfileprocessing.savecsv(df4)
    except Exception as error:
        print(f"Excepttion occurs : {error}")

if __name__=='__main__':
    main()



