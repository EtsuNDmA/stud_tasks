% ������� ����� � ����������
clc
clear
close all
% ������� ������ x �� 0,05 �� 1 � ����� 0,05
x=0.05:0.05:1;
% ������������ �������� ������� � ����� 0,05
f=func01(x);

% ������ ������ � ������� Plot
figure % ��������� ����� ����
plot(x,f) % ������ ������
grid on % �������� �����

% ������ ������ � ������� fplot
limits=[0.05 1];
figure % ��������� ����� ����
fplot(@func01,limits) % ������ ������
grid on % �������� �����