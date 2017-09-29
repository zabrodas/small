#pragma once

class DS18B20  {
  byte pin;
  byte s1,r1; unsigned long wt;
  byte s2; unsigned long r2;
  byte s3; int r3;

  int startReset();
  void writeBit(int bit);
  int readBit();
  int do1();
  void startReadWord(byte nb);
  void startWriteWord(byte nb, unsigned long w);
  int do2();
  int do3();
public:
  DS18B20(int pin_) { pin=pin_; }
  void startMeasuring();
  int getTemp();
  void inSetup();
  int inLoop(); // 1 - if new temp available
};

