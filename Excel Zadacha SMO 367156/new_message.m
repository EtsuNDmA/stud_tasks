function [ mes_id,mes_gen_time ] = new_message( mes_id_list,last_mes_gen_time )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
mes_id=max(mes_id_list)+1;
mes_gen_time=last_mes_gen_time+random('unif',9-4,9+4)
end

