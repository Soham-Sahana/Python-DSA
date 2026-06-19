# n = int(input("Enter any number:"))
# if n % 3 ==0 and n % 5 == 0:
#     print("Number is divisible by number")

#Printing numbers between any given range
# n1 = int(input('Enter value:'))
# for i in range(1,n1+1):
#     print(i)

#Printing odd and even numbers in a given range
evn = []
odd = []
for i in range(1,41):
    if i  % 2 == 0:
        evn.append(i)
    else:
        odd.append(i)

print("Even number:",evn)
print("Odd number:",odd)