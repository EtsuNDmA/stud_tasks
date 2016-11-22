
function synchrophasotron1()
close all
global q e U dTdE Rs
    % Скорость света
    
    % Заряд частицы
    e = 1e-9;
    % Кратность ускорения
    q = 1;
    % Ускоряющее напряжение
    U = 1000;
    % Число частиц
    N = 1;
    % Радиус ускорителя, м
    Rs = 1000/2.8e8;
    % Длина окружности ускорителя, м
    Ls = 2*pi*Rs;
    % Дифференциальная характеристика
    dTdE = 0;
    % Начальная равновесная скорость
    Vs0 = 0.6;
    % Начальная линейная скорость частиц
    V0 = Vs0;

    R0 = Rs;
    
    FIs0 = 0;
    Ws0 = q/Ls*Vs0;
    dE0 = 0;
    W0 = q/(2*pi*R0)*V0;

    X0 = [FIs0 Ws0 FI0 W0]';

    odeopts = odeset(...
            'AbsTol', 1e-6,...
            'Reltol', 1e-3);

    [t, X] = ode45(@dxdt, [0 0.1], X0, odeopts);
    
    figure
    plot(t, 2*pi*Rs/q*X(:,2))
    hold on
    plot(t, 2*pi*Rs/q*X(:,4))
    
    figure
    subplot(2,1,1)
    plot(t, X(:,1), t, X(:,3))
    legend FIs FI
    
    subplot(2,1,2)
    plot(t, X(:,2), t, X(:,4))
    legend Ws W
end

function dX = dxdt(t, X)
    global q  e U dTdE Rs
    
%     R = q/(2*pi*X(4))*sqrt(1-X(4)/X(2)*sqrt(1-(2*pi*Rs*X(2)/q)^2));
    f = 1/sqrt(t^2-t+1);
    
    dX(1,1) = X(2);
    dX(2,1) = f/(2*pi*Rs);
    dX(3,1) = X(4);
    dX(4,1) = 3*f/(2*pi*Rs)/X(2)*X(4)+q*e*U*dTdE/4/pi^2*X(2)^3*(cos(X(3))-cos(X(1)));

end