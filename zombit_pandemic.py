"""
Zombit pandemic
===============

The nefarious Professor Boolean is up to his usual tricks. This time he is
using social engineering to achieve his twisted goal of infecting all the
rabbits and turning them into zombits! Having studied rabbits at length,
he found that rabbits have a strange quirk: when placed in a group,
each rabbit nudges exactly one rabbit other than itself.
This other rabbit is chosen with uniform probability. We consider two
rabbits to have socialized if either or both of them nudged the other.
(Thus many rabbits could have nudged the same rabbit, and two rabbits may
have socialized twice.) We consider two rabbits A and B to belong
to the same rabbit warren if they have socialized, or if A has socialized
with a rabbit belonging to the same warren as B.

For example, suppose there were 7 rabbits in Professor Boolean's nefarious lab.
We denote each rabbit using a number. The nudges may be as follows:

1 nudges 2
2 nudges 1
3 nudges 7
4 nudges 5
5 nudges 1
6 nudges 5
7 nudges 3

This results in the rabbit warrens {1, 2, 4, 5, 6} and {3, 7}.

Professor Boolean realized that by infecting one rabbit, eventually it would
infect the rest of the rabbits in the same warren! Unfortunately, due to
budget constraints he can only infect one rabbit, thus infecting only the
rabbits in one warren. He ponders, what is the expected maximum number of
rabbits he could infect?

Write a function answer(n), which returns the expected maximum number of
rabbits Professor Boolean can infect given n, the number of rabbits.

n will be an integer between 2 and 50 inclusive. Give the answer as a string
representing a fraction in lowest terms, in the form "numerator/denominator".
Note that the numbers may be large.

For example, if there were 4 rabbits, he could infect
a maximum of 2 (when they pair up) or 4 (when they're all socialized),
but the expected value is 106 / 27. Therefore the answer would be "106/27".
"""

from fractions import Fraction
from math import factorial

mem_bincoef = {}    # cache for computed binomial coefficients
mem_concnt = {}     # cache for computed connected graphs
mem_parperm = {}    # cache for computed 

# Calculates binomial coefficient
def bincoef(n, k):
    key = (n, k)
    
    if key not in mem_bincoef:
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1
        k = min(k, n - k) 
        c = 1
        for i in xrange(k):
            c = c * (n - i) / (i + 1)
        mem_bincoef[key] = c
    return mem_bincoef[key]

# fast integer partitioning
# Using algorithm developed by Jerome Kelleher
# http://jeromekelleher.net/partitions.php
# http://arxiv.org/pdf/0909.2331v2.pdf   
def par2(n): 
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        while True:
            x = a[k - 1] + 1
            k -= 1
            while 2*x <= y:
                a[k] = x
                y -= x
                k += 1
            l = k + 1
            while x <= y:
                a[k] = x
                a[l] = y
                if 1 not in a[:k + 1]:
                    yield a[:k + 2]
                x += 1
                y -= 1
            a[k] = x + y
            y = x + y - 1
            if 1 not in a[:k + 1]:
                yield a[:k + 1]
            if k == 0:
                break
            
# Returns the total number of graphs with n nodes       
def total(n):
    return (n-1)**n

# Returns the totoal number of connected graphs with n nodes
# tried using A000435, but this requires floating point division
# Using fraction to avoid division, too slow
# Using A001864, which gives n * a(n)
def concnt(n):
    if n not in mem_concnt:
        values = [bincoef(n, k) * (n - k) ** (n - k) * k ** k for k in range(1, n)]
        mem_concnt[n] = sum(values) / n
    return mem_concnt[n]


# Counts the number of ways n items can be placed into a patition
# without respect to ordering
def parperms(l,n):
    key = tuple(l)
    if key not in mem_parperm:
        perms = 1
        for x in l:
            perms *= bincoef(n,x)
            n -= x
        for x in set(l):
            perms /= factorial(l.count(x)) 
        mem_parperm[key] = perms
    return mem_parperm[key]

def answer(n):
    # init dictionary setting all counts to zero
    m ={}
    for i in xrange(0, n + 1):
       m[i] = 0
         
    pts = par2(n)
    for p in pts:
        # for every partition count the number of ways it could have been formed 
        cnt = parperms(p,n)
        for x in set(p):
           cnt *= concnt(x) ** p.count(x)

        # add count for maximum part in partition
        m[max(p)] += cnt

    # Calculate the expected value        
    o = 0
    for i in xrange(0, n + 1):
        o += i*m[i]
    o *= Fraction(1,total(n))
    
    return str(o.numerator) + "/" + str(o.denominator)
