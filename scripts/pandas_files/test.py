
import pandas as pd 


def split_cols_and_validate_length(name):
    # print("hello")
    count_hifan = name.split("-")
    if count_hifan == None:
        print("yes")
        print(name)
    
    
    count_hifan = [x.strip() for x in count_hifan]
    # print(count_hifan)
    
    if len(count_hifan) == 3:
        if count_hifan[2] == 'Insurance Card':
            return ['Insurance Card',count_hifan[1],"2 - and Insurance Card at 3rd"]
        else:
            # print([count_hifan[1],count_hifan[2]])
            return [count_hifan[1],count_hifan[2],'2 - and Insurance Card not at 3rd']
    elif len(count_hifan) == 4:
        if count_hifan[3] == 'Insurance Card':
            return ["Insurance Card",f"{count_hifan[1]} {count_hifan[2]}","3 - and Insurance Card at 4th"]
        else:
            return [f"{count_hifan[1]} {count_hifan[2]}",count_hifan[3],"3 - and Insurance Card not at 4th"]
			
    elif len(count_hifan) == 5:
        if count_hifan[4] == 'Insurance Card':
            return ["Insurance Card",f"{count_hifan[1]} {count_hifan[2]} {count_hifan[3]}","4 - and Insurance Card at 5th"]
        else:
            return [f"{count_hifan[1]} {count_hifan[2]} {count_hifan[3]}",count_hifan[4],"4 - and Insurance Card not at 5th"]
    
    else:
        return ["","",name]
    
def main():
    df = pd.read_csv("sample_data_1.csv",sep="|")
    df_new = df[df["Case"]=="4 - and Insurance Card not at 5th"]
    print(df_new.head(3))
    # col_initial = "pagename"
    # # p
    # #
    # df_new = pd.DataFrame(df[col_initial].apply(split_cols_and_validate_length).tolist(),columns=['card_type','card_name_id','Case'])
    # df = df.reset_index()
    # df = pd.concat([df, df_new],axis=1)
    # df =df.set_index("index")
    # df.to_csv("sample_data_1.csv",sep="|",index=False)

if __name__ == "__main__":
    main()