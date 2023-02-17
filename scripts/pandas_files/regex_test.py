import re



# # .*?
pattern = """2022-12[0-9-,\s]*2022-09[0-9-,\s]*"""


txt ="2022-12,2022-11,2022-10,2022-09,2022-08,2022-07"
# txt ="0342health1232walletrw4tcard32t3wdetailsaf"
x = re.findall(pattern, txt)
# if x:
#     print(x)
# else:
#     print('no')
    

# l = [1,2,5,3,4]

# print(l[:4])
# txt = "-~!@$##@#%^^&()>X.,?/health wallet -~!@$##@#%^^&()>X.,?/card-~!@$##@#%^^&()>X.,?/ detail"
# # txt ="Health Wallet - Card Detail - 5ff34ce2e53aff8d76879bef"
# txt = txt.lower()	


# #Find all lower case characters alphabetically between "a" and "m":

# all_char= "[0-9A-Za-z@_!#$%^&*()<>?/\|-}{~:+-=,.\s]*"

# pattern = f"{all_char}health{all_char}wallet{all_char}card{all_char}detail{all_char}"

# # x = re.findall("[0-9A-Za-z@_!#$%^&*()<>?/\|-}{~:-]*health[0-9A-Za-z@_!#$%^&*()<>?/\|-}{~:-]*wallet[0-9A-Za-z@_!#$%^&*()<>?/\|}{~:-]*card[0-9A-Za-z@_!#$%^&*()<>?/\|-}{~:-]*detail[0-9A-Za-z@_!#$%^&*()<>?/\|}{~:-]*", txt)
# x =re.findall(pattern,txt)
# print(x)
# if x :
#     print("matched")
# else:
#     print("not matched")



rep='2022-12'
txt ="2022-12,2022-11,2022-10,2022-09,2022-08,2022-07,2022-06,2022-05,2022-04"
year=rep[0:4]
month=rep[5:]

list_q=[]


list_1 = txt.split(',')
list_1 =list_1[0:4]
for i in list_1:
    if i[5:] in ['12','09','06','03'] :
        list_q.append(i)

print(list_q)
date=[]
for i in list_1:
    if i in  list_q:
        date.append(i)

dates=[]
for  i in  list_1:
    if i >=date[-1]:
        dates.append(i)



print(dates)
