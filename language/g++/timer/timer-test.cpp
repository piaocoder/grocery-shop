#include <iostream>
#include <fstream>
#include <sys/time.h>
#include <unistd.h>

#include "timer-manager.h"

using namespace std;

extern "C"
void func1(int id, int num)
{
    struct timeval l_tv;
    gettimeofday(&l_tv, NULL);
    cout << "I was called (first) @ " 
        << l_tv.tv_usec << endl;
}

extern "C"
void func2(int id, int num)
{
    struct timeval l_tv;
    gettimeofday(&l_tv, NULL);
    cout << "I was called (second) @ " 
        << l_tv.tv_usec << endl;
}

int main(int, char *[])
{
    TimerManager t;
    t.add_timer(1000000 / 2, func1);
    t.add_timer(1000000 * 8, func2);
    t.start();

    while(true) {
        sleep(1);
    }
    return 0;
}
