function area = check_area(point)
    % �������� �������� �� ����� � ����������
    % ��� ����� �������� ����� ������� CP
    % ��� � - ����� ����������, � ������� �����
    center = [1 -1];
    radius = 4;
    CP = point-center;
    length = sqrt(CP(1)^2+CP(2)^2);
    
    % �������� ���� ������ ��� ���� ����� �����
    % ��������� ������ y = 2x - 3
    % �������� ���������� delta = P_y - (2*P_x-3)
    delta = point(2)-(2*point(1)-3);
    
    
    if length <= radius
        % ������ � ����������, ������ ������� 2 ��� 3
        % �������� ���� ������ ��� ���� ����� �����
        if delta >= 0
            area = 2;
        else
            area = 3;
        end
        
    else
        % �� ������ � ����������, ������ ������� 1 ��� 4
        % �������� ���� ������ ��� ���� ����� �����
        if delta >= 0
            area = 1;
        else
            area = 4;
        end
    end
end

