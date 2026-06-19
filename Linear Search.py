def linearSearch(list,target):
    for i in range(len(list)):
        if list[i]==target:
            return i 
    return -1
list = [10,20,30,40,50]
target=int(input("Enter element to search: "))
result = linearSearch(list,target)
print("Element found at index:",result)

