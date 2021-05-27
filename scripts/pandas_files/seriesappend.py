import pandas as pd 
sr1 = pd.Series(['New York', 'Chicago', 'Toronto', 'Lisbon', 'Rio'])
#index_1 = ['City 1', 'City 2', 'City 3', 'City 4', 'City 5']
#sr1.index = index_1
sr2 = pd.Series(['Chicage', 'Shanghai', 'Beijing', 'Jakarta', 'Seoul'])
#index_2 = ['City 6', 'City 7', 'City 8', 'City 9', 'City 10']
#sr2.index = index_2
#print(sr1.append(sr2))
print(sr1.combine(sr2,(lambda x1, x2: x1 if len(x1)>len(x2) else x2)))
#print(sr1.str.join('-'))
#new=sr1.apply(lambda x :"mexico"if x=="Rio" else "Meerut")
#print(new)
