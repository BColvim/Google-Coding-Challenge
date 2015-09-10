"""
Line up the captives
====================

As you ponder sneaky strategies for assisting with the great rabbit escape,
you realize that you have an opportunity to fool Professor Booleans guards
into thinking there are fewer rabbits total than there actually are.

By cleverly lining up the rabbits of different heights, you can obscure the
sudden departure of some of the captives.

Beta Rabbits statisticians have asked you for some numerical analysis of how
this could be done so that they can explore the best options.

Luckily, every rabbit has a slightly different height, and the guards are lazy
and few in number. Only one guard is stationed at each end of the rabbit
line-up as they survey their captive population.

With a bit of misinformation added to the facility roster, you can make the
guards think there are different numbers of rabbits in holding.

To help plan this caper you need to calculate how many ways the rabbits can be
lined up such that a viewer on one end sees x rabbits, and a viewer on the other
end sees y rabbits, because some taller rabbits block the view of the shorter
ones.

For example, if the rabbits were arranged in line with heights 30 cm, 10 cm,
50 cm, 40 cm, and then 20 cm,a guard looking from the left would see 2 rabbits
while a guard looking from the right side would see 3 rabbits.

Write a method answer(x,y,n) which returns the number of possible ways to
arrange n rabbits of unique heights along an east to west line, so that only x
are visible from the west, and only y are visible from the east. The return
value must be a string representing the number in base 10.

If there is no possible arrangement, return "0".

The number of rabbits (n) will be as small as 3 or as large as 40
The viewable rabbits from either side (x and y) will be as small as 1 and as
large as the total number of rabbits (n).
"""


mem_bincoef = {} # cache for computed binomial coefficients
mem_arrange = {} # cache for computed arrangements

# Binomial coefficient
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

def arrange(x, y, n):
    # use answer symmetry to avoid double calculations 
    if x > y:
        x,y = y,x

    # base cases
    if (n > 1) and (x+y <3):
        return 0
           
    if n == 1 or n == 2:
        return 1

    key = (x, y, n)
    if key not in mem_arrange:
        sum = 0
        #
        if x == 1:  # special case. One visible, none can be hidden

            # Iterate over all possible arrangements on right of max value
            for j in xrange(1,n-y+2):
                sum += arrange(j, y-1,n-1)
                
        else:
           
            # iterate over all possible counts left of max value          
            for i in xrange(max(1, x-1), n - y + 1):
                sum1 = 1
                sum2 = 1

                # Iterate over all possible arrangements on left of max value
                if i > 1: 
                    sum1 = 0
                    for j in xrange(1, i-x+3):
                        sum1 += arrange(x-1, j, i)

                # Iterate over all possible arrangements on right of max value
                if n - i -1 > 1: 
                    sum2 = 0
                    for j in xrange(1, n-y-i+2):
                        sum2 += arrange(j, y-1, n-i-1)

                # consider all permutations of for each division
                sum += sum1 * sum2 * bincoef(n-1,i) 
        mem_arrange[key] = sum
    
    return mem_arrange[key]

def answer(x, y, n):
    return arrange(x, y, n)
