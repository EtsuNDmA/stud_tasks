function f=plotsys(N_zv,param,verbose)
% N_zv - Номер звена
% param - Массив ячеейк параметров 
%             например {[1 2 3],[3 4 5]}
%verbose - строка, добавляемая к названию графика
%              

    for i=1:length(param)
        % Получаем передаточную функцию
        W{i} = TF_zv(N_zv,param{i});
        
        %Построение требуемых характеристик
        %ЛАЧХ и ЛФЧХ 
        if i==1
            f_bode=ltiview({'bode'},W{i});
            
        else
            figure(f_bode)
            ltiview( 'current',W{i},f_bode);
        end
        
        %АФХ 
        if i==1
            f_nyq=ltiview({'nyquist'},W{i});
        else
            figure(f_nyq)
            ltiview( 'current',W{i},f_nyq);
        end
        
        %весовая функция w(t) 
        if i==1
            f_imp=ltiview({'impulse'},W{i});
        else
            figure(f_imp)
            ltiview( 'current',W{i},f_imp);
        end
        %переходная функция h(t)
        if i==1
            f_step=ltiview({'step'},W{i});
        else
            figure(f_step)
            ltiview( 'current',W{i},f_step);
        end
    end
    
    % Включим сетку, название и сохраним в файл
    hAxes = findobj(f_bode,'type','axes');
    ax=hAxes(2);
    title(ax,['ЛАЧХ и ЛФЧХ, для разных ',verbose]);
    grid(ax,'on');
    
    fname = [pwd, '\img\', regexprep(['bode ',verbose],'[\\]',''),' ',num2str(N_zv),'.png'];
    set(f_bode,'PaperPositionMode','auto')
    saveas(f_bode,fname)
    
    
    hAxes = findobj(f_nyq,'type','axes');
    title(hAxes(2),['АФХ ,для разных ',verbose]);
    grid(hAxes(2),'on');
    
    fname = [pwd, '\img\', regexprep(['nyq ',verbose],'[\\]',''),' ',num2str(N_zv),'.png'];
    set(f_nyq,'PaperPositionMode','auto')
    saveas(f_nyq,fname)
    
    
    hAxes = findobj(f_imp,'type','axes');
    title(hAxes(2),['Весовая функция w(t), для разных ',verbose]);
    grid(hAxes(2),'on');
    
    fname = [pwd, '\img\', regexprep(['imp ',verbose],'[\\]',''),' ',num2str(N_zv),'.png'];
    set(f_imp,'PaperPositionMode','auto')
    saveas(f_imp,fname)
    
    
    hAxes = findobj(f_step,'type','axes');
    title(hAxes(2),['Переходная функция h(t), для разных ',verbose]);
    grid(hAxes(2),'on');
    
    fname = [pwd, '\img\', regexprep(['step ',verbose],'[\\]',''),' ',num2str(N_zv),'.png'];
    set(f_step,'PaperPositionMode','auto')
    saveas(f_step,fname)
    
    fprintf(['Fileses saved to ', regexprep(pwd,'[\\]','\\\'),'\\img\\\n'])
    
    
