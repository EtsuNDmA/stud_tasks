MA = [-4.4 10.6  -1.1  0;
      0    -15.9 -4.1  2.23;
      -4.2 4.2   -17.1 -4.3;
      47.3 -12.4 11.7  -0.54];
CD=0.5;
a = min(Cod_F1);
b = max(Cod_F1);
MB = a + (b-a).*rand(4,4);
CE = mean(Cod_F1);

format short e
X1 = MA + MB;
X2 = MA / CD;
X3 = MB.^CE;
X4 = MB * X2;

Y1 = sort(X1, 1, 'descend');
Y2 = cumsum(X2, 2);
Y3 = max(X3, 2);
Y4 = tril(MB);
Y5_MA = det(MA);
Y5_MB = det(MB);
Y6 = diag(MA);


