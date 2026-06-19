#Binary Search
def binarySearch(nums,target):
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
            
        return -1
nums = [2,4,5,6,8,1]
target = int(input("Enter target value: "))
a = binarySearch(nums,target)
print("Element found at index:",a)