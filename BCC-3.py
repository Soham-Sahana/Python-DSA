#Fibonacci series
# x = 0 
# y = 1
# for i in range(1,6):
#     print(x,end=" ")
#     x,y=y,x+y

num = int(input("Enter a number: "))
sum = 0 
t = num 

while t > 0:
    rem = t % 10
    sum += rem ** 3
    t //= 10 

print("Armstrong number") if sum == num else print("Not an armstrong number")
