%Построение графиков элементов матричной весовой функции
close all 
 
figure 
plot(t_,w11_s,'r-',t_,w11_vm,'b--',t_,w11_a,'m-.') 
grid on 
xlabel('t, c') 
ylabel('w11') 
title('Графики элемента w11 матричной весовой функции') 
legend('w11-struct','w11-VM','w11-analit',0) 
 
figure 
plot(t_,w21_s,'r-',t_,w21_vm,'b--',t_,w21_a,'m-.') 
grid on 
xlabel('t, c') 
ylabel('w21') 
title('Графики элемента w21 матричной весовой функции') 
legend('w21-struct','w21-VM','w21-analit',0) 
 
figure 
plot(t_,w12_s,'r-',t_,w12_vm,'b--',t_,w12_a,'m-.') 
grid on 
xlabel('t, c') 
ylabel('w12') 
title('Графики элемента w12 матричной весовой функции') 
legend('w12-struct','w12-VM','w12-analit',0) 
 
figure 
plot(t_,w22_s,'r-',t_,w22_vm,'b--',t_,w22_a,'m-.') 
grid on 
xlabel('t, c') 
ylabel('w22') 
title('Графики элемента w22 матричной весовой функции') 
legend('w22-struct','w22-VM','w22-analit',0) 
 

