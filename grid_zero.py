'''
Grid Zero
=========
 
You are almost there. The only thing between you and foiling Professor Boolean's
plans for good is a square grid of lights, only some of which seem to be lit up.
The grid seems to be a lock of some kind. That's interesting. Touching a light
toggles the light, as well as all of the other lights in the same row and column
as that light.
 
Wait! The minions are coming - better hide.
 
Yes! By observing the minions, you see that the light grid is, indeed, a lock.
The key is to turn off all the lights by touching some of them. The minions are
gone now, but the grid of lights is now lit up differently. Better unlock it
fast, before you get caught.
 
The grid is always a square. You can think of the grid as an NxN matrix of
zeroes and ones, where one denotes that the light is on, and zero means that the
light is off.
 
For example, if the matrix was
 
1 1
0 0
 
Touching the bottom left light results in
 
0 1
1 1
 
Now touching the bottom right light results in
 
0 0
0 0
 
...which unlocks the door.
 
Write a function answer(matrix) which returns the minimum number of lights that
need to be touched to unlock the lock, by turning off all the lights. If it is
not possible to do so, return -1.
 
The given matrix will be a list of N lists, each with N elements. Element
matrix[i][j] represents the element in row i, column j of the matrix. Each
element will be either 0 or 1, 0 representing a light that is off, and 1
representing a light that is on.
 
N will be a positive integer, at least 2 and no more than 15.
'''

def answer(matrix):
    n = len(matrix)
    if n % 2 == 0:
        # construct a moves matrix
        moves = []
        for y in range(n):
            moves.append([0]*n)
            
        # eliminate for each lit state
        elim_mat(moves,matrix)

        # count the moves
        return sum([sum(r) for r in moves])
    else:
        if not solvable(matrix):
            return -1

        # Solve n-1 x n-1 submatrix
        moves = []
        for y in range(n-1):
            moves.append([0]*(n-1))
            
        # eliminate for each lit state in submatrix
        elim_mat(moves,matrix)

        # augment moves matrix to size n
        for i in range(n-1):
            moves[i].append(0)
        moves.append([0]*(n))

        # perform moves on the matrix check
        # if the last bottom left corner also 
        # needs to be toggled
        if matrix[n-1][n-1] == 1:
            moves[n-1][n-1] = 1
            
        # encode moves as ints      
        bm = mat_to_bitmat(moves)
        mincount = sum([bitcount(row) for row in bm])
        
        #iterate through all possible column masks
        for i in xrange(0,2**n):
            
            # get the bitcount for all masked rows and sort
            bsums = sorted([bitcount(r^i) for r in bm])[::-1]
            moves = sum(bsums)
            
            fi = 0 # flip iterator

            # Need to maintain 0 parity, so that result is a 'quiet' configuration
            # in that it doesn't have a net effect on the board
            if parityOf(i) == 1:
                moves += n-2*bsums[0]
                fi = 1
                
            # flip pairs that result in a lower move count
            for j in xrange(fi,n-1,2):
                s = bsums[j] + bsums[j+1] 
                if s > n:
                    moves += 2*(n - s)
                else:
                    break
        
            if moves < mincount:
                mincount = moves
               
        return mincount 

# converts list of list to list toggles of integers
#to improve efficiency using bit operations
def mat_to_bitmat(m):
    d = len(m)
    v = [0]*d
    for i in range(d):
        for j in range(d-1,0-1,-1):
            v[i] <<= 1
            if m[i][j] == 1:
                v[i] += 1
    return v

#returns parity of an integer
def parityOf(n):
    parity = int(n) 
    while parity > 1 :
        parity = (parity >> 1) ^ (parity & 1) 
    return parity

# returns sum of the bits in an integer
def bitcount(n):
    count = 0
    while n > 0:
        count += (n&1)
        n >>= 1
    return count

# toggle all elements in row and column   
def elim(m, x, y):
    for y1 in range(len(m)):
        if y == y1:
            for x1 in range(len(m)):
                m[y1][x1] = (m[y1][x1]+1)%2
        else:
            m[y1][x] = (m[y1][x]+1)%2

# toggle all elements in m as specified by me
def elim_mat(m,me):
    n = len (m)
    for y in range(n):
        for x in range(n):
            if me[y][x] == 1:
                elim(m,x,y)

# is the matrix solvable
def solvable(m):
    par = [sum(r)%2 for r in m]
    for i in range(len(m)):
        par.append(sum([r[i] for r in m]) % 2)
    return len(set(par)) == 1
