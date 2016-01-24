#include <string>
#include <iostream>
using namespace std;

int main()
{
    string      str1 = " hello world! ";
    string      cookie = "cookie ";
    string      tempString = str1;
    size_t      pos_start, pos_end;

    pos_start = str1.find_first_not_of(" ");
    pos_end = str1.find_last_not_of(" ");
    cout<<"pos_start="<<pos_start<<"pos_end="<<pos_end<<endl;
    cout<<"result=="<<str1.substr(pos_start, pos_end-pos_start+1).c_str()<<endl;

    pos_start = cookie.find_first_not_of(" ");
    pos_end = cookie.find_last_not_of(" ");
    cout<<"\"cookie \"--> trim=="<<cookie.substr(pos_start, pos_end-pos_start+1).c_str()<<endl;

    return 0;
}
