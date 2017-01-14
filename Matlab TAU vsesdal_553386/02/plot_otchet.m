close all
% Инерционное звено
W1=TF_zv(1,[10,20]);
% АФХ
nyquist(W1);
hold on
plot([0 5], [0 -5],...
    '-ok',...
    'MarkerSize',10,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g')
plot([10], [0],...
    '-ok',...
    'MarkerSize',10,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g')


text(-1.5,0.5,'\omega=\infty','FontSize',18)
text(8.5,0.5,'\omega=0','FontSize',18)
text(4.5,-4.5,'\omega=1/T','FontSize',18)

polar([0 0 -pi/10 -pi/8 -pi/6 -pi/4], [0 2 2 2 2 2],'k')
text(2, -1,'\psi=\pi/4','FontSize',18)

title('АФХ','FontSize',22)
axis equal
xlabel('Re(|W|)','FontSize',18)
ylabel('Im(|W|)','FontSize',18)

% Весовая
figure
impulse(W1)
hold on
plot([0], [0.5],...
    '-ok',...
    'MarkerSize',10,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g')
text(2, 0.5, 'k/T','FontSize',18)
plot([0 120], [0 0],...
    '--k',...
    'LineWidth',2)
ylim([-0.1 0.6])


grid on
title('Весовая функция','FontSize',22)
ylabel('w(t)','FontSize',18)
xlabel('t','FontSize',18)

% Переходная
figure
step(W1)
hold on
plot([0 120], [10 10],...
    '--k',...
    'LineWidth',2)

annotation('doublearrow',[0.6 0.6],[0.12 0.75])
text(75, 5, 'k','FontSize',18)

plot([0 20], [0 10],...
    '--ok',...
    'LineWidth',2,...
    'MarkerSize',10,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g')

annotation('doublearrow',[0.15 0.278],[0.8 0.8])
text(8, 11.1, 'T','FontSize',18)

ylim([-0.1 12])
xlim([-0.1 120])
grid on
title('Переходная функция','FontSize',22)
ylabel('h(t)','FontSize',18)
xlabel('t','FontSize',18)

%ЛФЧХ
figure
plot([-5 log10(1/20) 5], [1 1 -2],'LineWidth',2)
annotation('doublearrow',[0.2 0.2],[0.52 0.7])
text(-3.9,0.5,'20 log_{10} k','FontSize',18)

hold on
grid on
set(gca,'xticklabel',[])
set(gca,'yticklabel',[])
plot([0 0],[-20 6],'-k')
plot([log10(1/20) log10(1/20)],[-2 2],'--k','LineWidth',2)
text(log10(1/20)-0.2,-2.1,'1/T','FontSize',18)
omega=logspace(-5,10,100);
plot(log10(omega),atan(-20*omega),'r','LineWidth',2)

plot([-5 10], [0 0], '--k','LineWidth',2)
text(-4.8,-0.2,'0','FontSize',18)
plot([-5 10], [-pi/2 -pi/2], '--k','LineWidth',2)
text(-4.8,-pi/2-0.2,'-\pi/2','FontSize',18)
plot([-5 10], [-pi/4 -pi/4], '--k','LineWidth',2)
text(-4.8,-pi/4-0.2,'-\pi/4','FontSize',18)

text(0,0.5,'-20 дБ/дек','FontSize',18)

ylim([-2.3 2.3])
xlim([-5 5])
title('ЛАФЧХ','FontSize',22)
ylabel('L(\omega), \psi(\omega)','FontSize',18)
xlabel('log_{10}(\omega), дек','FontSize',18)
%%
% Колебательное звено
W2=TF_zv(2,[1,0.5,0.5]);
% АФХ
figure
nyquist(W2);
hold on

plot(1, 0,...
    'o',...
    'MarkerSize',10,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g')
text(-0.5,0.1,'\omega=\infty','FontSize',18)

plot(0, 0,...
    'o',...
    'MarkerSize',10,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g')
text(1.1,-0.1,'\omega=0','FontSize',18)

plot(0, -1,...
    'o',...
    'MarkerSize',10,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g')
text(0.1,-1.1,'-k/(2\xi), \omega=1/T','FontSize',18)


% text(-1.5,0.5,'\omega=\infty','FontSize',18)
% text(8.5,0.5,'\omega=0','FontSize',18)
% text(4.5,-4.5,'\omega=1/T','FontSize',18)
% 
% polar([0 0 -pi/10 -pi/8 -pi/6 -pi/4], [0 2 2 2 2 2],'k')
% text(2, -1,'\psi=\pi/4','FontSize',18)
% 
title('АФХ','FontSize',22)
axis equal
xlabel('Re(|W|)','FontSize',18)
ylabel('Im(|W|)','FontSize',18)

set(gca,'xticklabel',[])
set(gca,'yticklabel',[])
ylim([-1.5 0.5])



%ЛФЧХ
figure
plot([-5 log10(1/20) 5], [1 1 -2],'LineWidth',2)
annotation('doublearrow',[0.2 0.2],[0.52 0.7])
text(-3.9,0.5,'20 log_{10} k','FontSize',18)

hold on
grid on
set(gca,'xticklabel',[])
set(gca,'yticklabel',[])
plot([0 0],[-20 6],'-k')
plot([log10(1/20) log10(1/20)],[-2 2],'--k','LineWidth',2)
text(log10(1/20)-0.2,-2.1,'1/T','FontSize',18)
omega=logspace(-5,10,100);
y=-2*0.5*0.5.*omega./((1-0.5.^2*omega.^2).^2+(2*0.5*0.5.*omega).^2);
x= -(1-0.5^2*omega.^2)./((1-0.5.^2*omega.^2).^2+(2*0.5*0.5.*omega).^2);
plot(log10(omega),atan2(y,x),'r','LineWidth',2)

plot([-5 10], [0 0], '--k','LineWidth',2)
text(-4.8,-0.2,'0','FontSize',18)
plot([-5 10], [-pi/2 -pi/2], '--k','LineWidth',2)
text(-4.8,-pi/2-0.2,'-\pi/2','FontSize',18)
plot([-5 10], [-pi/4 -pi/4], '--k','LineWidth',2)
text(-4.8,-pi/4-0.2,'-\pi/4','FontSize',18)

text(0,0.5,'-20 дБ/дек','FontSize',18)

ylim([-2.3 2.3])
xlim([-5 5])
title('ЛАФЧХ','FontSize',22)
ylabel('L(\omega), \psi(\omega)','FontSize',18)
xlabel('log_{10}(\omega), дек','FontSize',18)


%%
close all
% Неустойч звено
W1=TF_zv(3,[10,20]);
% АФХ
nyquist(W1);
hold on
plot([0 -5], [0 -5],...
    '-ok',...
    'MarkerSize',10,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g')
plot([-10], [0],...
    '-ok',...
    'MarkerSize',10,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g')


text(-1.5,0.5,'\omega=\infty','FontSize',18)
text(-8.5,0.5,'\omega=0','FontSize',18)
text(-4.5,-4.5,'\omega=1/T','FontSize',18)

polar([0 -pi -pi+pi/10 -pi+pi/8 -pi+pi/6 -pi+pi/4], [0 2 2 2 2 2],'k')
text(-2, -1,'\pi/4','FontSize',18)

title('АФХ','FontSize',22)
axis equal
xlabel('Re(|W|)','FontSize',18)
ylabel('Im(|W|)','FontSize',18)

% Весовая
figure
impulse(W1)
hold on

plot(0, 0.5,...
    '-ok',...
    'MarkerSize',10,...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor','g')
text(0.1, 0.8,'k/T','FontSize',18)

ylim([-0.1 5])
xlim([-0.1 30])

grid on
title('Весовая функция','FontSize',22)
ylabel('w(t)','FontSize',18)
xlabel('t','FontSize',18)

% Переходная
figure
step(W1)
hold on

ylim([-0.1 30])
xlim([-0.1 30])
grid on
title('Переходная функция','FontSize',22)
ylabel('h(t)','FontSize',18)
xlabel('t','FontSize',18)

%ЛФЧХ
figure
plot([-5 log10(1/20) 5], [1 1 -2],'LineWidth',2)
annotation('doublearrow',[0.2 0.2],[0.64 0.74])
text(-3.9,0.5,'20 log_{10} k','FontSize',18)

hold on
grid on
set(gca,'xticklabel',[])
set(gca,'yticklabel',[])
plot([0 0],[-20 6],'-k')
plot([log10(1/20) log10(1/20)],[-4 2],'--k','LineWidth',2)
text(log10(1/20)-0.2,-4.1,'1/T','FontSize',18)
omega=logspace(-5,10,100);
plot(log10(omega),-pi+atan(20*omega),'r','LineWidth',2)

plot([-5 10], [0 0], '--k','LineWidth',2)
text(-4.8,-0.2,'0','FontSize',18)
plot([-5 10], [-pi/2 -pi/2], '--k','LineWidth',2)
text(-4.8,-pi/2-0.2,'-\pi/2','FontSize',18)
plot([-5 10], [-pi -pi], '--k','LineWidth',2)
text(-4.8,-pi-0.2,'-\pi','FontSize',18)
plot([-5 10], [-0.75*pi -0.75*pi], '--k','LineWidth',2)
text(-4.8,-0.75*pi-0.2,'-3\pi/4','FontSize',18)

text(0,0.5,'-20 дБ/дек','FontSize',18)

ylim([-5 2.5])
xlim([-5 5])
title('ЛАФЧХ','FontSize',22)
ylabel('L(\omega), \psi(\omega)','FontSize',18)
xlabel('log_{10}(\omega), дек','FontSize',18)


