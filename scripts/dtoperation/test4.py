import xml.etree.ElementTree as ET

d={"brand":["redmi","oppo"],"price":[15000,20000]}
t=list(d.keys())
l=len(t)
val=list(d.values())
print(val[0][1])
len1=len(val[0])
re=ET.Element("Catalog")
s1=ET.Element("mobile")
re.append(s1)

for i in  t:
    for j in range(len1):

        b1=ET.SubElement(s1,d[i])
        b1.text=val[j][j]
