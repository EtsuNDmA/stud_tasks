function [eigval, eigvect] = powereig(A, eps, maxiter)
    % ������� ���������� ����������� �������� � ��������������� ���
    % ����������� ������
    [eigval(1,1), eigvect(1:size(A,1),1)] = powereigmax(A, eps, maxiter);
    % ��������� ����� �������
    AA = A-eigval(1)*eye(size(A,1));
    % ������� ���������� ����������� �������� � ��������������� ���
    % ����������� ������ ��� ������� AA
    [eigvalAA, eigvect(1:size(A,1),2)] = powereigmax(AA, eps, maxiter);
    % ������� ���������� �� ������ ����������� �������� ������� A
    eigval(2,1) = eigval(1,1)+eigvalAA;
end

function [eigval, eigvect] = powereigmax(A, eps, maxiter)
    % ������� ��������� ��������� ������
    eigvect(1:size(A,1),1) = randn(size(A,1),1);
    for i=1:maxiter
        % ������������ ��������� �������� ��� ������������ �������
        eigvect_new = A*eigvect;
        % ������������ ��������� ����������� � ������������ ��������
        eigval_new = eigvect_new(1,1)/eigvect(1,1);
        if i>1
            % ��������� ������� ��������
            if abs(eigval_new-eigval)<=eps
                eigval = eigval_new;
                eigvect = normc(eigvect_new);
                return
            end
        end
        eigval = eigval_new;
        eigvect = normc(eigvect_new);
    end
    error('�������� �� ���������� ��������� maxiter')
end

