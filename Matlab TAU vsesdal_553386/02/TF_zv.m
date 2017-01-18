%Функция описания звена в виде передаточной функции 
% 
function W = TF_zv(N_zv,inp_param) 
  p = tf('p'); 
  switch N_zv 
    case 1,         %инерционное звено, N_zv = 1, inp_param = [k,T] 
      k = inp_param(1); 
      T = inp_param(2); 
      W = k/(T*p+1);   
    case 2,         %колебательное звено, N_zv = 2, inp_param = [k,T,ksi] 
      k = inp_param(1); 
      T = inp_param(2); 
      ksi = inp_param(3); 
      W = k/(T^2*p^2+2*ksi*T*p+1);
    case 3,         %неустойчивое звено 1-го пор., N_zv = 3, inp_param = [k,T] 
      k = inp_param(1); 
      T = inp_param(2); 
      W = k/(T*p-1);   
  end 
%end of function TF_zv 
