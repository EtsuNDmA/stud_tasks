function f=zadacha03(x)
    if x<1
        fprintf('������� �� ���������� ��� ������� �������� x, ������� x �� 1 �� 12\n')
        f=NaN;
    elseif x<=exp(1)
        f=log(x);
    elseif x<=9
        f=x/exp(1);
    elseif x<=12
        f=exp(8-x);
    else
        fprintf('������� �� ���������� ��� ������� �������� x, ������� x �� 1 �� 12\n')
        f=NaN;
    end;
end
