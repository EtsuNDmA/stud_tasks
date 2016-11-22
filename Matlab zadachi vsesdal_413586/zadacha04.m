function N = zadacha04(vect)
% Определить количество положительных элементов вектора,
% расположенных между его максимальным и минимальным элементами

% Сначала проверим, что введен именно вектор
if (size(vect,1)==1 && size(vect,2)>1) || (size(vect,2)==1 && size(vect,1)>1)
    % Найдем максимальный и минимальный элементы
    max_el=max(vect);
    min_el=min(vect);
    % Найдем индексы максимального и минимального элементов, если элементов с 
    % таким значением несколько, выбираем только первый
    max_el_index=find(vect==max_el,1);
    min_el_index=find(vect==min_el,1);
    % Выделим элементы между max_el и min_el в отдельный вектор
    if max_el_index>min_el_index
        newvect = vect(min_el_index+1:max_el_index-1);
    else
        newvect = vect(max_el_index+1:min_el_index-1);
    end;
    % Найдем индексы положительных элементов
    posindexes=find(newvect>0);
    % Посчитаем их количество
    N = length(posindexes);
else
    fprintf('Ошибка! vect не является вектором')
    N= NaN;
end