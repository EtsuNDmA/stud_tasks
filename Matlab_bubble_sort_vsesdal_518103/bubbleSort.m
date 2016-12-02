function array = bubbleSort(array)
    itemCount = length(array); % Количество элементов в массиве
    while itemCount>=2 % Остановимся когда отсортируем последние 2 элемента
        itemCount = itemCount-1; % На каждой итерации уменьшаем число просматриваемых элементов
        for i = (1:itemCount)
            if(array(i) > array(i+1))
                array([i i+1]) = array([i+1 i]); %Обмениваем элементы местами
            end
        end
    end
end
