#pragma once

class CTimer {
  unsigned long wt;
public:
  void setUpAbs(unsigned long t);
  void setUpRel(unsigned long dt);
  void setUpInc(unsigned long dt);
  int isElapsed();
};

