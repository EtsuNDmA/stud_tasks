function addtail(queue, varargin)
% ���������� ���������� ��������� � ����� �������
    nVarargin = nargin-1;
    if ~nVarargin
        error('Not enough input arguments.')
    end
    for i=1:nVarargin
       queue.enqueue(varargin{i}) 
    end
    %fprintf('���������� ����������� ��������� = %d \n',nVarargin)

