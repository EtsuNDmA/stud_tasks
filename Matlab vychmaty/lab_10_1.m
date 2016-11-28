clc
clear all
close all

a = 0;
b = 2;
n = 5;

% Создаем таблицу значений
[x_table, y_table] = generate_table(a, b, n);
fprintf('Таблица значений:\n')
fprintf('x:')
fprintf(' %.4f', x_table)
fprintf('\n')
fprintf('y:')
fprintf(' %.4f', y_table)
fprintf('\n')
% Применяем МНК
c1 = lsquares(x_table,y_table,1);
c2 = lsquares(x_table,y_table,2);
c3 = lsquares(x_table,y_table,3);
% Выведем аппроксимирующие функции
fprintf('Аппроксимирующие функции:\n')
fprintf('Phi1(x) = %.4f + %.4f*x\n',c1)
fprintf('Phi2(x) = %.4f + %.4f*x + %.4f*x^2\n',c2)
fprintf('Phi3(x) = %.4f + %.4f*x + %.4f*x^2 + %.4f*x^3\n',c3)
% Значения точной функции
[x, y] = generate_table(a, b, 100);
% Значения аппроксимирующих функций
Phi1 = c1(1)+c1(2).*x;
Phi2 = c2(1)+c2(2).*x+c2(3).*x.^2;
Phi3 = c3(1)+c3(2).*x+c3(3).*x.^2+c3(4).*x.^3;
% Строим графики
plot(x_table,y_table,'o')
hold on
plot(x,y)
plot(x,Phi1)
plot(x,Phi2)
plot(x,Phi3)
legend('table','real','Phi1','Phi2','Phi3')
grid on
