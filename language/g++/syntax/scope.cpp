#include <iostream>
#include <queue>
#include <thread>
#include <unistd.h>
/*
 * 作用域和多线程结合在一起的测试
 */

using namespace std;


class A
{
    private:
        int         num;
        string      value;

    public:
        A(int num, string value) {
            this->num = num;
            this->value = value;
        }
        ~A() {
        }

        void display() {
            cout << this->num << "---" << this->value << endl;
        }
};


/*
 * 回调，其中形参为原有对象的一份拷贝，考虑到线程的原因：
 *      1,不会在该函数的形参中传入：
 *          不存在自定义赋值构造函数（因为可能存在指针）；
 *          引用参数（完全不可以）；
 *      2,建议使用：
 *          指针；
 *          存在复制构造函数的对象的非引用形参；
 */
void cb(A ao)
{
    //sleep(10);
    cout << "线程处理函数：" << endl;
    ao.display();
}


void cb1(A *aoPtr)
{
    cout << "线程处理函数：" << endl;
    aoPtr->display();
}


int main(int argc, char **argv)
{
    queue<thread*> qo;

    for (int i=0; i<10; i++) {
        A ao(3, "xiang");
        cout << "调用线程前的输出为："  << endl;
        ao.display();

        // 错误情况１：不能将临时变量存入queue中，
        //      这里因为作用域的原因会导致段错误
        // thread t1(cb, &ao);
        // thread to(cb);
        // qo.push(&to);

        // 正确解决方式1：
        thread *to = new thread(cb, ao);
        qo.push(to);
        cout << "------------------" << endl;

        // 正确解决方式２：
        A* aoPtr = new A(4, "xiangptr");
        thread *to1 = new thread(cb1, aoPtr);
        qo.push(to1);
    }

    while (!qo.empty()) {
        thread *s1 = qo.front();
        s1->join();
        qo.pop();
    }

    //sleep(20);
    cout << "*****************准备退出进程"
        "****************" << endl;

    return 0;
}
