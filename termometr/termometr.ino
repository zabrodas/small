#include <LiquidCrystal.h>
#include "timer.h"
#include "ds18b20.h"
#include "utils.h"
LiquidCrystal display(2, 3, 4, 5, 6, 7);

CTimer onePps;
DS18B20 tempSensor(8);
int lastTemp = -30000;
int estTemp = -30000;
int estTempErr2 = -30000;
int estTemp2 = -30000;
int ConvCnt = 0;

static const char *progress4[] = {"*", " ", "*", " "};

static const byte predictorTabLen = 30;
static const int16_t PROGMEM predictorTab[predictorTabLen + 1][predictorTabLen] = {
  { -1188, -1077, -969, -862, -758, -657, -557, -460, -365, -272, -181, -92, -5,
    80, 163, 245, 325, 403, 479, 553, 626, 698, 767, 836, 902, 968, 1031,
    1094, 1155, 1215
  },
  { 605, 565, 527, 490, 453, 417, 382, 347, 314, 281, 249, 217, 187, 156, 127,
    98, 70, 43, 16, -11, -37, -62, -86, -111, -134, -157, -180, -202, -223,
    -245
  }, {
    565, 529, 494, 460, 426, 393, 361, 330, 299, 269, 239, 211, 182, 155,
    128, 101, 76, 50, 26,
    2, -22, -45, -68, -90, -111, -133, -153, -173, -193, -213
  }, {
    527, 494, 462,
    431, 400, 370, 341, 312, 284, 257, 230, 204, 178, 153, 129, 105, 81, 58, 36,
    14, -8, -29, -49, -70, -89, -108, -127, -146, -164, -181
  }, {
    490, 460, 431,
    403, 375, 348, 321, 296, 270, 245, 221, 197, 174, 152, 129, 108, 86, 66, 45,
    25, 6, -13, -32, -50, -68, -85, -102, -119, -135, -151
  }, {
    453, 426, 400,
    375, 350, 326, 302, 279, 256, 234, 212, 191, 170, 150, 130, 111, 92, 73, 55,
    37, 20, 3, -14, -30, -46, -62, -77, -92, -107, -121
  }, {
    417, 393, 370, 348,
    326, 304, 283, 263, 243, 223, 204, 185, 166, 148, 131, 114,
    97, 80, 64, 48, 33, 18, 3, -11, -26, -39, -53, -66, -79, -92
  }, {
    382,
    361, 341, 321, 302, 283, 265, 247, 229, 212, 195, 179, 163, 147, 132, 116,
    102, 87, 73, 59, 46, 33, 20, 7, -5, -17, -29, -41, -52, -63
  }, {
    347, 330, 312,
    296, 279, 263, 247, 231, 216, 202, 187, 173, 159, 146, 132, 119, 107, 94, 82,
    70, 59, 47, 36, 25, 15, 4, -6, -16, -26, -35
  }, {
    314, 299, 284, 270, 256, 243,
    229, 216, 204, 191, 179, 167, 155, 144, 133, 122, 111, 101, 91, 81, 71, 61,
    52, 43, 34, 25, 17, 8, 0, -8
  }, {
    281, 269,
    257, 245, 234, 223, 212, 202, 191, 181, 171, 161, 152, 143, 134, 125, 116,
    108, 99, 91, 83, 75, 68, 60, 53, 46, 39, 32, 26, 19
  }, {
    249, 239, 230, 221,
    212, 204, 195, 187, 179, 171, 163, 156, 149, 141, 134, 127, 121, 114, 108,
    101, 95, 89, 83, 77, 72, 66, 61, 55, 50, 45
  }, {
    217,
    211, 204, 197, 191, 185, 179, 173, 167, 161, 156, 150, 145, 140, 135, 130,
    125, 120, 116, 111, 107, 102, 98, 94, 90, 86, 82, 78, 74, 71
  }, {
    187, 182,
    178, 174, 170, 166, 163, 159, 155, 152, 149, 145, 142, 139, 136, 132, 129,
    126, 124, 121, 118, 115, 113, 110, 108, 105, 103, 100, 98, 96
  }, {
    156, 155,
    153, 152, 150, 148, 147, 146, 144, 143, 141, 140, 139, 137, 136, 135, 134,
    133, 131, 130, 129, 128, 127, 126, 125, 124, 123, 122, 121, 120
  }, {
    127, 128,
    129, 129, 130, 131, 132, 132, 133, 134, 134, 135, 136, 136, 137, 137, 138,
    138, 139, 140, 140, 141, 141, 142, 142, 143, 143, 143, 144, 144
  }, {
    98, 101,
    105, 108, 111, 114, 116, 119, 122, 125, 127, 130, 132, 135, 137, 140, 142,
    144, 146, 149, 151, 153, 155, 157, 159, 161, 162, 164, 166, 168
  }, {
    70, 76,
    81, 86, 92, 97, 102, 107, 111, 116, 121, 125, 129, 134, 138, 142, 146, 150,
    154, 157, 161, 165, 168, 172, 175, 178, 181, 185, 188, 191
  }, {
    43, 50, 58, 66,
    73, 80, 87, 94, 101, 108, 114, 120, 126, 133, 138, 144, 150, 155, 161, 166,
    171, 176, 181, 186, 191, 196, 200, 204, 209, 213
  }, {
    16, 26, 36, 45, 55, 64,
    73, 82, 91, 99, 108, 116, 124, 131, 139, 146, 154, 161, 168, 175, 181, 188,
    194, 200, 206, 212, 218, 224, 230, 235
  }, {
    -11, 2, 14, 25, 37, 48, 59, 70, 81,
    91, 101, 111, 121, 130, 140, 149, 157, 166, 175, 183, 191, 199, 207, 214,
    222, 229, 236, 243, 250, 256
  }, {
    -37, -22, -8, 6, 20, 33, 46,
    59, 71, 83, 95, 107,
    118, 129, 140, 151, 161, 171, 181, 191, 201, 210, 219, 228, 237, 245, 253,
    262, 270, 277
  }, {
    -62, -45, -29, -13,
    3, 18, 33, 47, 61, 75, 89, 102, 115, 128, 141, 153, 165, 176, 188, 199,
    210, 221, 231, 241, 251, 261, 270, 280, 289, 298
  }, {
    -86, -68, -49, -32, -14,
    3, 20, 36, 52, 68, 83, 98, 113, 127, 141, 155, 168, 181, 194, 207, 219, 231,
    243, 254, 265, 276, 287, 298, 308, 318
  }, {
    -111, -90, -70, -50, -30, -11, 7,
    25, 43, 60, 77, 94, 110, 126, 142, 157, 172, 186, 200, 214, 228, 241, 254,
    267, 279, 292, 303, 315, 326, 338
  }, {
    -134, -111, -89, -68, -46, -26, -5, 15,
    34, 53, 72, 90, 108, 125, 142, 159, 175, 191, 206, 222, 237, 251, 265, 279,
    293, 306, 319, 332, 345, 357
  }, {
    -157, -133, -108, -85, -62, -39, -17, 4, 25,
    46, 66, 86, 105, 124, 143, 161, 178, 196, 212, 229, 245, 261, 276, 292,
    306, 321, 335, 349, 362, 376
  }, {
    -180, -153, -127, -102, -77, -53, -29, -6,
    17, 39, 61, 82, 103, 123, 143, 162, 181, 200, 218, 236, 253, 270, 287, 303,
    319, 335, 350, 365, 380, 394
  }, {
    -202, -173, -146, -119, -92, -66, -41, -16,
    8, 32, 55, 78, 100, 122, 143, 164, 185, 204, 224, 243, 262, 280, 298, 315,
    332, 349, 365, 381, 397, 412
  }, {
    -223, -193, -164, -135, -107, -79, -52, -26,
    0, 26, 50, 74, 98, 121, 144, 166, 188, 209,
    230, 250, 270, 289, 308, 326, 345, 362, 380, 397, 413, 429
  }, {
    -245, -213,
    -181, -151, -121, -92, -63, -35, -8, 19, 45, 71, 96, 120, 144, 168, 191, 213,
    235, 256, 277, 298, 318, 338, 357, 376, 394, 412, 429, 447
  }
};

static const byte predictorTabScale = 12;
byte tempQueueIndex = 0;
int tempQueue[predictorTabLen];

int sv(int tbl_i, int temp_i) {
  int j = temp_i;
  long ts = 0;
  for (int i = 0; i < predictorTabLen; i++) {
    int pt = (int16_t)pgm_read_word_near(&predictorTab[tbl_i][i]);
    ts += (long)pt * tempQueue[j];
    if (++j >= predictorTabLen) j = 0;
  }
  int res = (ts + (1 << (predictorTabScale - 1))) >> predictorTabScale;
  return res;
}

void predictor() {
  if (lastTemp <= -30000) {
    estTemp = -30000;
    return;
  }

  //Serial.print("predictor:");
  estTemp = sv(0, tempQueueIndex);
  long terr = 0;
  byte j = tempQueueIndex;
  for (int i = 1; i <= predictorTabLen; i++) {
    int err = sv(i, tempQueueIndex) - tempQueue[j];
    terr += long(err) * err;
    if (++j >= predictorTabLen) j = 0;
  }
  terr /= predictorTabLen;
  estTempErr2 = (int)terr;
  Serial.print(lastTemp); Serial.print("->"); Serial.print(estTemp); Serial.print(":"); Serial.println(estTempErr2);
}

int predictor2(int lt) {
  int t1=tempQueue[tempQueueIndex];
  int i2=tempQueueIndex+predictorTabLen/2; if (i2>=predictorTabLen) i2-=predictorTabLen;
  int t2=tempQueue[i2];
  int t3=lt;
  
  int t0=t2;
  int d1=t2-t1;
  int d2=t3-t2;
  if (d1==0 || d2==0  || d1==d2) {
    estTemp2=t3;
  } else {
    long d1d2=(long)d1*d2;
    int d1md2=d1-d2;
    Serial.print("p2: t1="); Serial.print(t1);
    Serial.print(" t2="); Serial.print(t2);
    Serial.print(" t3="); Serial.print(t3);
    Serial.print(" d1="); Serial.print(d1);
    Serial.print(" d2="); Serial.print(d2);
    estTemp2=(d1d2+(d1md2>>1))/d1md2+t0;
    Serial.print(" et="); Serial.println(estTemp2);
  }
}

void onTempAvailable() {
  ConvCnt++;
  display.setCursor(7, 0); display.print(progress4[ConvCnt & 3]);
  int t = tempSensor.getTemp();
  if (t <= -30000) {
    estTemp2=t;
  } else if (lastTemp <= -30000) {
    for (int i = 0; i < predictorTabLen; i++) tempQueue[i] = t;
    tempQueueIndex = 0;
    estTemp2=t;
  } else {
    // predictor2(t);
    tempQueue[tempQueueIndex] = t;
    if (++tempQueueIndex >= predictorTabLen) tempQueueIndex = 0;
  }
  lastTemp = t;
  predictor();
  char s[10];
  formatTemp(lastTemp, s); display.setCursor(0, 0); display.print(s); display.print(" ");

  // formatTemp(estTemp2, s); display.setCursor(0, 1); display.print(s); display.print("  ");
  #if 1
  if (estTempErr2 <= 32) {
    formatTemp(estTemp, s); display.setCursor(0, 1); display.print(s); display.print("  ");
  } else {
    display.setCursor(0, 1); display.print("        ");
  }
  #endif
}


void setup() {
  Serial.begin(115200);
  Serial.println("Termometr start");
  display.begin(16, 2);
  display.setCursor(0, 0); display.print("TermStrt");
  tempSensor.inSetup();
  onePps.setUpRel(1000);

}


void loop() {
  if (tempSensor.inLoop()) {  // new data available
    onTempAvailable();
  }

  if (onePps.isElapsed()) {
    onePps.setUpInc(1000);
    tempSensor.startMeasuring();
  }
}



