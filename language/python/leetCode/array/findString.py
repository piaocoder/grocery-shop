#!/usr/bin/evn python

def exist(board, word):
    X = len(board)
    Y = len(board[0])
    cor_add = lambda x, y: (x[0]+y[0], x[1]+y[1])
    neighbor = [(1,0), (-1,0), (0,1), (0,-1)]
    stack = []
    for i in xrange(X):
        for j in xrange(Y):
            if board[i][j] == word[0]:
                stack.append(([(i, j)], word[1:]))
    print "stack(%s, %s):"%(X,Y), stack, "| word:", word
    while not stack == []:
        s = stack.pop()
        c, w = s
        if w == '':
            return True
        l = c[-1]
        ln = [cor_add(l, n) for n in neighbor]
        print "Pop:", c, "l=", l, "ln=", ln
        for x in ln:
            if not (x[0]>=0 and x[0]<X and x[1]>=0 and x[1]<Y):
                continue
            if not (board[x[0]][x[1]] == w[0]):
                continue
            if x not in c:
                stack.append((c + [x], w[1:]))
    return False

if __name__ == "__main__":
    '''main'''
    board = [
                "ABCE",
                "SFCS",
                "ADEE"
            ]
    print exist(board, "ABCCED")
