"""
Breeding like rabbits
=====================

As usual, the zombie rabbits (zombits) are breeding... like rabbits!
But instead of following the Fibonacci sequence like all good rabbits do,
the zombit population changes according to this bizarre formula, where R(n) is
the number of zombits at time n:

R(0) = 1
R(1) = 1
R(2) = 2
R(2n) = R(n) + R(n + 1) + n (for n > 1)
R(2n + 1) = R(n - 1) + R(n) + 1 (for n >= 1)

(At time 2, we realized the difficulty of a breeding program with only one
zombit and so added an additional zombit.)

Being bored with the day-to-day duties of a henchman, a bunch of Professo
Boolean's minions passed the time by playing a guessinggame:
"When will the zombit population be equal to a certain amount?"

Then, some clever minion objected that this was too easy, and proposed a
slightly different game: "When is the last time that the zombit population will
be equal to a certain amount?"

Write a function answer(str_S) which, given the base-10 string representation of
an integer S, returns the largest n such that R(n) = S.

Return the answer as a string in base-10 representation.
If there is no such n, return "None".

S will be a positive integer no greater than 10^25.
"""

mem_r = { 0:1, 1:1, 2:2 }

def answer(str_S):
    S = int(str_S)

    # check odd case first since it grows faster
    return (bin_search(S, 0, S, 1) or bin_search(S, 0, S, 0) or "None")

def R(n):
    if not n in mem_r:
        if n % 2 == 0:
            n1 = (n >> 1)
            mem_r[n] = R(n1) + R(n1+1) + n1
        else:
            n1 = (n >> 1)
            mem_r[n] = R(n1-1) + R(n1) + 1
    return mem_r[n]

# Binary search for target based on parity.
# Works because even and odd sequences are each monotonic 
def bin_search(target, lower, upper, parity):

    if lower > upper:
        return ""
    
    #find midpoint
    mid = (lower+upper)/2
    
    # adjust for parity
    if (mid+parity)%2 != 0:
        mid +=1

    S = R(mid)

    if S == target:  # found it!
        return mid
    elif lower == upper:
        return ""
    elif S > target: # search lower half
        return bin_search(target, lower, mid-1, parity)
    else:            # search upper half
        return bin_search(target, mid+1, upper, parity)
