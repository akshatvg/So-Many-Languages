import re
def convert(cpp):
    numbers=['1','2','3','4','5','6','7','8','9','0']
    def ser(st,el): #returns el val
        for i in range(len(st)):
            if st[i] == el:
                return i

    def fe(st):
        ret_list=[]
        ml=''
        for i in st:
            if i !=' ':
                ml+=i
        st=ml
        elvar=ser(st,'=')
        elvar-=1
        it_var = st[elvar] #the variable
        st_ind = elvar+2
        start = st[elvar+2] #start of loop
        for x in range(st_ind+1,st_ind+3):
            if st[x] in numbers:
                start+=st[x]
            else:
                break

        inc = x-st_ind-1
        #print(inc)
        stop = st[elvar+6+inc] #end of loop
        stop_ind = 0
        for u in range(7+inc,9+inc):
            if st[elvar+u] in numbers:
                stop+=st[elvar+u]
                stop_ind+=1
            else:
                break
        it = st[elvar+10+inc+stop_ind] #to check iteration value
        ret_list = [it_var,start,stop,it]
        return ret_list

    def we(st):
        ne=''
        for i in st:
            if i == '(' or i == ')':
                i = ' '
                ne+=i
            else:
                ne+=i
        ne+=':'
        #print(ne)
        return ne

    def ie(st):
        ne=''
        for i in st:
            if i == '(' or i == ')':
                i = ' '
                ne+=i
            else:
                ne+=i
        ne+=':'
        #print(ne)
        return ne
            
        
        
    '''cpp =
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
    for (int j=0;j<12;j+5)
    {
    cout<<j;
    }
    while(x<23)
    {
    cout<<x;
    x++;
    }
    if(x==2)
    {
    cout<<x;
    }
    else if(x>2)
    {
    cout<<x+2;
    }
    getch()
    }
    '''

    #print(cpp)
    sl=[]
    fl=[]
    for i in cpp:
        app=''
        if i!='':
            app+=i
        else:
            app=''
        sl.append(app)
    app=''
    for i in sl:
        if i != '\n':
            app+=i
        else:
            fl.append(app)
            app=''
    #print(fl)
    sl=[]
    for i in fl:
        if '#' not in i and 'void' not in i and 'main()' not in i and 'int' not in i:
            sl.append(i)
        elif 'for' in i:
            sl.append(i)
    #print('EXTRACTED CPP CODE:\n',sl)

    py_code = []

    for i in sl:
        if 'cin>>' in i:
            x = ser(i,'>')
            x+=2
            var = i[x:len(i)-1:]
            ctp = var+'= input()\n'
            py_code.append(ctp)
            ctp=''
        elif 'cout<<' in i:
            x = ser(i,'<')
            x+=2
            var = i[x:len(i)-1:]
            ctp = 'print('+var+')\n'
            py_code.append(ctp)
            ctp=''

        elif '//' in i:
            tp = '#'+i[2::]+'\n'
            py_code.append(tp)



        elif 'for' in i:
            for_els = fe(i)
            if for_els[1] < for_els[2]:
                if for_els[3]=='+':
                    ctp = 'for '+for_els[0]+' in range('+for_els[1]+','+for_els[2]+',1):\n'
                    py_code.append(ctp)
                else:
                    ctp = 'for '+for_els[0]+' in range('+for_els[1]+','+for_els[2]+','+for_els[3]+'):\n'
                    py_code.append(ctp)
            elif for_els[1] > for_els[2]:
                if for_els[3]=='-':
                    ctp = 'for '+for_els[0]+' in range('+for_els[1]+','+for_els[2]+',-1):\n'
                    py_code.append(ctp)
                else:
                    ctp = 'for '+for_els[0]+' in range('+for_els[1]+','+for_els[2]+',-'+for_els[3]+'):\n'
                    py_code.append(ctp)
                    
            
            ctp=''

        elif 'while' in i:
            ctp = we(i)+'\n'
            py_code.append(ctp)

        elif ('if' in i or 'else' in i) and 'else if' not in i:
            ctp = ie(i)+'\n'
            #print(123)
            py_code.append(ctp)

        elif 'else if' in i:
            ind = ser(i,'f')
            #print('i reached here')
            new_str = 'elif'+i[ind+1::]
            ctp = ie(new_str)+'\n'
            py_code.append(ctp)
            
        
        elif '++' in i:
            ctp= i[0]+'+=1\n'
            py_code.append(ctp)
        elif '--' in i:
            ctp= i[0]+'-=1\n'
            py_code.append(ctp)

            
        elif 'getch()' in i or '{' in i:
            u=1
            
        else:
            if '}' in i:
                py_code.append(i)
            else:
                ctp=i[0:len(i)-1:]+'\n'
                py_code.append(ctp)
        
    #py_code.remove('\n')
    print('PYTHON CODE EXTRACTS:\n', py_code)
    #print('\n\nFINAL CODE:')
    al=[]
    fl=[]
    for i in range(len(py_code)):
        if 'for' in py_code[i]:
            c=0
            while py_code[i+c] != '}':
                if 'for' not in py_code[i+c]:
                    #print('    '+py_code[i+c],end='')
                    al.append(py_code[i+c])
                    fl.append('    '+py_code[i+c])
                else:
                    #print(py_code[i+c],end='')
                    al.append(py_code[i+c])
                    fl.append(py_code[i+c])
                c+=1
        elif 'while' in py_code[i]:
            c=0
            while py_code[i+c] != '}':
                if 'while' not in py_code[i+c]:
                    #print('    '+py_code[i+c],end='')
                    al.append(py_code[i+c])
                    fl.append('    '+py_code[i+c])
                else:              
                    #print(py_code[i+c],end='')
                    al.append(py_code[i+c])
                    fl.append(py_code[i+c])
                c+=1
        elif 'if' in py_code[i] or 'else' in py_code[i] or 'elif' in py_code[i]:
            c=0
            while py_code[i+c] != '}':
                if 'if' not in py_code[i+c]:
                    #print('    '+py_code[i+c],end='')
                    al.append(py_code[i+c])
                    fl.append('    '+py_code[i+c])
                else:              
                    #print(py_code[i+c],end='')
                    al.append(py_code[i+c])
                    fl.append(py_code[i+c])
                c+=1
        elif py_code[i]!='}' and py_code[i] not in al:
            #print(py_code[i],end='')
            fl.append(py_code[i])
    #print(fl)
    return fl
            



