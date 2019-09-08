import re


def convert(py):


    numbers=['1','2','3','4','5','6','7','8','9','0']
    
    def ser(std,el): #returns el val
        for x in range(len(std)):
            if std[x] == el:
                return x

    def Convert(string): 
        li = list(string.split(" ")) 
        return li 


    
    #preperations
    sl=[]
    fl=[]
    for i in py:
        
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
            if app != '':
                fl.append(app)
            app=''
    sl=[]
    for i in fl:
        if i == '':
            ##print('i reached here')
            fl.remove(i)
        
        if 'import' in i :
           sandy = "gey"
        else:
            sl.append(i)
    #print('extracted py code',sl) 
    php_code = []
    f=1
    for i in sl:
        ##print(i)
        if i[:3] == "   ":
            f=0
        if i[:3] != "   " and f==0:
            php_code.append("}")
        
        #

        if i is not None:
            r1 = re.findall(r"print\(.*?\)",i)
            if r1:
                stri=''
                for i in r1:
                    stri+=i
                r2 = re.findall(r"\(.*?\)",stri)
                if r2 is not None:
                    stri=''
                    for j in r2:
                        j = j[1:-1]
                        stri+=j
                        if j[0]=="'" or j[0]=='"':
                            code = "echo " + j + ';'
                            php_code.append(code)
                        else:
                            code = "echo $" + j.strip() + ';'
                            php_code.append(code)
                        
                        for l in j:
                            if l == ",":
                                php_code.pop()
                                j= "echo " + j[:j.index(l)+1]+" $" + j[j.index(l)+2:] + " ;"
                                #j= j[:j.index(l)+3]+  j[j.index(l)+4:] + " ;"
                                php_code.append(j)
    #equations
        ##print(i)
        if "=" in i or "-" in i or "+" in i or "*" in i or "/" in i:
            if "input" in i:
                i=i.replace("input","fgets(STDIN);")
                i=i[:i.index(";")+1]
                #php_code.append(i)
            '''elif "$input" in i:
                i=i.replace("$input","fgets(STDIN);"+1)
                i=i[:i.index(";")]'''
                #php_code.append(j)
            ##print("yesss")
            u=''
            for x in i:
                if x!= ' ':
                    u+=x
                else:
                    b=1
            
            #print(i)
            ##print(u)
            i=i.strip()
            lister = Convert(i)
            
            ##print(lister)
            r_el=[]
            for k in lister:
                stri=''
                res = re.findall(r"[A-Za-z]*",k)
                #print(lister)
                if res and 'fgets(STDIN);' not in lister:
                    for k in res:
                        if k != '' and k !=" ":
                            r_el.append(k)
            n=0
            num=0
            for m in r_el:
                num = u.find(m,n)
                #print(num)
                u = u[:num]+"$"+u[num:]
                n+=1
                #print(u)
            php_code.append(u)
            
            
                

               # var = l.index(k)
                #l=l[var:]

                ##print(l,var)

                        

                        ##print(stri)
                        #for j in r1 :
                        #   #print(j)

                #php_code.append(i)

        if i is not None:
            r1 = re.findall(r"for\ .*?in range\(.*?\)",i)
            if r1:
                stri=''
                variable=''
                range=''
                lis=[]
                for j in r1:
                    stri+=j
                    ##print(j)
                lis = Convert(stri)
                ##print(lis)
                for m in lis:
                    if m == "for":
                        variable = lis[lis.index(m)+1]
                range = lis[-1]
                range = range.split("(")
                range = range[1].split(")")[0]
                range = range.split(',')
                ##print("for ("+"$"+variable+"; $"+variable+"<="+range[1]+"; $"+variable+"+="+range[2])
                #print(variable,range)
                if len(range) == 3: 
                    for_loop = "for ("+"$"+variable+";"+ range[0] +"<= $"+variable+"<="+range[1]+"; $"+variable+"+="+range[2]+"){"
                elif len(range)==2:
                    for_loop = "for ("+"$"+variable+";"+range[0]+" $"+variable+"<="+range[1]+" {"
                elif len(range)==1:
                    for_loop = "for ("+"$"+variable+"; $"+variable+"<="+range[0]+" {"
                php_code.append(for_loop)
                
        
        if i is not None:
            r1 = re.findall(r"while.*?\:",i)
            if r1:
                stri=''
                lis=[]
                for j in r1:
                    stri+=j
                stri = stri.replace(")",'')
                stri = stri.replace("(",'')

                lis = Convert(stri)
                #print(lis)
                for m in lis:
                    if m == "while":
                        variable = lis[lis.index(m)+1]
                        ranger = lis[lis.index(m)+2 :] 
                ranger_string = ''
                for i in ranger:
                    ranger_string += i
                
                string ="while ( $"+variable + ranger_string +") {" 
                string = string.replace(":",'')
                php_code.append(string)


                
                




                                
                             

    
    #print(php_code)
    ph_c = '<?php\n'
    for i in php_code:
        ph_c+=i+'\n'
    ph_c+='?>'
    ph_c = ph_c.replace('$fgets','fgets')
    #print(ph_c)
    return ph_c



if __name__ == '__main__':
    py ='''
    import manboobs
    n= input()
    a= input()
    b= input()



    for x in range(2,n,2):
        answer= ( y + z ) / x
    while i < 6:
        i+=1
    print("Tewari", akshat)'''

    x = convert(py)
    print(x)