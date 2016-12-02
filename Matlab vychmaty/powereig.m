function [eigval, eigvect] = powereig(A, eps, maxiter)
    % —читаем наибольшее собственное значение и соответствующий ему
    % собственный вектор
    [eigval(1,1), eigvect(1:size(A,1),1)] = powereigmax(A, eps, maxiter);
    % ‘ормируем новую матрицу
    AA = A-eigval(1)*eye(size(A,1));
    % —читаем наибольшее собственное значение и соответствующий ему
    % собственный вектор дл€ матрицы AA
    [eigvalAA, eigvect(1:size(A,1),2)] = powereigmax(AA, eps, maxiter);
    % —читаем наименьшее по модулю собственное значение матрицы A
    eigval(2,1) = eigval(1,1)+eigvalAA;
end

function [eigval, eigvect] = powereigmax(A, eps, maxiter)
    % ¬ыберем случайный начальный вектор
    eigvect(1:size(A,1),1) = randn(size(A,1),1);
    for i=1:maxiter
        % –ассчитываем следующую итерацию дл€ собственного вектора
        eigvect_new = A*eigvect;
        % –ассчитываем слудующее приближение к собственному значению
        eigval_new = eigvect_new(1,1)/eigvect(1,1);
        if i>1
            % ѕровер€ем условие останова
            if abs(eigval_new-eigval)<=eps
                eigval = eigval_new;
                eigvect = normc(eigvect_new);
                return
            end
        end
        eigval = eigval_new;
        eigvect = normc(eigvect_new);
    end
    error('“очность не достигнута увеличьте maxiter')
end

