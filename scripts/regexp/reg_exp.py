import re
text="In 1992, Tim Berners-Lee ciiiiiiirculated a document titled “HTML Tags,” which outlined just 20 tags, many of which are now obsolete or have taken other forms. The first surviving tag to be defined in the document, after the crucial anchor tag, is the paragraph tag. It wasn’t until 1993 that a discussion emerged on the proposed image tag"
print(re.findall("ai", text))
print(re.findall("^In",text))
print(re.findall("in$",text))
print(re.findall("\d{10}",text))
print(re.findall("ci*",text))
print(re.findall("be{2}",text))
print(re.findall("\AIn",text))
print("\w",text)



