IsDiagDom = @(A)all( 2*abs(diag(A))>sum(abs(A),2));

% ��������� ������� ������������� ������������
if ~IsDiagDom( A )
    MakeDiagDom(A)
end