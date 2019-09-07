from flask import Flask, flash, redirect, render_template, url_for, request, make_response
from flask_cors import CORS
import ibm_watson
import re
import webbrowser
import requests,json
import urllib
import os
import c2p
import time



app = Flask(__name__)
CORS(app)

def transform(text_file_contents):
    return text_file_contents.replace("=", "=")


@app.route('/')
def form():
    return render_template('convert.html')
    #return render_template('gfile.html')

@app.route('/transform', methods=['POST','GET'])
def transform_view():
    request_file = request.files['data_file']
    if not request_file:
        return "No file"

    file_contents = request_file.stream.read().decode("utf-8")

    result = transform(file_contents)

    print(result)
    py_list = c2p.convert(result)
    pycode=''
    for i in py_list:
        print(i,end='')
        pycode+=i
    #print(pycode)
    response = make_response(pycode)
    response.headers["Content-Disposition"] = "attachment; filename=converted_py_code.py"
    return response

@app.route('/box', methods=['POST','GET'])
def box():
    if request.method == 'POST':
        resp_json = request.get_json()
        to_convert = resp_json['text']

        py_list = c2p.convert(to_convert)
        pycode=''
        for i in py_list:
            print(i,end='')
            pycode+=i
        time.sleep(2)
        return json.dumps({"response": pycode}), 200


@app.route('/practice')
def practice():
    global intent 
    intent=[]
    return render_template('compiler.html')

@app.route('/shop')
def shop():
    global intent 
    intent=[]
    return render_template('shop.html')

@app.route('/print/name', methods=['POST', 'GET'])

def get_names():

    global c
    global intent
    c=1
    if request.method == 'POST':
        resp_json = request.get_json()
        command = resp_json['text']
        if command=='cplusplus':
            command='open c++'
    assistant = ibm_watson.AssistantV1(
    version='2019-02-28',
    iam_apikey='u1N9ThXmpZUk_-1_F1AaAw-11BbBXFtCbonmmerHbnFI',
    url='https://gateway-wdc.watsonplatform.net/assistant/api'
    )

    response = assistant.message(
        workspace_id='7cb1c0fc-6e91-4b63-9e93-8a30028bd58e',
        input={
            'text': command #use the <text> we get with flask
        }
    ).get_result()


    a=response
    b=a['intents']
    if b==[]:
        if c==1:
            
            intent.append('nothing')
        else:
            intent.append('nothing')
    else:
        if c==1:
            
            intent.append(b[0]['intent'])
        else:
            intent.append(b[0]['intent'])
    print('user said:', command)
    print(intent)
    
    while intent[0]=='python':
        
        if intent[-1]=='for_loop':
            to_send = """for x in range (a,b):
    #enter your code here"""
        elif intent[-1]=='nested_for':
            to_send = """for x in range(a,b):
    for y in range(a,b):
        #enter your code here"""
        elif intent[-1]=='if_condition':
            to_send = """if a==b:
    #enter your code here"""

        elif intent[-1]=='nested_if':
            to_send = """if a==b:
    if a==b:
        #enter your code here
    else:
        #enter your code here"""

        elif intent[-1]=='else_if':
            to_send = """if a>=b:
    #enter your code here
elif a==b:
    #enter your code here"""

        elif intent[-1]=='else_condition':
            to_send = """elif a &gt;= b:
    #enter your code here
else:
    #enter your code here"""

        elif intent[-1]=='while_loop':
            to_send = """while x == y:
    #enter your code here"""

        elif intent[-1]=='do_while_loop':
            to_send="""a = 1
while True: #acts a the 'do' part.
    print(a)
    a+=3
    if(a > 10):
        break
#Python doesn't have a do-while loop. Hence emulating it with boolean."""

        elif intent[-1]=='print':
            to_send = """print(#your variable or string) """

        elif intent[-1]=='exit_loop':
            to_send ="""    if (condition):
    break"""
        
        elif intent[-1]=='init_string' or intent=='init_char':
            to_send="""var=input()"""

        elif intent[-1]=='init_int':
            to_send="""var=int(input())"""

        elif intent[-1]=='init_double':
            to_send="""var=double(input())"""

        elif intent[-1]=='arith_addition':
            to_send="""def add(a,b):
    return a+b
x=int(input())
y=int(input())
ans=add(x,y)
print(ans)"""

        elif intent[-1]=='arith_subtraction':
            to_send="""def sub(a,b):
    return a-b
x=int(input())
y=int(input())
ans=sub(x,y)
print(ans)"""

        elif intent[-1]=='arith_multiplication':
            to_send="""def multi(a,b):
    return a*b
x=int(input())
y=int(input())
ans=multi(x,y)
print(ans)"""

        elif intent[-1]=='arith_division':
            to_send="""def divi(a,b):
    return a/b
x=int(input())
y=int(input())
ans=divi(x,y)
print(ans)"""
        
        elif intent[-1]=='create_array':
            to_send="""var=[]
n=int(input())
for i in range(n):
    app=int(input())
    var.append(app)
print('the array is:',var)"""

        elif intent[-1]=='def_function':
            to_send="""def func_name(#arguments):
    #write your code here
    return #any variable
x=func_name(#arguments)"""

        elif intent[-1]=='cplus' or intent[-1]=='swift' or intent[-1]=='php':
            to_send= """Please Use the Change language option!"""

        elif intent[-1]=='python':
            to_send="""python running!"""
        
        elif intent[-1]=='recus':
            to_send="""def func(a):
    a+=1
    if a<=15:
        print(a)
        func(a) #recusion part.
    else:
        print('a exceeded the limit of 15!')
    return
func(9)"""

        elif intent[-1]=='switch_condition':
            to_send="""switch={
    1:'monday',
    2:'tuesday',
    3:'wednesday',
    4:'thursday',
    5:'friday',
    6:'saturday',
    7:'sunday'
    }
day=int(input())
print(switch[day])
#python does't have the concept of switch, hence this is achieved using dictionaries."""

        
        else:
            to_send="""I am sorry, i dont know what that means"""
            
        c+=1
        return json.dumps({"response": to_send}), 200
    
########################################################c++######################################################################################################################### 
    while intent[0]=='cplus':
        if intent[-1]=='for_loop':
            to_send = """for(int x=a ; x&lt;b ; x++) {
    //enter your code; 
}"""

        elif intent[-1]=='print':
            to_send = """cout << "Enter your string here!" << endl; """

        elif intent[-1]=='nested_for':
            to_send = """for(int x=a;x&lt;b;x++) {
for(int y=c;y&lt;d;y++) {
    //enter your code; 
}
}"""

        elif intent[-1]=='if_condition':
            to_send = """int x;
if(x==a) {
    //enter your code; 
}"""

        elif intent[-1]=='nested_if':
            to_send = """int x,y;
    if(x==a) {
    if(y==a) {
       //enter your code;  
    }
}"""

        elif intent[-1]=='else_if':
            to_send = """int x;
if(x==a) {
//enter your code; 
}
else if(x==b) {
//enter your code; 
}"""
                
        elif intent[-1]=='else_condition':
            to_send = """int x;
if(x==a) {
//enter your code;  
}
else {
//enter your code;  
}"""
                
        elif intent[-1]=='while_loop':
            to_send = """while(x!=a) {
//enter your code; 
}"""

        elif intent[-1]=='exit_loop':
            to_send = """break;"""

        elif intent[-1]=='do_while_loop':
            to_send = """int x;
do {
//enter your code;  
} while(x&lt;a);"""

        elif intent[-1]=='init_string':
            to_send = """string x;"""

        elif intent[-1]=='init_int':
            to_send = """int x;"""

        elif intent[-1]=='init_char':
            to_send = """char name[100];"""

        elif intent[-1]=='init_float':
            to_send = """float x;"""
 
        elif intent[-1]=='arith_addition':
            to_send = """#include &lt;iostream&gt; 
using namespace std;
int main() {
    int x,y,sum;
    cin>>x>>y;
    sum = x+y;
    cout<<"Sum is: "<< sum << endl;
return 0;
}"""

        elif intent[-1]=='arith_subtraction':
            to_send = """#include &lt;iostream&gt;
using namespace std;
int main() {
    int x,y,diff;
    cin>>x>>y;
    diff = x-y;
    cout<<"Difference is: "<< diff << endl;
return 0;
}"""

        elif intent[-1]=='arith_multiplication':
            to_send = """#include &lt;iostream&gt;
using namespace std;
int main() {
    int x,y,prod;
    cin>>x>>y;
    prod = x*y;
    cout<<"Product is: "<< prod << endl;
return 0;
}"""

        elif intent[-1]=='arith_division':
            to_send = """#include &lt;iostream&gt;
using namespace std;
int main() {
    int x,y,quo;
    cin>>x>>y;
    quo = x/y;
    cout<<"Quotient is: "<< quo << endl;
return 0;
}"""

        elif intent[-1]=='arith_remainder':
            to_send = """#include &lt;iostream&gt;
using namespace std;
int main() {
    int x,y,rem;
    rem = x%y;
    cout<<"Remainder is: "<< rem << endl;
return 0;
}"""

        elif intent[-1]=='def_function':
            to_send = """#include &lt;iostream&gt;
// function declaration
int func(int x, int y);
int main () {
    // local variable declaration
    int a,b;
    // calling a function.
    func(a,b);
return 0;
}
// function
int func(int x, int y) {
    //enter your code;
}"""

        elif intent[-1]=='create_class':
            to_send = """class base { 
// Access specifier 
public:  
// Data Members 
string name; 
// Member Functions() 
void printname() { 
    cout <<"Name is: "<<name; 
} 
};""" 

        elif intent[-1]=='create_object':
            to_send = """// Declare an object of class base 
base obj1;"""

        elif intent[-1]=='include_lib_basic':
            to_send = """#include &lt;iostream&gt;
#include &lt;conio.h&gt;
#include &lt;string.h&gt;
#include &lt;math.h&gt;
#include &lt;ctype.h&gt;
#include &lt;stdlib.h&gt;"""

        elif intent[-1]=='include_lib_adv':
            to_send = """#include <vector>
#include &lt;string&gt;
#include &lt;file&gt;
#include &lt;map&gt;
#include &lt;complex&gt;"""

        elif intent[-1]=='create_array':
            to_send = """int a[100] , x , b;
cout << "Enter array size:" << endl;
cin >> b;
cout << " Enter array elements: " << endl;
for (x=a ; x &lt; b ; x++) {
    cin >> a[x] ;
}
cout << "Array is: " << endl;
for(x=a ; x &lt; b ; x++) {
    cout << a[x] ;
}"""

        elif intent[-1]=='switch_condition':
            to_send = """char variable;
switch(variable) { 
case valueOne: 
//statements 
break; 
case valueTwo: 
//statements
break; 
default: //optional
//statements
}"""    
        elif intent[-1]=='swift' or intent[-1]=='python' or intent[-1]=='php':
            to_send= """Please Use the Change language option!"""

        elif intent[-1]=='cplus':
            to_send="""running c++"""
        
        else:
            to_send="""I am sorry, i dont know what that means"""

        c+=1
        return json.dumps({"response": to_send}), 200

########################################################PHP######################################################################################################################### 
    while intent[0]=='php':
        if intent[-1]=='for_loop':
            to_send = """for ($x = a; $x <= b; $x++) {
//enter your code
} """

        elif intent[-1]=='print':
            to_send = """ echo " Enter your string here ! " ; """

        elif intent[-1]=='nested_for':
            to_send = """for ($x = a; $x <= b; $x++) {
    for ($y = c; $y <= d; $y++) {
        //enter your code;
        }
}"""

        elif intent[-1]=='if_condition':
            to_send = """$t = "varable";
if ($t < "Condition") {
    //enter your code;
    }"""

        elif intent[-1]=='nested_if':
            to_send = """$x = "variable";
$y = "Variable"
if($x=="condition") {
    if($y=="condition") {
        //enter your code;
    }
}"""

        elif intent[-1]=='else_if':
            to_send = """$x = "variable";
if($x==a) {
    //enter your code;
}
else if($x==b) {
    //enter your code;
}
else if($x==c) {
    //enter your code;
}"""
                    
        elif intent[-1]=='else_condition':
            to_send = """$x = "Variable";
if($x==a) {
    //enter your code;
}
else {
    //enter your code;
}"""
                    
        elif intent[-1]=='while_loop':
            to_send = """while($x!="condition") {
    //enter your code;
}"""

        elif intent[-1]=='exit_loop':
            to_send = """break;"""

        elif intent[-1]=='do_while_loop':
            to_send = """$x = "variable";
do {
    //enter your code;
} while($x<"condition");"""

        elif intent[-1]=='init_string':
            to_send = """string $x; """

        elif intent[-1]=='init_int':
            to_send = """int $x; """

        elif intent[-1]=='init_char':
            to_send = """char name[100];"""

        elif intent[-1]=='init_float':
            to_send = """float $x; """

        elif intent[-1]=='arith_addition':
            to_send = """<?php
function add(float $x,float $y){
    return $x+$y;
}
?>"""

        elif intent[-1]=='arith_subtraction':
            to_send = """<?php
function add(float $x,float $y){
    return $x-$y;
}
?>"""

        elif intent[-1]=='arith_multiplication':
            to_send = """<?php
function add(float $x,float $y){
    return $a*$b;
}
?>"""

        elif intent[-1]=='arith_division':
            to_send = """<?php
function add(float $x,float $y){
    return $a/$b;
}
?>"""

        elif intent[-1]=='arith_remainder':
            to_send = """<?php
function add(float $x,float $y){
    return $a%$b;
}
?>"""

        elif intent[-1]=='def_function':
            to_send = """<?php
function add(float $x,float $y){
    //enter your code
    return "Your Output";
}
add($x,$y);
?>"""


        elif intent[-1]=='create_array':
            to_send = """int a[100],x,b;
echo 'Enter array size:';
$handle = fopen ("php://stdin","r");
$line = fgets($handle);
echo 'Enter array elements:';
for(x=a;x<b;x++) {
    a[x]=fgets($handle);
}
echo 'Array is: ' ;
for($x=a;$x<b;$x++) {
    echo $a[$x];
}"""

        elif intent[-1]=='switch_condition':
            to_send = """$x = "variable";
switch ($x) {
    case "1":
        //enter your code
        break;
    case "2":
        //enter your code
        break;
    case "3":
        //enter your code
        break;
    default: //optional
        //default return code;
}"""

        elif intent[-1]=='cplus' or intent[-1]=='python' or intent[-1]=='swift':
            to_send= """Please Use the Change language option!"""

        elif intent[-1]=='php':
            to_send="""running php"""
        
        else:
            to_send="""I am sorry, i dont know what that means"""

        c+=1
        return json.dumps({"response": to_send}), 200

    ######################################################## SWIFT ######################################################################################################################### 

    while intent[0]=='swift':
        if intent[-1]=='for_loop':
            to_send = """for i in a...b {
    //enter your code here
} """

        elif intent[-1]=='print':
            to_send = """ print(//enter your code) """

        elif intent[-1]=='nested_for':
            to_send = """for i in a...b {
    for j in a...b{
        //enter your code here
    }
}"""

        elif intent[-1]=='if_condition':
            to_send = """let a = 10
if a &lt; b {
	//enter your code
}
//print("This statement is always executed.")"""

        elif intent[-1]=='nested_if':
            to_send = """let a = 10
if a &gt; b {
	if a &gt; b {
	    //enter your code
    }
}
//print("This statement is always executed.")
"""

        elif intent[-1]=='else_if':
            to_send = """let a = 10
if a &gt; b {
	//enter your code
} else if a &gt; b {
	//enter your code
}
//print("This statement is always executed.")
"""
                    
        elif intent[-1]=='else_condition':
            to_send = """let a = 10
if a &gt; b {
    //enter your code
}
else {
    //enter your code
}"""
                    
        elif intent[-1]=='while_loop':
            to_send = """while a <= b {
    //enter your code 
}"""

        elif intent[-1]=='exit_loop':
            to_send = """if a &gt; b {
    break
}"""

        elif intent[-1]=='do_while_loop':
            to_send = """repeat {
    var i = 1
    //enter your code here.
    i = i + 1
} while a &lt; b"""

        elif intent[-1]=='init_string':
            to_send = """var your_string = 'change it here' """

        elif intent[-1]=='init_int':
            to_send = """var your_integer = 0 """

        elif intent[-1]=='init_char':
            to_send = """var your_char = 'C' """

        elif intent[-1]=='init_float':
            to_send = """var your_float = 0.00 """

        elif intent[-1]=='arith_addition':
            to_send = """func add(a: Int , b: Int) -> Int {
    let sum = a + b
    return sum
}
print("sum is" , add(a: 2, b: 4), separator: " ")"""

        elif intent[-1]=='arith_subtraction':
            to_send = """func sub(a: Int , b: Int) -> Int {
    let diff = a - b
    return diff
}
print("diff is" , sub(a: 10, b: 4), separator: " ")"""

        elif intent[-1]=='arith_multiplication':
            to_send = """func multi(a: Int , b: Int) -> Int {
    let prod = a * b
    return prod
}
print("product is" , multi(a: 2, b: 4), separator: " ")"""

        elif intent[-1]=='arith_division':
            to_send = """func divi(a: Int , b: Int) -> Int {
    let diff = a / b
    return diff
}
print("quotient is" , divi(a: 19, b: 4), separator: " ")"""

        elif intent[-1]=='arith_remainder':
            to_send = """func modu(a: Int , b: Int) -> Int {
    let mod = a % b
    return mod
}
print("reminder is" , modu(a: 18, b: 4), separator: " ")"""

        elif intent[-1]=='def_function':
            to_send = """func your_func_name(a: Int , b: Int) -> String {
    //enter your code
    if a &gt; b{
        The_final_output = "Edit this function"
    }
    return The_final_output
}
print("output:" , your_func_name(a: 18, b: 4), separator: " ")"""

        elif intent[-1]=='recus':
            to_send = """func your_fun(a: Int) -> String {
    var a = a + 1
    if a <= 15 {
        print(a)
        your_fun(a: a)
        }
    else{
        print("a has exceeded the limit of 15")
    }
    return ""
}
print(your_fun(a: 9))"""


        elif intent[-1]=='create_array':
            to_send = """var your_array = [1,2,3,4,5,6]
print(your_array)"""

        elif intent[-1]=='switch_condition':
            to_send = """let someCharacter: Character = "z" // or someinteger: Int = 2
switch someCharacter {
case "a": // case 1:
    // enter your code
case "z": // case 2:
    // enter your code
default:
    // default reply
}"""

        elif intent[-1]=='cplus' or intent[-1]=='python' or intent[-1]=='php':
            to_send= """Please Use the Change language option!"""
        
        elif intent[-1]=='swift':
            to_send="""running swift"""
        
        else:
            to_send="""I am sorry, i dont know what that means""" 

        c+=1
        return json.dumps({"response": to_send}), 200

    c+=1
    return json.dumps({"response": 'Come back later for that language :) '}), 200
    

if __name__=='__main__':
    c=1
    intent=[]
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=False)
