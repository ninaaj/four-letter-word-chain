"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""
import words, sys, traceback
BORD = '\n---------------------------------------------------\n'
DBBR = BORD + '{}' + BORD
WELC = DBBR.format('\t\tWORD CHAIN')
MENU = '\n[P]lay\n[Q]uit\nCHOICE: '
SUBM = '\n\nDo you want to use only 4-letter words \nor switch between 3, 4, and 5-letter words?\n[Y]es switch\n[N]o switch\nANSWER: '
INVL = '\n\nInvalid Input\nPlease enter {}'
PQ, YN = 'P/p or Q/q', 'Y/y or N/n\nANSWER: '
PLAY, QUIT, YES, NO = ['P','p'], ['Q','q'], ['Y','y'], ['N','n']
CHS = [PLAY,QUIT]
ANS = [YES,NO]
an, base, ch, start, end = '', 4 ,'','',''
try:
    w = words.Words()
    w.set_base(base)
    w.load_files()
    w.pop_graph()
    print(WELC)
    while ch not in QUIT:
        w.reset()
        start, end = '',''
        ch = input(MENU)
        if not any(ch in c for c in CHS):
            print(INVL.format(PQ))
        elif ch in PLAY:
            an = input(SUBM)
            while not any(an in a for a in ANS):
                an = input(INVL.format(YN))
            if an in YES:
                w.set_switch(True)
            else:
                w.set_switch(False)  
            # added in input word error checking for myself  
            while len(start) != base:
                start = input('\nPlease enter a ' + str(base) + '-letter start word: ')
            while len(end) != base:              
                end = input('\nPlease enter a ' + str(base) + '-letter end word: ')
            if start == end:
                print('Start and end words are the same.\nchain length is 0')
                continue
            res = w.set_words(start, end)
            if res != 0:
                print(res)
                continue
            res = w.find_chain()
            if res:
                chain = w.get_chain()
                for c in chain:
                    print('\n' + c)
                print('\nchain length is ' + str(len(chain)-1))
            else:
                print('\nNo chain was found between "' + start + '" and "' + end + '"')
    print('\nGOODBYE' )

except Exception as e:
    print(str(e))
    _, _, tb = sys.exc_info()
    print(traceback.format_list(traceback.extract_tb(tb)[-1:])[-1])