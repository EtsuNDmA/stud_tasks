clc
clear all
close all
% Начальные условия
y0=[0 0 0 0 0 0];
% Начальное время моделирвания
t0=0;
% Конечное время моделирования
tf=0.2;
% Решения системы дифуров
[t,y]=ode45('difur',[t0 tf],y0);

% Параметры задачи
R1=40;
R2=12;
R3=15;
C1=25e-6;
C2=45e-6;
C3=60e-6;
C4=25e-6;
L1=30e-3;
L2=30e-3;
% Результаты
Uc1=y(:,1);
Uc2=y(:,2);
Uc3=y(:,3);
Uc4=y(:,5);
i4=y(:,6);
i5=y(:,6);

i3=i4+i5;
i2=(120*sin(120*t)-Uc1-Uc2-R1*i3)/(R1+R2);
i1=i2+i3;
% Построение графиков
figure
plot(t,[i1 i2 i3 i4 i5])
legend i1 i2 i3 i4 i5
xlabel 't, sec'
ylabel 'i, A'
grid on

figure
plot(t,[Uc1 Uc2 Uc3 Uc4])
legend Uc1 Uc2 Uc3 Uc4
xlabel 't, sec'
ylabel 'U, V'
grid on