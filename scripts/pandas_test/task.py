import pandas as pd 

from lib import csvfileprocessing

# MAIN FUNCTION
def main():
    l=[]
    set_list=[]
    df4=pd.DataFrame()
    csvfileprocessing.readcsv(l,set_list)
    df4=csvfileprocessing.merge(l,set_list)
    df4=csvfileprocessing.filer(df4)
    df4=csvfileprocessing.meltdf(df4)
    print(df4)
    #savecsv(df4)

if __name__=='__main__':
    main()



