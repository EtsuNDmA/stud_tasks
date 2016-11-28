IsDiagDom = @(A)all( 2*abs(diag(A))>sum(abs(A),2));

% ѕровер€ем условие диагонального преобладани€
if ~IsDiagDom( A )
    MakeDiagDom(A)
end