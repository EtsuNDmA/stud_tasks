clc
clear all

A = [1.7  -2.2   3.0;
       2.1   1.9  -2.3;
       4.2   3.9  -3.1];
b = [1.8; 2.8; 5.1];

% ��������� ������� ������������� ������������
IsDiagDom = @(A)all( 2*abs(diag(A))>sum(abs(A),2));
IsDiagDom(A)

% ����������� ������� �
C = [ 1     1     0;
        1     3    -2;
        3     0    -1];
   
B = C*A;   
d = C*b;
      
IsDiagDom(B)

Bnorm1 = max(sum(abs(B)))
BnormInf = max(sum(abs(B')))

% ������� 
% Bx=d
% ������������� � �������������� ����
% x=alpha*x+beta

for i=1:3
    alpha(i,1:3) = B(i,1:3)/B(i,i);
    beta(i,1) = d(i)/B(i,i);
end

alpha = eye(3)-alpha;

betanorm = sum(abs(beta));
alphanorm = max(sum(abs(alpha)));

e = 0.1;

k_apriori = (log(e)-log(betanorm)+log(1-alphanorm))/log(alphanorm)-1;

% �������� ��������� �����������
x(1:3,1) = beta;

for k=2:k_apriori
    x(:,k) = alpha*x(:,k-1)+beta;
    if sum(abs(x(:,k)-x(:,k-1)))<=e*(1-alphanorm)/alphanorm
        fprintf('������� ������� [%f; %f; %f]\n',x(:,end))
        fprintf('����������� ����� �������� %d\n', k-1)
        break
    end
end

% ������ �������
f=A*x(:,end)-b
sum(abs(f))





