import pandas as pd 
import re
def split_cols_value_and_validate_length_input(name):
    
    all_char= "[0-9A-Za-z@_!#$%^&*()<>?/\|-}{~:+-=,.\s]*"
    pattern = f"{all_char}health{all_char}wallet{all_char}card{all_char}detail{all_char}"
    
    
    
    count_hifan = name.split("-") 
    count_hifan = [x.strip() for x in count_hifan]
    
    if re.search("standard",str(name).lower()):
        
        # print(count_hifan)
        
        if len(count_hifan) == 3:
            if count_hifan[2] == 'Insurance Card':
                return ["",'Insurance Card',count_hifan[1]]
            else:
                # print([count_hifan[1],count_hifan[2]])
                return ["",count_hifan[1].title(),count_hifan[2]]
        elif len(count_hifan) == 4:
            if count_hifan[3] == 'Insurance Card':
                return ["","Insurance Card",f"{count_hifan[1]} {count_hifan[2]}"]
            else:
                return ["",f"{count_hifan[1]} {count_hifan[2]}".title(),count_hifan[3]]
                
        elif len(count_hifan) == 5:
            if count_hifan[4] == 'Insurance Card':
                return ["","Insurance Card",f"{count_hifan[1]} {count_hifan[2]} {count_hifan[3]}"]
            else:
                return ["",f"{count_hifan[1]} {count_hifan[2]} {count_hifan[3]}".title(),count_hifan[4]]
        
        else:
            return ["","",name]
    elif re.findall(pattern,str(name).lower()):
        # print(count_hifan)
        if len(count_hifan) == 3:
            return ['Health Wallet Card Detail',"",count_hifan[2].title()]
        elif len(count_hifan) ==4:
            return ['Health Wallet Card Detail',"",f"{count_hifan[2]} {count_hifan[3]}".title()]
        else:
            return ["","",name]
    else:
        return ["","",""]
    
def main():
    df = pd.read_csv("raw_wallet_v2.csv",sep="|")
    
    exp = ((df['pagename'].str.lower()).str.contains("standard")) & (df["metric_name"]=="pageviews")
    exp=(df["metric_name"]=="pageviews")
    meta_df =df[exp]
    # print(meta_df)
    
    # df = df[~(df['pagename'].str.lower()).str.contains("standard") | (df["metric_name"] !="pageviews") ]
    df = df[~exp]
    
    col_initial = "pagename"
    df_new = pd.DataFrame(meta_df[col_initial].apply(split_cols_value_and_validate_length_input).tolist(),columns=['Card_Category','card_type','card_name_id'])
    # print(df_new)
    meta_df= meta_df.reset_index()

    meta_df= pd.concat([meta_df, df_new],axis=1)
    # print(meta_df)
    meta_df =meta_df.drop("index",axis=1)
    
    meta_df.to_csv("meta_df.csv",sep="|",index=False)
    df = df.append(meta_df)
    df.to_csv("append_df1.csv",sep="|",index=False)
    # print(df)
    # meta_df = meta_df.set_index("index")
    # print(meta_df)
    
    # meta_df=meta_df[['card_type','card_name_id']]

    # df =pd.concat([df,meta_df],axis=1)
    
    

   
    # # columns=["date","user_id","platform","walletcard_id","pagename","metric_name","metric_value","card_type","card_name_id","guid"]
    # # df =df.reindex(columns=columns)
    # df.to_csv("final_df_2.csv",sep="|",index=False)
    
    
if __name__ == "__main__":
    main()