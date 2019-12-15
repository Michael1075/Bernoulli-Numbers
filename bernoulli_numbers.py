import math
import time

def cmdivisor(a,b):
    if a==b:
        N=a
    elif a==1 or b==1:
        N=1
    else:
        if a<b:
            a,b=b,a
    while True:
        if a%b==0:
            N=b
            break
        else:
            a=a%b
            a,b=b,a
            if b==1:
                N=1
                break
    return N
    
def cmmultiple(a,b):
    return a*b//cmdivisor(a,b)

def frac(a,b):
    if a==0:
        c=0
        d=1
    else:
        if a<0 and b<0 or a>0 and b>0:
            mode=1
        else:
            mode=0
        a=abs(a)
        b=abs(b)
        n=cmdivisor(a,b)
        c=a//n
        d=b//n
        if mode==0:
            c=-c
    return (c,d)
    
def fracsum(a,b):
    if a[1]<0:
        a[0]=-a[0]
        a[1]=-a[1]
    if b[1]<0:
        b[0]=-b[0]
        b[1]=-b[1]
    n=cmmultiple(a[1],b[1])
    m=a[0]*n//a[1]+b[0]*n//b[1]
    if m==0:
        n=1
    return frac(m,n)

def fracdifference(a,b):
    if a[1]<0:
        a[0]=-a[0]
        a[1]=-a[1]
    if b[1]<0:
        b[0]=-b[0]
        b[1]=-b[1]
    n=cmmultiple(a[1],b[1])
    m=a[0]*n//a[1]-b[0]*n//b[1]
    if m==0:
        n=1
    return frac(m,n)

def fracproduct(a,b):
    return frac(a[0]*b[0],a[1]*b[1])
    
def fracdivision(a,b):
    return frac(a[0]*b[1],a[1]*b[0])

def write(i):
    if i[1]==1:
        return str(i[0])
    else:
        return '{0}/{1}'.format(i[0],i[1])
    
def combination(a,b):
    return frac(math.factorial(a),math.factorial(b)*math.factorial(a-b))

def formula(k):
    Formula=['S_{0}(n)='.format(k)]
    for j in range(1,k+2,1):
        c=fracproduct(fracproduct(B[j-1],combination(k+1,j-1)),(1,k+1))
        d=k+2-j
        if j==1:
            part=write(c)+'*n^{0}'.format(d)
            Formula.append(part)
        else:
            if c[0]==0:
                pass
            elif c[0]>0:
                part='+'+write(c)+'*n^{0}'.format(d)
                Formula.append(part)
            else:
                part=write(c)+'*n^{0}'.format(d)
                Formula.append(part)
    print(''.join(Formula))

def calculate(n,r):
    S=(0,1)
    for j in range(1,r+2,1):
        c=fracproduct(B[j-1],combination(r+1,j-1))
        d=r+2-j
        S=fracsum(S,fracproduct(c,(n**d,1)))
    S=fracproduct(S,(1,r+1))
    print('S_{0}({1})={2}'.format(r,n,S[0]))

seperator='--------------------'
print('Menu of modes')
print('0: Formulas of S_i(n) where i ranges from 1 to r and n is a constant')
print('1: Display of B[i] where i ranges from 0 to r, which are known as Bernoulli numbers')
print('2: Display of b[i] where i ranges from 0 to r, which equals to B[i]/i!')
print('3: Calculation of S_r(n) where r and n are both up to you')
print('4: Calculation of S_r(i) where i ranges from 1 to n')
print('5: Calculation of S_i(n) where i ranges from 1 to r')
print('6: Stop')
print(seperator)

while True:
    while True:
        Mode=input('Please choose one mode from the above: ')
        Modes=['0','1','2','3','4','5','6']
        if Mode in Modes:
            mode=int(Mode)
            break
        else:
            continue
    if mode==6:
        print(seperator)
        break
    elif mode in [3,4,5]:
        while True:
            strn=input('Input n, which should be a positive integer: ')
            if strn.isdigit() and strn!='0':
                n=int(strn)
                break
            else:
                continue
    while True:
        strr=input('Input r, which should be a positive integer: ')
        if strr.isdigit() and strr!='0':
            r=int(strr)
            break
        else:
            continue
    print(seperator)
    
    start=time.clock()
    
    if mode==2:
        print('Mode 2: Display of b[i] where i ranges from 0 to {0}, which equals to B[i]/i!'.format(r))
        b=[(1,1)]
        for t in range(1,r+1,1):
            s=(0,1)
            for i in range(1,t+1,1):
                s=fracsum(s,fracdivision(b[t-i],frac(math.factorial(i+1),1)))
            a=fracdifference(frac(1,math.factorial(t)),s)
            b.append(a)
        for c in range(0,r+1,1):
            print('b[{0}]={1}'.format(c,write(b[c])))
        
    else:
        B=[(1,1)]
        for t in range(1,r+1,1):
            s=(0,1)
            for i in range(0,t,1):
                s=fracsum(s,fracproduct(combination(t+1,i),B[i]))
            a=fracdivision(fracdifference((t+1,1),s),(t+1,1))
            B.append(a)
        if mode==0:
            print('Mode 0: Formulas of S_i(n) where i ranges from 1 to {0} and n is a constant'.format(r))
            for k in range(1,r+1,1):
                formula(k)
        elif mode==1:
            print('Mode 1: Display of B[i] where i ranges from 0 to {0}, which are known as Bernoulli numbers'.format(r))
            for c in range(0,r+1,1):
                print('B[{0}]={1}'.format(c,write(B[c])))
        elif mode==3:
            print('Mode 3: Calculation of S_{0}({1})'.format(r,n))
            formula(r)
            calculate(n,r)
        elif mode==4:
            print('Mode 4: Calculation of S_{0}(i) where i ranges from 1 to {1}'.format(r,n))
            formula(r)
            for i in range(1,n+1,1):
                calculate(i,r)
        else:
            print('Mode 5: Calculation of S_i({0}) where i ranges from 1 to {1}'.format(n,r))
            for i in range(1,r+1,1):
                calculate(n,i)
    
    end=time.clock()
    print('Running time: %s Seconds'%(end-start))
    print(seperator)