%Построение графиков элементов матричной переходной функции 
% 
close all 
 
figure 
plot(t_,h11_s,'r-',t_,h11_vm,'b--',t_,h11_a,'m-.') 
grid on 
xlabel('t, c') 
ylabel('h11') 
title('Графики элемента h11 матричной переходной функции') 
legend('h11-struct','h11-VM','h11-analit',0) 
 
figure 
plot(t_,h21_s,'r-',t_,h21_vm,'b--',t_,h21_a,'m-.') 
grid on 
xlabel('t, c') 
ylabel('h21') 
title('Графики элемента h21 матричной переходной функции') 
legend('h21-struct','h21-VM','h21-analit',0) 
 
figure 
plot(t_,h12_s,'r-',t_,h12_vm,'b--',t_,h12_a,'m-.') 
grid on 
xlabel('t, c') 
ylabel('h12') 
title('Графики элемента h12 матричной переходной функции') 
legend('h12-struct','h12-VM','h12-analit',0) 
 
figure 
plot(t_,h22_s,'r-',t_,h22_vm,'b--',t_,h22_a,'m-.') 
grid on 
xlabel('t, c') 
ylabel('h22') 
title('Графики элемента h22 матричной переходной функции') 
legend('h22-struct','h22-VM','h22-analit',0) 