#include "ds18b20.h"
const int Toffset=int(0.2*16+0.5);


void DS18B20::inSetup() {
    pinMode(pin,INPUT_PULLUP);
    s1=s2=s3=0; r3=-30003;
}
int DS18B20::startReset() {
    pinMode(pin,INPUT_PULLUP);
    wt=micros()+480; s1=2;
}
void DS18B20::writeBit(int bit) {
    // Serial.print("writeBit: "); Serial.println(bit);
    if (bit) {
      noInterrupts();
      pinMode(pin,OUTPUT); digitalWrite(pin,LOW);
      //delayMicroseconds(4);
      pinMode(pin,INPUT_PULLUP);
      interrupts();
      wt=micros()+60; r1=1; s1=4;
    } else {
      noInterrupts();
      pinMode(pin,OUTPUT); digitalWrite(pin,LOW);
      delayMicroseconds(65);
      pinMode(pin,INPUT_PULLUP);
      interrupts();
      wt=micros()+5; r1=0; s1=4;
    }
}
int DS18B20::readBit() {
      noInterrupts();
      pinMode(pin,OUTPUT); digitalWrite(pin,LOW);
      //delayMicroseconds(1);
      pinMode(pin,INPUT_PULLUP);
      // delayMicroseconds(14);
      r1=digitalRead(pin)==HIGH;
      interrupts();
      wt=micros()+65; s1=4;
      // Serial.print("readBit: "); Serial.println(r1);
      return r1;
}
int DS18B20::do1() {
    if (s1==0 || s1==1) return 1;
    unsigned long t=micros();
    signed long dt=t-wt;
    if (dt<0) return 0;
    switch (s1) {
      case 2: pinMode(pin,OUTPUT); digitalWrite(pin,LOW); wt=micros()+480; s1=3; return 0;
      case 3:
        noInterrupts(); pinMode(pin,INPUT_PULLUP); delayMicroseconds(60); r1=digitalRead(pin)==HIGH; interrupts();
        wt=micros()+420; s1=5; return 0;
      case 4: s1=r1; return 1;
      case 5: s1=r1; /* Serial.print("Reset: "); Serial.println(r1); */ return 1;
      default: s1=0; return 1;
    }
}
void DS18B20::startReadWord(byte nb) {
    s2=nb; r2=0;
}
void DS18B20::startWriteWord(byte nb, unsigned long w) {
    s2=nb+100; r2=w;
}
int DS18B20::do2() {
    if (do1()==0) return 0;
    if (s2==0 || s2==100) return 1;
    if (s2>100) {
      writeBit(r2&1);
      r2>>=1;
    } else {
      r2=(unsigned)r2>>1;
      r2|=readBit()<<15;
    }
    s2--;
    if (s2==0 || s2==100) return 1;
    return 0;
}
int DS18B20::do3() {
    if (do2()==0) return 0;
    int b;
    switch (s3) {
      case 0: return 2;
      case 1: startReset(); s3=2; return 0;
      case 2: if (r1==1) { r3=-30000; s3=0; return 1; } 
              startWriteWord(16, 0x44CC); s3=4; return 0;
      case 4: b=readBit(); if (b==1) s3=5; return 0;
      case 5: startReset(); s3=6; return 0;
      case 6: if (r1==1) { r3=-30001; s3=0; return 1; }
              startWriteWord(16, 0xBECC); s3=7; return 0;
      case 7: startReadWord(16); s3=8; return 0;
      case 8: r3=r2+Toffset; s3=0; return 1;
      default: r3=-30002; s3=0; return 1;
    }
}
int DS18B20::inLoop() {
//  Serial.println(s1); Serial.println(s2); Serial.println(s3);
  if (do3()==1) {
    //Serial.print("Air temp=");
    Serial.print(r3); Serial.print(",");
    return 1;
  } else {
    return 0;
  }
}

void DS18B20::startMeasuring() { 
  //Serial.println("Air temp: start measuring");
  s3=1; s1=s2=0;
}
int DS18B20::getTemp() { return r3; }

