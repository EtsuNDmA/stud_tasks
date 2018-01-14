Str_F = 'Remizova';
Str_I = 'Ludmila';
Str_O = 'Sergeevna';

Str_Fv = upper(Str_F);
Str_V = strvcat(Str_Fv, Str_I, Str_O);
Str_H = strcat(Str_F(1), Str_I(1), Str_O(1));
Cod_F1 = double(Str_F);
Cod_F2 = length(Str_I);
Cod_F3 = char(Cod_F1+Cod_F2);
