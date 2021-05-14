import pandas as pd 

def agg(df):
    df=df.aggregate({"Age":['sum','min'],"Weight":["min","max"],"Marks":["sum"]})
    return df

def main():
    data1 =  {'Name':['Jai', 'Anuj', 'Jai', 'Princi', 'Gaurav', 'Anuj', 'Princi', 'Abhi'],
            'Age':[27, 24, 22, 32, 33, 36, 27, 32],
            'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj','Jaunpur', 'Kanpur', 'Allahabad', 'Aligarh'],
            'Qualification':['Msc', 'MA', 'MCA', 'Phd','B.Tech', 'B.com', 'Msc', 'MA'],"Weight":[78,45,70,87,68,89,80,47],
            'Marks':[70,67,87,93,78,84,90,65]
            }
    df=pd.DataFrame(data1)
    print(agg(df))

if __name__=="__main__":
    main()
