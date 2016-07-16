#include <iostream>
#include <tuple>
#include <queue>

using namespace std;


typedef tuple<string, int, string, int> TupleMsg;
typedef queue<TupleMsg> QueueMsg;

int main(int argc, char **argv)
{
    TupleMsg    t1("kuang", 1, "男", 23);
    TupleMsg    t2("xiang", 2, "女", 23);
    TupleMsg    t3 = t1;

    cout << "t1:";
    cout << get<0>(t1) << "-" << get<1>(t1) << "-" 
        << get<2>(t1) << "-" << get<3>(t1) << endl;

    cout << "t2:";
    cout << get<0>(t2) << "-" << get<1>(t2) << "-" 
        << get<2>(t2) << "-" << get<3>(t2) << endl;

    cout << "t3:";
    cout << get<0>(t3) << "-" << get<1>(t3) << "-" 
        << get<2>(t3) << "-" << get<3>(t3) << endl;

    QueueMsg    qobj;
    qobj.push(t1);
    qobj.push(t2);
    cout << "队列中数据:" << endl;
    while (!qobj.empty()) {
        cout << get<0>(qobj.front()) << "-" 
            << get<2>(qobj.front()) << endl;
        qobj.pop();
    }

    return 0;
}
