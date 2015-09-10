"""
Binary bunnies
==============

As more and more rabbits were rescued from Professor Booleans horrid laboratory,
you had to develop a system to track them, since some habitually continue to
gnaw on the heads of their brethren and need extra supervision.

For obvious reasons, you based your rabbit survivor tracking system on a binary
search tree, but all of a sudden that decision has come back to haunt you.

To make your binary tree, the rabbits were sorted by their ages and each,
luckily enough, had a distinct age.

For a given group, the first rabbit became the root,
and then the next one (taken in order of rescue) was added,
older ages to the left and younger to the right.

The order that the rabbits returned to you determined the end pattern of
the tree, and herein lies the problem.

Some rabbits were rescued from multiple cages in a single rescue operation,
and you need to make sure that all of the modifications or pathogens
introduced by Professor Boolean are contained properly.

Since the tree did not preserve the order of rescue, it falls to you to figure
out how many different sequences of rabbits could have produced an identical
tree to your sample sequence, so you can keep all the rescued rabbits safe.

For example, if the rabbits were processed in order from [5, 9, 8, 2, 1],
it would result in a binary tree identical to one created from [5, 2, 9, 1, 8].

You must write a function answer(seq) that takes an array of up to 50 integers
and returns a string representing the number (in base-10) of sequences that
would result in the same tree as the given sequence.
"""


from math import factorial

mem_bincoef = {}    # cache for computed binomial coefficients

def answer(seq):
    return perm_tree(create_tree(seq))

# create a tree from the sequence
def create_tree(seq):
    tree = []

    for elem in seq:
        add_elem(tree,elem)

    return tree

# adds a new element to the tree
def add_elem(tree, elem):
    if len(tree) == 0:
        tree.append(elem)
        tree.append([])
        tree.append([])
    elif elem < tree[0]:
        add_elem(tree[1],elem)
    else:
        add_elem(tree[2],elem)

# counts the number of elements in the tree
def count_tree(tree):
    if len(tree) == 0:
        return 0
    return 1 + count_tree(tree[1]) + count_tree(tree[2])

# counts the number of ways the subtrees can be interleaved
def perm_tree(tree):
    if len(tree) == 0:
        return 1
    ct1 = count_tree(tree[1])
    ct2 = count_tree(tree[2])
    return bincoef(ct1+ct2,ct1)*perm_tree(tree[1])*perm_tree(tree[2])

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
