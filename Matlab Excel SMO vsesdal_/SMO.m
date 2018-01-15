state_queue=0;
state_main='empty';
n=1;
%Plan 1 event
mes_id=1;
mes_gen_time=random('unif',9-4,9+4);
event_list(1).time=mes_gen_time;
event_list(1).event_id='new_mes_in_que';
while t(n)<100
    t(n)=event_list(n).time;
    
    [state_queue, state_main] = next_event_processing(...
        event_list.event_id(n), state_queue, state_main);
    %Plan new event
    
    

    n=n+1;
end