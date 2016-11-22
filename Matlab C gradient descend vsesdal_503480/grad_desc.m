function logic_result = grad_desc(func,grad,y0,e,a,b,g,n)
%grad_desc ��������� ������� ������� func
%   INPUTS
%   func - �������
%   grad - �������� ������� func
%   y0 - ��������� �����������
%   e - ��������
%   a - ��������� ���
%   b - ����������� ��������� ����
%   g - ���������������
%   n - ������������ ����� ����� ������
%   OUTPUTS
%   logic_result - true ���� �������� ���������� � n ��������, ����� false
y = zeros(n,2);
foo = zeros(1,n);
gra = zeros(n,2);
y(1,:) = y0;
for i=1:n
    foo(i) = func(y(i,:));
    gra(i,:) = grad(y(i,:));
    delta = a*gra(i,:);
    y(i+1,:) = y(i,:)-delta;
    % ��������� ������� ��� �������� ����
    foo_next = func(y(i+1,:));
    while foo_next>foo(i)-g*(delta*gra(i,:)')
        % ������ ���
        delta = delta*b;
        y(i+1,:) = y(i,:)-delta;
        foo_next = func(y(i+1,:));
        if norm(delta) < 1e-9
            error('Smth wrong')
        end
    end
    
    % ��������� ������� ��������
    if abs(foo_next-foo(i)) <= e
        foo(i+1) = foo_next;
        % ����� ���������� ���� �������� � ����
        fid = fopen('result.txt','w');
        fprintf(fid, 'N\tx1\t\tx2\t\tf\n');
        for j=1:i+1
            fprintf(fid, '%d\t%.4f\t%.4f\t%.4f\n',j-1,y(j,1),y(j,2),foo(j));
        end
        fclose(fid);
        % ������� ���������� �� �����
        fprintf('=====    Result    ====\n')
        fprintf('\tx1_min = %.4f\n\tx2_min = %.4f\n',y(i+1,:))
        fprintf('\tfu_min = %.4f\n',foo_next)
        fprintf('\tnum_steps = %d\n', i)

        logic_result = true;
        return
    end
end
% ���� ����� �� ���� ������, �� �������� �� ������������� �� n ��������
fprintf('Max step exceeded, tolerance do not satisfied')
logic_result = false;
end

