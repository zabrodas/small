
static const byte NUM_ADC_CHAN=6;
static const byte NUM_DMX_CHAN=7;
static const byte commutator[NUM_DMX_CHAN]={3,0,1,2,3,4,5};
static int adcPrev[NUM_ADC_CHAN];
static const int HISTERESIS=8;

void setup() {
  Serial.begin(115200);
  Serial.println("ttttt");
  for (byte i=0; i<NUM_ADC_CHAN; i++) adcPrev[i]=-32767;
}


void loop() {
  byte adc[NUM_ADC_CHAN];
  for (byte i=0; i<NUM_ADC_CHAN; i++) {
    int v=analogRead(i);

    if (abs(v-adcPrev[i])<HISTERESIS) {
      v=adcPrev[i];
    } else {
      adcPrev[i]=v;
    }
    
    if (i<4) v=1023-v;
    adc[i]=v>>2;
  }

  byte dmx[NUM_DMX_CHAN];
  for (int i=0; i<NUM_DMX_CHAN; i++) dmx[i]=adc[commutator[i]];
  //dmx[0]=dmx[1]=dmx[2]=dmx[3]=255;
  dmx[4]=dmx[5]>20 ? max(dmx[6],20) : 0;
  //dmx[5]=50;
  //dmx[6]=0;
  //dmx[6]=0;
  //dmx[7]=0;
  
#if 1
  Serial.begin(50000,SERIAL_8N2);
  Serial.write(0);
  Serial.begin(250000,SERIAL_8N2);
  Serial.write(0);
  for (int i=0; i<NUM_DMX_CHAN; i++) Serial.write(dmx[i]);
#endif

  delay(10);
}

