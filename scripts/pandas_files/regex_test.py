import re



# # .*?
# pattern = """[0-9A-Za-z@_!#$%^&*()<>?/\|}{~:]*health       
#             [0-9A-Za-z@_!#$%^&*()<>?/\|}{~:]*wallet
#             [0-9A-Za-z@_!#$%^&*()<>?/\|}{~:]*card
#             [0-9A-Za-z@_!#$%^&*()<>?/\|}{~:]*detail
#             [0-9A-Za-z@_!#$%^&*()<>?/\|}{~:]*"""


# txt ="~health-1e1wallet-card-detail"
# # txt ="0342health1232walletrw4tcard32t3wdetailsaf"
# x = re.findall(pattern, txt)
# print(x)
# if x:
#     print("YES! We have a match!")
# else:
#     print("No match")




txt = "-~!@$##@#%^^&()>X.,?/health wallet -~!@$##@#%^^&()>X.,?/card-~!@$##@#%^^&()>X.,?/ detail"
# txt ="Health Wallet - Card Detail - 5ff34ce2e53aff8d76879bef"
txt = txt.lower()	


#Find all lower case characters alphabetically between "a" and "m":

all_char= "[0-9A-Za-z@_!#$%^&*()<>?/\|-}{~:+-=,.\s]*"

pattern = f"{all_char}health{all_char}wallet{all_char}card{all_char}detail{all_char}"

# x = re.findall("[0-9A-Za-z@_!#$%^&*()<>?/\|-}{~:-]*health[0-9A-Za-z@_!#$%^&*()<>?/\|-}{~:-]*wallet[0-9A-Za-z@_!#$%^&*()<>?/\|}{~:-]*card[0-9A-Za-z@_!#$%^&*()<>?/\|-}{~:-]*detail[0-9A-Za-z@_!#$%^&*()<>?/\|}{~:-]*", txt)
x =re.findall(pattern,txt)
print(x)
if x :
    print("matched")
else:
    print("not matched")


