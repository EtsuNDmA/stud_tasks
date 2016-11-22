#include "root_eq.h"

double rootEq(func1 f , func1 df_dx , func1 df_dx2, double a , double b , double eps , int n )
{ double xh,xk;
  int i;
  if(f(a)*df_dx2(a)>0)
   {  xh=b;
      xk=a;
   }
  else
  {  xh=a;
     xk=b;
  }

  while(fabs(xk-xh)>eps && i++<=n)
  {  xk=xk-f(xk)/df_dx(xk);
     xh=xh-f(xh)*(xk-xh)/(f(xk)-f(xh));
  }
  return (xk+xh)/2;
}
