"""
	Christina Trotter
	5/27/19
	Python 3.6.2
	Notes:  this file contains functions that did not need to be included in the words.py file
"""

# adds all the neighbors to each node, then puts all the nodes in one list, WAY too many for loops 
def create_graph(a, b, c):
        
    for i in range(0, len(a)-1):
        for j in range(i+1, len(a)):
            if are_neighbors(a[i].word, a[j].word):
                a[i].add_neighbor(a[j])
                a[j].add_neighbor(a[i])
        
    for i in range(0, len(c)-1):
        for j in range(i+1, len(c)):
            if are_neighbors(c[i].word, c[j].word):
                c[i].add_neighbor(c[j])
                c[j].add_neighbor(c[i])           
        
    for i in range(0, len(b)-1):
        for j in range(i+1, len(b)):
            if are_neighbors(b[i].word, b[j].word):
                b[i].add_neighbor(b[j])
                b[j].add_neighbor(b[i])
        
        for n in a:
            if are_neighbors(n.word, b[i].word):
                b[i].add_neighbor(n)
                n.add_neighbor(b[i])

        for n in c:
            if are_neighbors(n.word, b[i].word):
                b[i].add_neighbor(n)
                n.add_neighbor(b[i])
        
    b.extend(a)
    b.extend(c)
    return b

# function to estimate how close a four letter word is to the target word
# calls and returns the value of switch_estimate if words do not have same length
# returns a value from 0 to 4
# higher = better  
def estimate(a,b):
    z = 0
    if len(a) != len(b):
        return switch_estimate(a,b)
    else:    
        for i in range(0,len(a)):
            if a[i] == b[i]:
                z += 1   
    return z

# function to estimate how close a three or five letter word is to the target word
# returns a value from 0 to 4
# higher = better 
def switch_estimate(a,b):
    if abs(len(a)-len(b)) != 1:
        return 0
    a,b = assign(a,b)
    z = 0
    for i in range(0,len(a)):
        if a[i] == b[i] or a[i] == b[i+1]:
            z += 1  
    return z

# function to determine if two words that have the same length are neighbors
# calls and returns the value of are_switch_neighbors if words do not have same length
def are_neighbors(a,b):
    if len(a) != len(b):
        return are_switch_neighbors(a,b)
    diff = 0
    for i in range(0,len(a)):
        if a[i] != b[i]:
            diff += 1
        if diff > 1:
            return False
    return True  

# function to determine if two words that have different lengths are neighbors
def are_switch_neighbors(a,b):
    shift = False
    if abs(len(a)-len(b)) != 1:
        return False
    a,b = assign(a,b)
    for i in range(0,len(a)):
        if shift and a[i] != b[i+1]:
            return False
        if a[i] != b[i] and a[i] != b[i+1]:
            return False
        if a[i] != b[i] and a[i] == b[i+1] and not shift:
            shift = True  
    return True 

# function to determine if the given start and target word are in the current graph
def result(a,b):
    if a is None and b is None:
        return 'Both words were not found in the current word graph'
    if a is None:
        return 'The start word was not found in the current word graph'
    if b is None:
        return 'The end word was not found in the current word graph'
    return 0

# function to determine which word has the lesser length
def assign(a,b):
    if len(a) < len(b):
        return a,b 
    else:
        return b,a
