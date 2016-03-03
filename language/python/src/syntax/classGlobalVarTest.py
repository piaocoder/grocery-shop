'''
1，类全局变量的测试
'''
class task_queue:
    queue=[]
    num = 0
    
    def append(self,obj):
        self.queue.append(obj)
        self.num += 1
        
    def print_queue(self):
        print self.queue, self.num
        
if __name__=="__main__":
    a=task_queue()
    b=task_queue()
    
    a.append('tc_1')
    a.num += 1

    a.print_queue()
    b.print_queue()

    task_queue.num = 1000
    a.print_queue()
    b.print_queue()

