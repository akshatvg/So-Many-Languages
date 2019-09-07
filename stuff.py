import c2p

c_code ='''
#include<iostream>
#include<conio.h>
void main()
{
int n,a,b,answer;
cin>>n;
cin>>a;
cin>>b;
for (int x = 2; x<n; x+2)
{
answer=(a+b)/x;
cout<<answer;
}
getch()
}'''

py_list = c2p.convert(c_code)
pycode=''
for i in py_list:
    print(i,end='')
    pycode+=i
#print(pycode)
