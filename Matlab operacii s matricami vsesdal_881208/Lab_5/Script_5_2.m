X = -5:0.1:5;
Y = zeros(length(X), 1);  % Заполняем Y нулями

for i = 1:length(X)
    x = X(i);
    if x < 0
        Y(i) = 3*x + sqrt(1+x^2);
    elseif x <= 1
        Y(i) = 2*cos(x) * exp(-2*x);
    else
        Y(i) = 2*sin(3*x);
    end
end

figure
plot(X, Y)
hold on
grid on
% Линии изменения куска функции
plot([0 0], [min(Y) max(Y)], 'r--')
plot([1 1], [min(Y) max(Y)], 'r--')
xlabel('X')
ylabel('Y')
title('Y(x)')