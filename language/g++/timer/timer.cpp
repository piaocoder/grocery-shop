#include "timer.h"

using namespace std;


Timer::Timer()
{
	this->startedAt = 0;
	this->pausedAt = 0;
	this->paused = false;
	this->started = false;
}

bool Timer::is_started()
{
	return this->started;
}

bool Timer::is_stopped()
{
	return !this->started;
}

bool Timer::is_paused()
{
	return this->paused;
}

bool Timer::is_active()
{
	return !this->paused & this->started;
}

void Timer::pause()
{
	if (this->paused || !this->started) {
		return;
    }
	this->paused = true;
	this->pausedAt = clock();
}

bool Timer::resume()
{
	if (!this->paused) {
		return false;
    }
	this->paused = false;
	this->startedAt += (clock() - this->pausedAt);

    return true;
}

void Timer::stop()
{
	this->started = false;
}

bool Timer::start()
{
	if (this->started) {
		return false;
    }
	this->started = true;
	this->paused = false;
	this->startedAt = clock();

    return true;
}

void Timer::reset()
{
	this->paused = false;
	this->startedAt = clock();
}

clock_t Timer::get_ticks()
{
	if (!this->started) {
		return 0;
    }

	if (this->paused) {
		return this->pausedAt - this->startedAt;
    }

	return clock() - this->startedAt;
}
