import pandas as pd
def stockBuySell(price, n):
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    if (n == 1):
        return
    i = 0
    records_list = []
    while (i < (n - 1)):
        record = dict()
        while ((i < (n - 1)) and (price[i + 1] <= price[i])):
            i += 1
        if (i == n - 1):
            break
        buy = i
        i += 1
        
        while ((i < n) and (price[i] >= price[i - 1])):
            i += 1
            sell = i - 1
            
        profit = price[sell] - price[buy]
        record["buy"] = days[buy]
        record["sell"] = days[sell]
        record["profit"] = profit
        records_list.append(record)
    
    return records_list
		



price = [110, 280, 260,310, 40, 535, 695]
n = len(price)

print(pd.DataFrame(stockBuySell(price, n)))

