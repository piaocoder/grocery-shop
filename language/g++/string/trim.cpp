/// \file trim.cpp
/// \brief 字符串空格的处理测试函数
/// \author unlessbamboo@gmail.com
/// \version 1.0
/// \date 2016-08-16

#include <string>
#include <iostream>
using namespace std;


#ifdef BAMBOO
#define BAMBOO_TEST "mylove"
#else
#define BAMBOO_TEST "waha"
#endif

int main()
{
    const char *bamboo = "Unlessbamboo";
    //const char *bamboo1 = "Unlessbamboo";
    string      str1 = " hello world! ";
    string      str2(bamboo);
    string      str3(bamboo);
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

    if (str2 == str3) {
        cout << "str2 == str3!" << endl;
    } else {
        cout << "str2 != str3!" << endl;
    }
    cout << "str2 address:" << static_cast<const void *>(str2.c_str())
        << "\tstr3 address:" << static_cast<const void *>(str3.c_str()) << endl;

    return 0;
}
