#ifndef _NEWDUN_TIMER_H_
#define _NEWDUN_TIMER_H_

#include <ctime>

class Timer {
    private:
        clock_t startedAt;
        clock_t pausedAt;
        bool started;
        bool paused;
	public:
        Timer();
        bool is_started();
        bool is_stopped();
        bool is_paused();
        bool is_active();
        void pause();
        bool resume();
        void stop();
        bool start();
        void reset();
        clock_t get_ticks();
};


#endif
