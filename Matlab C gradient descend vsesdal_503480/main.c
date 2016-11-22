#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

typedef double* (*functype)(const double*) ;

double* func(const double* x)
{
    double* f = (double*)malloc(sizeof(double));
    *f = x[0]*x[1]+50/x[0]+20/x[1];
    return f;
}

double* grad(const double *x)
{
    double* g = (double*)malloc(2 * sizeof(double));
    g[0] = x[1]-50/(x[0]*x[0]);
    g[1] = x[0]-20/(x[1]*x[1]);
    return g;
}

int grad_desc(functype func, functype grad,
             double* y0, double e, double alpha, double beta, double gamma, int n)
{
    double y[n+1][2];
    double f_arr[n+1];
    double delta[2];
    y[0][0] = y0[0];
    y[0][1] = y0[1];

    for(int i=0; i<=n; i++){
        double* f = func(y[i]);
        double* g = grad(y[i]);

        delta[0] = alpha*g[0];
        delta[1] = alpha*g[1];
        y[i+1][0] = y[i][0]-delta[0];
        y[i+1][1] = y[i][1]-delta[1];

        // проверяем условие для величины шага
        double* f_next = func(y[i+1]);
        for(int j=0; j<=10; j++){
            if(*f_next>*f-gamma*(delta[0]*g[0]+delta[1]*g[1])){
                // дробим шаг
                free(f_next);
                delta[0] *= beta;
                delta[1] *= beta;
                y[i+1][0] = y[i][0]-delta[0];
                y[i+1][1] = y[i][1]-delta[1];
                f_next = func(y[i+1]);
                if(sqrt(delta[0]*delta[0]+delta[1]*delta[1])<1e-9 ){
                    printf("Smth wrong!");
                    return 0;
                }
            }
            else break;
        }
        // сохраняем результаты в массив
        f_arr[i] = *f;

        // проверяем условие останова
        if (fabs(*f_next-*f) <= e){
            f_arr[i+1] = *f_next;

            FILE *fl = fopen("results.txt", "w");
            if (fl == NULL)
            {
                printf("Error opening file!\n");
                exit(-1);
            }
            fprintf(fl, "N\tx1\t\tx2\t\tf\n");
            for(int k=0;k<=i+1;k++){
                fprintf(fl, "%d\t%.4f\t%.4f\t%.4f\n",k ,y[k][0] ,y[k][1], f_arr[k]);
            }
            fclose(fl);
            // выводим результаты на экран
            printf("=====    Result    ====\n");
            printf("\tx1_min = %.4f\n\tx2_min = %.4f\n", y[i+1][0], y[i+1][1]);
            printf("\tfu_min = %.4f\n", f_arr[i+1]);
            printf("\tnum_steps = %d\n", i+1);
            free(f_next);
            return 1;
        }
        free(f_next);
        free(f);
        free(g);
    }
    printf("Tolerance do not satisfied\n");
    return 0;
}

int main()
{
    double y0[] = {1.0, 1.0};
    int r = grad_desc(func, grad, y0, 0.01, 1, 0.2, 0.1, 10);
    printf("Answer %d", r);
    return 0;
}
