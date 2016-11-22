#ifndef ROOT_EQ_H_INCLUDED
#define ROOT_EQ_H_INCLUDED
#include <math.h>
typedef double (*func1)(double) ;

double rootEq(func1 f , func1 df_dx , func1 df_dx2, double a , double b , double eps , int n );


#endif // ROOT_EQ_H_INCLUDED
