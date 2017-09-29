#include "timer.h"

void CTimer::setUpAbs(unsigned long t) { wt=t; }
void CTimer::setUpRel(unsigned long dt) { wt=millis()+dt; }
void CTimer::setUpInc(unsigned long dt) { wt+=dt; }
int CTimer::isElapsed() {
  unsigned long t=millis();
  signed long dt=t-wt;
  return dt>=0;
}

