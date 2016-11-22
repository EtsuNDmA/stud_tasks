classdef FIFOQueue < handle
    
    properties(Access=private, Constant=true)
        REFLENGTH = 1000;
    end
    
    properties
        head
        tail
        count
        element
    end
    
    methods
        function obj = FIFOQueue()
        % Конструктор очереди
            obj.element = cell(1,obj.REFLENGTH);
            obj.head = 1;
            obj.tail = 1;
            obj.count = 0;
        end
        
        function enqueue(obj, elem)
        % Вставка элемента в хвост очереди
        
           % Увеличиваем контейнер при заполнении
           if obj.tail == length(obj.element)
               obj.element=[obj.element,cell(1,obj.REFLENGTH)];
           end
           obj.element{obj.tail} = elem;
           obj.tail = obj.tail+1;
           obj.count = obj.count+1;
        end
        
        function elem = dequeue(obj)
        % Получение элемента из головы очереди
        
            % Уменьшаем контейнер при head > REFLENGTH
            if obj.head > obj.REFLENGTH
               obj.element=obj.element(REFLENGTH+1:end);
               obj.head = 1;
               obj.tail = obj.tail-obj.REFLENGTH;
            end
            if obj.count == 0
                error('Queue is empty.')
            end
            elem = obj.element{obj.head};
            obj.head = obj.head+1;
            obj.count = obj.count-1;
        end
        
        function result=isempty(obj)
        % Проверка очереди на пустоту
            result = obj.count==0;
        end
        
        function cnt = get_count(obj)
        % Возвращает количество элементов в очереди
            cnt = obj.count;
        end
    end
 
end

