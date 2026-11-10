clc
clear
x = [0:0.2:1];
y = f(x);
subplot(5,2,1)
plot(x,y,'*');
grid on
for i=2:5
p=polyfit(x,y,i)
y1=polyval(p,x);
subplot(5,2,(i-1)*2+1)
plot(x,y1)
grid on
subplot(5,2,(i-1)*2+2)
plot(x,y,x,y1)
grid on
end