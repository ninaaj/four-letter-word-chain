"""
	Christina Trotter
	5/27/19
	Python 3.6.2
	Notes:  this file contains the Node and Words class
"""

import words_helper as wh
from operator import itemgetter 
from collections import OrderedDict 

# node object for word graph
class Node:
    def __init__(self, word):
        self.word = word
        self.neighbors = []
    
    def __eq__(self, x):
        return hasattr(x, 'word') and self.word == x.word
    
    def __hash__(self):
        return hash(self.word)
    
    def add_neighbor(self, node):
        self.neighbors.append(node)

class Words:

    def __init__(self):
        self.dicts = {} # for list versions for the three files
        self.filenames = ['five_alpha.txt','old_four.txt','three_lc.txt']
        self.graph = None # list
        self.start = None # node of start word
        self.end = None # node of end word
        self.chain = [] # word chain
        self.explored = [] # explored list
        self.queue = OrderedDict() # priority queue / frontier (entries are placed in order of highest to lowest value)
        self.end_found = False # Flag for whether or not the end word has been reached
        self.switch = False # Flag for whether or not 3 and 5-letter words should be included in the graph search
        self.base = 0; # length of main words being used

	# loads files
    def load_files(self):
        print('\nLoading files (this might take a while)')
        for f in self.filenames:
            print('Loading ' + f + '...')
            file = open(f, 'r')
            file = file.read()
            self.dicts[f[:f.find('_')]] = file.split('\n')

	# populates graphs by creating a node for each word then calling create_graph 
	# that returns a list of all the nodes
    def pop_graph(self):
        three, four, five = [], [], []
        key = 'four' if 'four' in self.dicts else 'old'
        for w in self.dicts['three']:
            if(len(w) != 0):
                three.append(Node(w))
        for w in self.dicts[key]:
            if(len(w) != 0):
                four.append(Node(w))
        for w in self.dicts['five']:
            if(len(w) != 0):
                five.append(Node(w))
        self.graph = wh.create_graph(three,four,five)
    
	# function for setting the start and target words
    def set_words(self, start, end):
        for c in self.graph:
            if c.word == start:
                self.start = c
                break
        for c in self.graph:
            if c.word == end:
                self.end = c
                break
        return wh.result(self.start,self.end)

	# function for backtracking through the explored list to put together the correct shortest chain of words
    def create_chain(self):
        current = self.explored.pop()
        self.chain.append(current)
        for e in self.explored[::-1]: 
            if wh.are_neighbors(current,e):
                if len(self.chain) > 1 and wh.are_neighbors(self.chain[-2],e):
                    self.chain.pop()
                self.chain.append(e)
                current = e
        self.chain = self.chain[::-1]

	# function that carries out the main process of finding a chain between the start and end word
    def find_chain(self):
        current = self.start
        self.queue[current] = wh.estimate(current.word,self.end.word)
        while self.queue and current:
            if not self.switch and len(current.word) != self.base:
                while len(current.word) != self.base:
                    current = self.helper()
                    if not current:
                       break
            if current.word == self.end.word:
                self.explored.append(self.end.word)
                self.end_found = True
                break
            if current.word not in self.explored:
                self.explored.append(current.word)
                for c in current.neighbors:     
                    self.queue[c] = wh.estimate(c.word,self.end.word)
            current = self.helper()
        if self.end_found:
            self.create_chain()
            return True
        return False   

	# helper function for find_chain that checks if the queue is empty
	# calls sort_queue, and returns the next node in the queue
    def helper(self):
        if not self.queue:
            return False
        self.sort_queue()
        k,v = self.queue.popitem(last=False) 
        return k

	# function that sorts the queue items in decending order by value
    def sort_queue(self):
        temp = sorted(self.queue.items(), key = itemgetter(1), reverse=True)
        self.queue = OrderedDict()
        for k,v in temp:
            self.queue[k] = v

	# function for resetting certain varibles
    def reset(self):
        self.start = None
        self.end = None
        self.chain = []
        self.explored = []
        self.queue = OrderedDict()
        self.end_found = False

    # some basic setters and getters to promote good programming standards
    def set_switch(self, switch):
        self.switch = switch
    
    def set_base(self, base):
        self.base = base

    def get_chain(self):
        return self.chain