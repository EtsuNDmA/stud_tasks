function addtail(queue, varargin)
% Добавление нескольких элементов в конец очереди
    nVarargin = nargin-1;
    if ~nVarargin
        error('Not enough input arguments.')
    end
    for i=1:nVarargin
       queue.enqueue(varargin{i}) 
    end
    %fprintf('Количество добавленных элементов = %d \n',nVarargin)

