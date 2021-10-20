class Farms:
    def __init__(self,hens,cows):
        self.hens=hens
        self.cows=cows
        
        
def MaxLegs(farms):
    if farms is [] or farms is None:
        return -1
    
    else:
        maxlegs = []
        for farm in farms:
            maxlegs.append((farm.cows * 4) + (farm.hens * 2))
            
        return max(maxlegs)
            
        
        
f1=Farms(87,22)
f2=Farms(52,81)

print(MaxLegs([f1,f2]))

# print((4*22)+(2*87)+(4*81)+(2*52))