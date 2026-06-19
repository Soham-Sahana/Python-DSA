def next_greater(arr, target):
    nearest = -1
    for i in range(len(arr)):
        if arr[i] == target:
            return arr[i]
        if arr[i] > target:
            if nearest == -1 or arr[i] < nearest:
                nearest = arr[i]
    return nearest
arr = [3,2,1,9,8,7,4,6,5]
target = int(input("Enter a target value: "))
o = next_greater(arr,target)
print("Element found at index:",o)