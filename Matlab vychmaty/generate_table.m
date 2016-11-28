function [x, y] = generate_table(a, b, n)
   x = linspace(a,b,n);
   y = sin(x.^2).*exp(0.3*x); % TODO вставить функцию
end