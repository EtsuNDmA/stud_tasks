function c = lsquares(x,y,k)
% Базисные функции phi_i(x)=x^k

    A = zeros(k+1,k+1);
    b = zeros(k+1,1);
    for i=1:k+1
        for j=1:k+1
          sumA = 0;
          sumB = 0;
            for n=1:length(x)
                sumA = sumA+x(n)^(i-1)*x(n)^(j-1);
                sumB = sumB+y(n)*x(n)^(i-1);
            end
          A(i,j) = sumA;
          b(i,1) = sumB;
        end
    end
    % Решаем систему линейных уравнений Ac=b
    c = A\b;
end


