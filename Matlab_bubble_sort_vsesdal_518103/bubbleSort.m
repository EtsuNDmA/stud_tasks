function array = bubbleSort(array)
    itemCount = length(array); % ���������� ��������� � �������
    while itemCount>=2 % ����������� ����� ����������� ��������� 2 ��������
        itemCount = itemCount-1; % �� ������ �������� ��������� ����� ��������������� ���������
        for i = (1:itemCount)
            if(array(i) > array(i+1))
                array([i i+1]) = array([i+1 i]); %���������� �������� �������
            end
        end
    end
end
