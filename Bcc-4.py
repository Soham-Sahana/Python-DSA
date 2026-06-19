#List Tuple Set Dictionary Example with printing their type
# li=[10,15,20,25]
# print(li)
# print(type(li))

# tp=(10,15,20,25)
# print(tp)
# print(type(tp))

# st={10,15,20,25}
# print(st)
# print(type(st)) 

# dic={10:"ten",15:"fifteen",20:"twenty",25:"twenty five"}
# print(dic)
# print(type(dic))

#Second Largest From the list
# num=[10,18,19,91,87,63,90,102,101]
# for x in range(2):
#   max=num[0]
#   for i in num:
#     if i>max:
#       max=i
#   print(num)
#   num.remove(max)
# print(max)

#Find all pairs sum is equal to target
# target=20
# li=[10,15,5,20,12,7,13,10,0]
# for i in range(len(li)):
#   for j in range(i+1,len(li)):
#     if li[i]+li[j]==target:
#       print("Sum of",li[i],li[j],"=",target)

l = [4,5,6,7,7,8,9,9]
dict={}
for i in l:
  if i in dict:
    dict[i]+=1
  else:
    dict[i]=1
print(dict)