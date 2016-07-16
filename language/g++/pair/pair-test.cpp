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
            this->a = 0;
            this->b = "xxxxx";
        }
        Test1(int num) {
            this->a = num;
            this->b = "xxxxx";
        }
        ~Test1() {
        }
        void display() {
            cout << this->a << endl;
        }
};

// 当然，可以使用tuple代替该方式
typedef pair<Test1, Test1> test_pair_t;
typedef pair<test_pair_t, test_pair_t> test_mul_pair_t;

int main(int argc, char **argv) 
{
    test_mul_pair_t     mulPairObj;
    test_pair_t         p1, p2;
    Test1 o1(1), o2(2), o3(3), o4(4);
    p1 = make_pair(o1, o2);
    p2 = make_pair(o3, o4);
    mulPairObj = make_pair(p1, p2);

    cout << "First1:";
    mulPairObj.first.first.display();
    cout << "First2:";
    mulPairObj.first.second.display();
    cout << "Second1:";
    mulPairObj.second.first.display();
    cout << "Second1:";
    mulPairObj.second.second.display();


    return 0;
}
