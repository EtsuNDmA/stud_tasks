function N = zadacha04(vect)
% ���������� ���������� ������������� ��������� �������,
% ������������� ����� ��� ������������ � ����������� ����������

% ������� ��������, ��� ������ ������ ������
if (size(vect,1)==1 && size(vect,2)>1) || (size(vect,2)==1 && size(vect,1)>1)
    % ������ ������������ � ����������� ��������
    max_el=max(vect);
    min_el=min(vect);
    % ������ ������� ������������� � ������������ ���������, ���� ��������� � 
    % ����� ��������� ���������, �������� ������ ������
    max_el_index=find(vect==max_el,1);
    min_el_index=find(vect==min_el,1);
    % ������� �������� ����� max_el � min_el � ��������� ������
    if max_el_index>min_el_index
        newvect = vect(min_el_index+1:max_el_index-1);
    else
        newvect = vect(max_el_index+1:min_el_index-1);
    end;
    % ������ ������� ������������� ���������
    posindexes=find(newvect>0);
    % ��������� �� ����������
    N = length(posindexes);
else
    fprintf('������! vect �� �������� ��������')
    N= NaN;
end