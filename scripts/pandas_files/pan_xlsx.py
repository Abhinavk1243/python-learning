import pandas as pd
import xlrd
# dict={"Name":["abhinav","aakash","abhishek","arpit","Rohan","Maynak"], "roll_no":[1,2,3,4,5,6],"Marks":[76,87,90,55,54,66]}
# df=pd.DataFrame(dict)


def percentage_change(row):
    
    if int(row['upper_range'])!=0 and int(row['lower_range'])!=0:
        if row['validation_value']>row['upper_range']:
            pct_diff = (int(row['validation_value']-int(row['upper_range'])))/int(row['upper_range'])
        else:
            pct_diff = abs((int(row['lower_range'])-int(row['validation_value']))/int(row['lower_range']))
        
        if pct_diff*100>50:
            return 'DANGER'
        else:
            return 'PASSED'
    else:
        return 'invalid'

xls = xlrd.open_workbook('outlier.xlsx', on_demand=True)
sheet_name = xls.sheet_names()   
writer = pd.ExcelWriter('outlier_text.xlsx', engine ='xlsxwriter')
for i in sheet_name :
    df=pd.read_excel('outlier.xlsx',sheet_name=i)
    df_grp = df.groupby(['entity','metric_id','dims'])

    df['pct_diff>5']=df.apply(percentage_change,axis=1)
    print(len(df))
    # print(f"less then 5 {len(df[df['pct_diff>5']=='<5'])}")
    df=df[['metric_id', 'dims', 'entity', 'functional_area', 'metric_id_type',
        'month_ending', 'metric_value', 'validation_value', 'upper_range',
        'lower_range', 'pct_diff>5']]
    df=df.rename({'pct_diff>5':'validation_result'})
    
    df.to_excel(writer, sheet_name =i,index =False)
writer.save()
    # print(df)
# print(f"greater then 5 {len(df[df['pct_diff>5']=='>5'])}")
#riter = pd.ExcelWriter('Test.xlsx', engine ='xlsxwriter')
#3df.to_excel(writer, sheet_name ='Sheet1')
#writer.save()

# 
# df1=pd.read_excel("greenday_test.xlsx",sheet_name='new')
# # # print(list(df.columns))
# # #/*--1000051,qbr_Challenges_prerun - Completes (lifetime)--*/ 

# # df1=pd.DataFrame(df[['metric_id','metric_description','functional_area']])
# # df1['comment'] = '/*'+df1['metric_id'].astype(str) +','+df1['functional_area']+' - '+df1['metric_description']+'--*/'

# # df1.to_excel('comments.xlsx',sheet_name='sheet1',index=False)
# df['metric_id'] =df['metric_id'].astype(str)
# df['metric_id'] = df['metric_id'].replace(to_replace='2504',value='100002504')
# df['metric_id'] = df['metric_id'].replace(to_replace='2505',value='100002505')

# writer = pd.ExcelWriter('greenday.xlsx', engine ='xlsxwriter')
# df.to_excel(writer, sheet_name ='old',index =False)
# df1.to_excel(writer, sheet_name ='new',index =False)
# writer.save()







# df=pd.read_excel("qbr_eligible_validation.xlsx",sheet_name='missing_records')

# df1= df.groupby(['entity'])

# for i in df1:
#     print(list(i))
#     break