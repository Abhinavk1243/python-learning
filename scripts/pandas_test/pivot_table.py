import pandas as pd 
df = pd.DataFrame({"Working_days":["Monday","Tuesday","Wednesday","Thursday","Friday"],"New York":[70,73,69,68,75],"Los Angles":[80,78,74,83,76]})
df1=pd.melt(df,id_vars="Working_")