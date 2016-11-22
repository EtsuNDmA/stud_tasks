function [ state_queue, state_main ] = next_event_processing( event_id, state_queue, state_main)
    switch event_id
        case 'new_mes_in_que'
            if strcmp(state_main,'busy')
                state_queue=state_queue+1;
            else
                state_main='busy';
            end;
            
        case 'mes_done'
            fprint('Mesage Done\n')
            if state_queue>0
                state_queue=state_queue-1;
                state_main='busy';
            else
                state_main='empty';
            end
    end
end

