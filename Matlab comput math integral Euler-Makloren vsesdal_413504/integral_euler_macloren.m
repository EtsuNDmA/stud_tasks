function int = integral_euler_macloren(N)
% Вычисляет \int\limits_{-1}^{1} dx/(x^2+1)

if N<2
    fprintf('Ошибка! N Должно быть >=2')
    int=NaN;
else
    h=2/N;
    x=-1:h:1;
    f=1./(x.^2+1);
    int=h*(0.5*f(1)+0.5*f(N+1)+sum(f(2:N)))+1/12*h^2*(0.5+0.5);
end

end

