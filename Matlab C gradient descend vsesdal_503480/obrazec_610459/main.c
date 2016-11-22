#include <stdio.h>
#include <stdlib.h>
#include "root_eq.h"
#include <math.h>

double f1( double x )
{  return 2*x+ log10(x) + 0.5;
}
double df1_dx( double x )
{  return 2+ 1/(x*log(10));
}
double df1_dx2( double x )
{  return -log(10)/(log(10)*log(10)*x*x);
}

double f2(double x)
{ return x*x*x+ x*x/5 + x/2 + 0.8;
}
double df2_dx(double x)
{ return 3*x*x+ 0.4*x + 0.5;
}
double df2_dx2(double x)
{ return 6*x + 0/8;
}


int main()
{   double a1=0.01,b1=0.5,a2=-1,b2=-0.5,eps,x1,x2;
    int n;
   // puts("Input [a1;b1] :");
   // scanf("%lf%lf",&a1,&b1);
    puts("Input eps :");
    scanf("%lf",&eps);
    puts("Input n :");
    scanf("%d",&n);
    x1=rootEq(f1,df1_dx, df1_dx2 , a1 ,b1 , eps , n);
   // puts("Input [a1;b1] :");
   // scanf("%lf%lf",&a2,&b2);
    x2=rootEq(f2,df2_dx,df2_dx2, a2 ,b2 , eps , n);
    printf("x1=%lf , x2 = %lf",x1,x2);
    return 0;
}
