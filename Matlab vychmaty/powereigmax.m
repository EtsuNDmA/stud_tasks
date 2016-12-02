function [eigval, eigvect] = powereigmax(A, eps, maxiter)
    % Выберем случайный начальный вектор
    eigvect(1:size(A,1),1) = randn(size(A,1),1);
    for i=1:maxiter
        % Рассчитываем следующую итерацию для собственного вектора
        eigvect_new = A*eigvect;
        % Рассчитываем слудующее приближение к собственному значению
        eigval_new = eigvect_new(1,1)/eigvect(1,1);
        if i>1
            % Проверяем условие останова
            if abs(eigval_new-eigval)<=eps
                eigval = eigval_new;
                eigvect = normc(eigvect_new);
                return
            end
        end
        eigval = eigval_new;
        eigvect = normc(eigvect_new);
    end
    error('Точность не достигнута увеличьте maxiter')
end

