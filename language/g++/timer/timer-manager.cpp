#include <algorithm>
#include <iterator>
#include <sys/time.h>
#include <unistd.h>
#include "timer-manager.h"

using namespace std;

TimerManager::Timer::Timer(long usec, fn callback)
{            
    this->duration = usec;
    this->callback = callback;
    this->start = 0;
}


bool TimerManager::Timer::operator ==(Timer other)
{
    if ((this->callback == other.callback) 
            && (this->duration == other.duration)) {
        return true;
    }
    return false;
}


void TimerManager::Timer::operator =(Timer other)
{
    duration = other.duration;
    callback = other.callback;
    start = other.start;
}

extern "C" void *create_pthread(void *data)
{
    TimerManager *thread_timer_manager = 
        static_cast<TimerManager *>(data);
    thread_timer_manager->run();
    return data;
}


TimerManager::TimerManager() :
    m_bRunning(false),
    m_bGo(false),
    m_lMinSleep(0)
{
    int         mutex_creation;
    int         mutex_cond_creation;
    int         thread_creation;

    mutex_creation = pthread_mutex_init(&m_tGoLock, NULL);
    if(mutex_creation != 0) {
        cerr << "Failed to create mutex" << endl; 
        return;
    }

    mutex_cond_creation = pthread_cond_init(
            &m_tGoLockCondition, NULL);
    if(mutex_cond_creation != 0) {
        cerr << "Failed to create condition mutex" 
            << endl;
        return;
    }

    thread_creation = pthread_create(&m_tTimerThread,
            NULL, create_pthread, this);
    if(thread_creation != 0) {
        cerr << "Failed to create thread" << endl;
        return;
    }
    m_bRunning = true;
}

TimerManager::~TimerManager() 
{
    void *result;

    pthread_mutex_lock(&m_tGoLock);
    m_bRunning = false;
    pthread_mutex_unlock(&m_tGoLock);

    pthread_join(m_tTimerThread, &result);
    pthread_mutex_destroy(&m_tGoLock);
    pthread_cond_destroy(&m_tGoLockCondition);
}

void TimerManager::run() 
{
    pthread_mutex_lock(&m_tGoLock);
    while(m_bRunning) {
        while (!m_bGo) {
            pthread_cond_wait(&m_tGoLockCondition, &m_tGoLock);
        }
        pthread_mutex_unlock(&m_tGoLock);
        if (!m_bRunning) {
            break;
        }

        struct timeval l_tv;
        usleep(max(0l, m_lMinSleep));
        gettimeofday(&l_tv, NULL);
        m_lMinSleep = 0;
        long l_lMin = 0;
        for(list<Timer>::iterator it=m_cTimers.begin(); 
                it != m_cTimers.end(); ++it) {
            TimerManager::Timer l_oTimer = *it;
            long elapsed_time = (
                    (l_tv.tv_sec * 1000000 + l_tv.tv_usec) 
                    - (l_oTimer.start));
            l_lMin = elapsed_time - l_oTimer.duration;
            if (elapsed_time >= l_oTimer.duration) {
                l_lMin = l_oTimer.duration;
                l_oTimer.callback(0, 1);
                gettimeofday(&l_tv, NULL);
                it->start = (l_tv.tv_sec * 1000000) 
                    + l_tv.tv_usec;
            }
            m_lMinSleep = min(m_lMinSleep, l_lMin);
        }
    }
}

void TimerManager::start()
{
    pthread_mutex_lock(&m_tGoLock);
    m_bGo = true;
    pthread_cond_signal(&m_tGoLockCondition);
    pthread_mutex_unlock(&m_tGoLock);
}

void TimerManager::stop() 
{
    pthread_mutex_lock(&m_tGoLock); 
    m_bGo = false;
    pthread_mutex_unlock(&m_tGoLock);
}

TimerManager::Timer TimerManager::set_up_timer(
        long micro_duration, fn callback)
{
    struct timeval l_tv;

    gettimeofday(&l_tv, NULL);
    Timer l_oTimer(micro_duration, callback);
    l_oTimer.start = (l_tv.tv_sec * 1000000) + l_tv.tv_usec;

    return l_oTimer;
}

void TimerManager::add_timer(long usec, fn callback) 
{
    pthread_mutex_lock(&m_tGoLock);
    Timer insert = set_up_timer(usec, callback);

    for (list<Timer>::iterator it = m_cTimers.begin(); 
            it != m_cTimers.end(); ++it) {
        if (*it == insert) {
            return;
        }
    }
    m_cTimers.push_back(insert);
    pthread_mutex_unlock(&m_tGoLock);
}

