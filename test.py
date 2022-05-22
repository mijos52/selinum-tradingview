import  re

try :
    result = re.search('s',"hello").group()
except Exception as e :
    print (e)
result1 = re.search('e',"hello").group()
print(result1)


