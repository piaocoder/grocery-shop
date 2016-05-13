#include <iostream>
#include <set>
#include <string>
#include <utility>

using namespace std;


class Test1{
    private:
        int         a;
        string      b;

    public:
        Test1() {
            this->a = 3;
            this->b = "xxxxx";
        }
        ~Test1() {
        }
};

typedef pair<Test1, Test1> test_pair_t;
typedef set<test_pair_t> test_set_t;

int main(int argc, char **argv) 
{
    Test1 testObj(), test2Obj();
    test_pair_t         pairObj;
    test_set_t          setObj;

    pairObj = make_pair(testObj, test2Obj);
    setObj.insert(pairObj);


    return 0;
}
