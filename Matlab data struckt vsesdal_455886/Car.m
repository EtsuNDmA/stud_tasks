classdef Car < handle
% Реализация класса Car для Хранения параметров автомобилей    
    properties
        id
        make
        model
        year
        transmission
        engine
        drive_type
        color
    end
    
    methods
        function obj = Car(id)
        % Конструктор    
           obj.id = id;
        end
        
        function addfield(obj,varargin)
        % Добавление полей    
            nVarargin = nargin-1;
            if ~nVarargin || rem(nVarargin,2)~=0
                error('Not enough input arguments.')
            end
            i=1;
            while i<=nVarargin
                obj.(varargin{i}) = varargin{i+1};
                i = i+2;
            end
            
        end
        
        function delfield(obj,varargin)
        % Очистка полей    
            nVarargin = nargin-1;
            if ~nVarargin
                error('Not enough input arguments.')
            end
            i=1;
            while i<=nVarargin
                obj.(varargin{i}) = [];
                i = i+1;
            end
        end
    end
end

