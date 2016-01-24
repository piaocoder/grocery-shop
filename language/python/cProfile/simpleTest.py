def sum_num(max_num):
    total = 0
    for i in range(max_num):
        total += i
    return total
 
 
def test():
    total = 0
    for i in range(40000):
        total += i
 
    t1 = sum_num(100000)
    t2 = sum_num(400000)
 
    return total
 
if __name__ == "__main__":
    '''Use cProfile module test program performance.'''
    import cProfile

    cProfile.run('test()', filename="result.out")
    #test()
