#include <iostream>
#include <vector>
#include <chrono>

#include "ThreadPool.h"

class SB {
    public:
        int display(int i)
        {
            std::cout << "郑碧峰:" << std::endl;
            std::cout << "hello " << i << std::endl;
            std::this_thread::sleep_for(std::chrono::seconds(1));
            std::cout << "world " << i << std::endl;
            return i*i;
        }

        int run() 
        {
            ThreadPool pool(4);
            std::vector< std::future<int> > results;

            for(int i = 0; i < 8; ++i) {
                pool.enqueue(&SB::display, this, i);
                //results.emplace_back(
                        //pool.enqueue(&SB::display, this, i)
                    //pool.enqueue([i] {
                        //std::cout << "hello " << i << std::endl;
                        //std::this_thread::sleep_for(std::chrono::seconds(1));
                        //std::cout << "world " << i << std::endl;
                        //return i*i;
                    //})
                //);
                std::cout << "xxxxxxxxxxxxxxxxxxxxxxxxxxx" << std::endl;
            }

            //for(auto && result: results)
                //std::cout << result.get() << ' ';
            //std::cout << std::endl;
            return 0;
        }
};


int main()
{
    // 方法１
//#define METHOD1
#ifdef METHOD1
    ThreadPool pool(4);
    std::vector< std::future<int> > results;
    SB sb;

    for(int i = 0; i < 8; ++i) {
        results.emplace_back(
                pool.enqueue(&SB::display, &sb, i)
        );
        std::cout << "xxxxxxxxxxxxxxxxxxxxxxxxxxx" << std::endl;
    }

    for(auto && result: results)
        std::cout << result.get() << ' ';
    std::cout << std::endl;
#endif

    // 方法２
    SB sb;
    sb.run();
    
    return 0;
}
