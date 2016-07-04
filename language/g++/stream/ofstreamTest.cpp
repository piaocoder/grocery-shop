#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char **argv)
{
    ofstream        *error, *debug;

    error = new ofstream();
    const char *file1 = "error.log";
    error->open(file1, ios::out|ios::app);
    if (!error->is_open()) {
        cout << "打开日志文件：" << file1 << "失败" << endl;
        exit(-1);
    }

    debug = new ofstream();
    const char *file2 = "debug.log";
    debug->open(file2, ios::out|ios::app);
    if (!debug->is_open()) {
        cout << "打开日志文件：" << file2 << "失败" << endl;
        exit(-1);
    }

    cout <<  "准备开始记录error日志：" << endl;
    for (int i=0; i<10; i++) {
        *error << "index" << i << endl;
    }

    cout <<  "准备开始记录debug日志：" << endl;
    for (int i=10; i<100; i++) {
        *debug << "index" << i << endl;
    }

    error->flush();
    debug->flush();

    return 0;
}
