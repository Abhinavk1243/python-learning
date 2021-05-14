# importing pandas module
from numpy import sin, single
import pandas as pd 

#function of merge using single key
def singlekey(df,df1):
        single_key=pd.merge(df,df1,on='key')
        print(single_key)

#function of merge using multiple key
def mulkey(df,df1):
        mul_key=pd.merge(df,df1,on=['key','key1'])
        print(mul_key)

#function of merge  using left join
def leftjoin(df,df1):
        left=pd.merge(df,df1,how="left",on=['key','key1'])
        print(left)

#function of merge  using right join
def rightjoin(df,df1):
        right=pd.merge(df,df1,how="right",on=['key','key1'])
        print(right)

def main():

        # Define a dictionary containing employee data 
        data1 = {'key': ['K0', 'K1', 'K2', 'K3'],
                'key1': ['K0', 'K1', 'K0', 'K1'],
                'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'], 
                'Age':[27, 24, 22, 32],} 
        
        # Define a dictionary containing employee data 
        data2 = {'key': ['K0', 'K1', 'K2', 'K3'],
                'key1': ['K0', 'K0', 'K0', 'K0'],
                'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'], 
                'Qualification':['Btech', 'B.A', 'Bcom', 'B.hons']} 
        
        # Convert the dictionary into DataFrame  
        df = pd.DataFrame(data1)
        
        # Convert the dictionary into DataFrame  
        df1 = pd.DataFrame(data2) 

        print("merge by single key")
        singlekey(df,df1)
        print("\n")

        print("merge by multiple keys")
        mulkey(df,df1)
        print("\n")

        print("merge by left join")
        leftjoin(df,df1)
        print("\n")
        
        print("merge by right join")
        rightjoin(df,df1)

if __name__=="__main__":
        main()








