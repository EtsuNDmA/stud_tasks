classdef FIFOQueue < handle
    
    properties
        head
        tail
        count
        element
    end
    
    methods
        function obj = FIFOQueue()
            obj.element = zeros(1,2);
            obj.head = 1;
            obj.tail = 1;
            obj.count = 0;
        end
        
        function enqueue(obj, elem)
           if obj.tail==obj.element(end)
               obj.element=[obj.element,zeros(1,length(obj.element)*2)];
               fprintf('Увеличиваем контейнер при q.element длиной %d\n',length(obj.element))
           end
           obj.element(obj.tail) = elem;
           obj.tail = obj.tail+1;
           obj.count = obj.count+1;
        end
        
        function elem = dequeue(obj)
            % Get element
            if obj.count == 0
                error('Queue is empty')
            end
            elem = obj.element(obj.head);
            obj.head = obj.head+1;
            obj.count = obj.count-1;
        end
        
        function result=isempty(obj)
            result = obj.count==0;
        end
    end
    
end

