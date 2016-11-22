function result = grad(x)
%grad градиент целевой функции
result = [x(2)-50/x(1)^2, x(1)-20/x(2)^2];
end

