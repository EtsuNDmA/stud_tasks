x1 = 2:0.001:4;
y1 = 5 * tan(0.5*x1) ./ (-x1+3) ./ (x1+1);

x2 = 0:0.1:20;
y2 = sin(0.5*x2) - 1;

days = 1:2:30;
temperature = [8 9 6 3 7 14 12 6 6 8 14 5 6 4 4 ...
               4 2 34 4 7 7 6 8 10 13 12 9 19 20];
           
subplot(1,2,1); plot(x1,y1)
title('Функция 1')
legend('y1=5*tan(0.5*x./(-x+3)./(x+1)')
xlabel('x')
ylabel('y')
grid on
subplot(1,2,2); polar(x2,y2)
legend('y2=cos(2.*x)')
xlabel('x')
ylabel('y')
title('Функция 2')
figure
bar(days,temperature(days))
grid on
xlabel('Day')
ylabel('Temperatyre, C')
title('Температура')
