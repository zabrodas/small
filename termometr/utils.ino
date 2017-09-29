#include "utils.h"

int formatFixNum(int x, char *sgn, int w1, int w2, char *s) {
  char *p=s;
  if (x<0) {
    x=-x;
    if (sgn) *(p++)=sgn[1];
  } else {
    if (sgn) *(p++)=sgn[0];
  }
  p+=w1+w2; if (w2) p++;
  char *p1=p;
  for (int i=0; i<w2; i++) {
    *(--p1)=x%10+'0'; x/=10;
  }
  if (w2) *(--p1)='.';
  for (int i=0; i<w1; i++) {
    *(--p1)=x%10+'0'; x/=10;
  }
  *p=0;
  return p-s;
}

int formatTemp(int x, char *s) {
  if (x<=-30000 || x>=30000) {
    strcpy(s,"???.??");
    return 6;
  }
  return formatFixNum((x*25+2)>>2,"+-",2,2,s);
};

