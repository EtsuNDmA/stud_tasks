%�������� ������� ������������ �������: ������������ ����� 1 �������
 
%������� ���� ���������� � ������ 
clear all  
 
%������� ���������� ���� 
clc 
 
%�������� ���� ���������� �������� 
set(0,'ShowHiddenHandles','on') 
delete(get(0,'Children')) 
 
%�������� ������������� ����� 1 ������� (N_zv = 3) ����� ��� ������������ �������  
%��� ��������� ��������� ����������. ��������� ������������� ����� 1 �������
%�������� �������� inp_param = [k,T]
 
%��������� k 
param{1} = [1,1];
param{2} = [2,1];
param{3} = [3,1];
 
%��������� � 
param{4} = [1,0.354];
param{5} = [1,0.707];
param{6} = [1,1.414];
 
%���������� ��������� ������������� 
plotsys(3,param(1:3),'k');
plotsys(3,param(4:6),'T');
