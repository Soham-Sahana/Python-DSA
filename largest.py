#find the largest of 3 numbers
a,b,c=12,36,86

if a>b and a>c:
        print(a,"is the largest")
elif b>c and b>a:
        print(b,"is the largest")
else:
        print(c,"is the largest")



## second logic 
if c-(a+b)>=0:
        print(c,"is the largest")
elif b-(a+c)>=0:
        print(b,"is the largest")
else:
        print(a,"is the largest")
        