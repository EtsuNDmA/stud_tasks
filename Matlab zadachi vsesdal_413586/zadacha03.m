function f=zadacha03(x)
    if x<1
        fprintf('Функция не определена для данного значения x, введите x от 1 до 12\n')
        f=NaN;
    elseif x<=exp(1)
        f=log(x);
    elseif x<=9
        f=x/exp(1);
    elseif x<=12
        f=exp(8-x);
    else
        fprintf('Функция не определена для данного значения x, введите x от 1 до 12\n')
        f=NaN;
    end;
end
