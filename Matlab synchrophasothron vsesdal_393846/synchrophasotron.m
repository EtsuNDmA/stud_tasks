function [tq, RR, ANG, VVs] = synchrophasotron()

global q e U dwdE Rs c cosfis
    % �������� �����
    c = 2.8e8;
    % ���������������� ��������������
    dwdE = -8e26;
    % ��������� ����������� ��������
    Vs0 = 0.1*c;
    % ��������� �������� �������� �������
    V0 = Vs0+0.00001*c*rand(1);
    % ��������� ������
    ANG0 = 0;
    % ��������� ����
    FI0 = pi/3-pi/10 + 2*pi/10*rand(1);
    % ������� ����������� ����
    cosfis = cos(pi/3);
    % ��������� ������ ������
    R0 = V0/Vs0*sqrt(1-Vs0^2)/sqrt(1-V0^2)*Rs;
    % ��������� ������ ��������� [ANG_S Ws ANG W FI]
    X0 = [ANG0 Vs0/2/pi/Rs ANG0 V0/2/pi/R0 FI0]';
    % ��������� ��������
    odeopts = odeset(...
            'MaxStep',0.000025);
    % ������ ������������
    [t, X] = ode45(@dxdt, [0 0.001], X0, odeopts);
    % ������������ �������� ��������
    v = X(:,4)*2*pi*R0/c;
    vs = X(:,2)*2*pi*Rs/c;
    % ������������ ������ ������
    R = v./vs.*sqrt(1-vs.^2)./sqrt(1-v.^2)*Rs;
    % ������ �������
    figure
    
    subplot(4,1,1)
    plot(t, X(:,1)-X(:,3))
    title '������� � ������������ ���� ������� � ����������� �������'
    legend \theta_s-\theta
    grid on
    hold on
    
    subplot(4,1,2)
    plot(t, pi/3*ones(1,length(t)), t,  X(:,5))
    title '����'
    legend \phi_s \phi
    grid on
    hold on
    
    subplot(4,1,3)
    plot(t, X(:,2)*2*pi*Rs/c, t, X(:,4)*2*pi*R0/c)
    title '�������� ��������'
    legend v_s v
    grid on
    hold on
    
    subplot(4,1,4)
    plot(t, Rs*ones(1,length(t)), t, R)
    title '������ ������'
    legend R_s R 
    grid on
    hold on
   
    % ������������� � ������������������ ����������
    % ��� ����, ����� �� ������ ������ ���� ���������� ����� ����� 5000
    tq = linspace(t(1),t(end),5000);
    RR = interp1(t,(R-Rs)*1+Rs,tq);
    ANG = interp1(t,X(:,3),tq);
    VVs = interp1(t,vs,tq);
%     length(RR)
%     length(ANG)
%     figure
%     polar(ANG, RR)
%     comet(R.*cos(X(:,3)),R.*sin(X(:,3)))
%     plot(t(2:end)-t(1:end-1))
end

function dX = dxdt(t, X)
    global q  e U dwdE Rs cosfis
    
%     R = q/(2*pi*X(4))*sqrt(1-X(4)/X(2)*sqrt(1-(2*pi*Rs*X(2)/q)^2));
    f = 1000000/(0.01*t+0.00001);

    dX(1,1) = X(2);
    dX(2,1) = f/(2*pi*Rs);
    dX(3,1) = X(4);
    dX(4,1) = X(4)/X(2)*f/(2*pi*Rs)+q*e*U*dwdE/2/pi*(cos(X(5))-cosfis);
    dX(5,1) = q*(X(2)-X(4));
end