#ifndef TIMERMANAGER_H_
#define TIMERMANAGER_H_
#include <stdlib.h>
#include <iostream>
#include <pthread.h>
#include <list>

extern "C" {
    void *create_pthread(void *data);
}


typedef void (*fn)(int, int);

class TimerManager {
	private:
		class Timer {
            public:
                suseconds_t     duration;
                suseconds_t     start;
                fn              callback;
                //void            (*callback)(int);

            public:
                Timer(long usec, fn callback);
                bool operator ==(Timer other);
                void operator =(Timer other);
		};

		Timer set_up_timer(long micro_duration, fn callback);
		friend void *create_pthread(void *data);
		void run();

    private:
		bool                m_bRunning;
		bool                m_bGo;
		long                m_lMinSleep;
		std::list<Timer>    m_cTimers;
		pthread_t           m_tTimerThread;
		pthread_cond_t      m_tGoLockCondition;
		pthread_mutex_t     m_tGoLock;

	public:
		TimerManager();
		~TimerManager();
		void start();
		void stop();
		void add_timer(long usec, fn callback);
};

#endif
