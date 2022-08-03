from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector as msql

# Create your views here.
login=False
def connect():
          return msql.connect(host='localhost',user='root',password='admin',database='company')
def loginForm(request):
          global login
          con = connect()
          mycursor = con.cursor()
          query="select * from login"
          mycursor.execute(query)
          mydata = mycursor.fetchone()
          user = mydata[0]
          password = mydata[1]
          
          if request.method=="POST":
                    logindata = request.POST
                    u = logindata['user']
                    p = logindata['pass']
                    if u==user and p==password:
                              login=True
                              return render(request,'home.html')
                    else:
                              return HttpResponse("<h1>Invalid Login Details</h1>")
          else:
                    return render(request,'login.html')
def aboutUs(request):
          return render(request,'aboutus.html')

def contactUs(request):
          return render(request,'contactus.html')
def mainPage(request):
          #if login==True:
                    return render(request,'home.html')
          #else:
           #         return render(request,'login.html')
def newEmployee(request):
          con = connect()
          mycursor = con.cursor()
          
          if request.method=="POST":
                    newdata = request.POST
                    eno = int(newdata['empno'])
                    ename = newdata['ename']
                    edept = newdata['edept']
                    esalary = int(newdata['esalary'])
                    query="insert into emp values({},'{}','{}',{})".format(eno,ename,edept,esalary)
                    mycursor.execute(query)
                    con.commit()
                    return render(request,'feedback.html')
          else:
                    return render(request,'newemp.html')

def showEmployee(request):
          con = connect()
          mycursor = con.cursor()
          query="select * from emp"
          mycursor.execute(query)
          myrecords = mycursor.fetchall()
          output="<table width='70%' align='center' border='2'>\
                    <tr>\
                    <td colspan='4' align='center'>EMPLOYEE DATABASE</td>\
                    </tr>\
                    <tr bgcolor='lightgrey'>\
                    <td>EMPNO</td>\
                    <td>EMP NAME</td>\
                    <td>DEPARTMENT</td>\
                    <td>SALARY </td>\
                    </tr>"
          for row in myrecords:
                    output+=("<tr>\
                    <td>"+str(row[0])+"</td>"+
                    "<td>"+str(row[1])+"</td>"+
                    "<td>"+str(row[2])+"</td>"+
                    "<td>"+str(row[3])+"</td></tr>")
          output+="</table>"
          link = "<p align='center'><a href='/mainpage/'>BACK</a></p>"
          output+=link
          return HttpResponse(output)
def searchEmp(request):
          con = connect()
          mycursor=con.cursor()
          if request.method=="POST":
                    try:
                              formdata = request.POST
                              eno = int(formdata['empno'])
                              query="select * from emp where empno={}".format(eno)
                              mycursor.execute(query)
                              row = mycursor.fetchone()                        
                              output="<table width='70%' align='center' border='2'>\
                              <tr>\
                              <td colspan='4' align='center'>EMPLOYEE DATABASE</td>\
                              </tr>\
                              <tr bgcolor='lightgrey'>\
                              <td>EMPNO</td>\
                              <td>EMP NAME</td>\
                              <td>DEPARTMENT</td>\
                              <td>SALARY </td>\
                              </tr>"
                    
                              output+=("<tr>\
                              <td>"+str(row[0])+"</td>"+
                              "<td>"+str(row[1])+"</td>"+
                              "<td>"+str(row[2])+"</td>"+
                              "<td>"+str(row[3])+"</td></tr>")
                              output+="</table>"
                              link = "<p align='center'><a href='/mainpage/'>BACK</a></p>"
                              output+=link
                              return HttpResponse(output)
                    except:
                              output="<p align='center'><font color='red' size='7'> Employee Number not found </font></a>"
                              output+="<p align='center'><a href='/mainpage/'>BACK</a></p>"
                              return HttpResponse(output)
          else:
                    return render(request,'searchemp.html')

def editEmp(request):
          con = connect()
          mycursor=con.cursor()
          if request.method=="POST":
                    try:
                              formdata = request.POST
                              if formdata['update']=='Update':
                                        eno = int(formdata['empno'])
                                        name = formdata['name']
                                        dept = formdata['dept']
                                        salary=int(formdata['salary'])
                                        query="update emp set name='{}',dept='{}',salary={} where empno={}".format(name,dept,salary,eno)
                                        mycursor.execute(query)
                                        con.commit()
                                        output="<p align='center'><font color='red' size='7'> Record Update Successfully! </font></a>"
                                        output+="<p align='center'><a href='/mainpage/'>BACK</a></p>"
                                        return HttpResponse(output)
                                        return HttpResponse(output)
                                        
                              else:
                                        
                                        eno = int(formdata['empno'])
                                        query="select * from emp where empno={}".format(eno)
                                        mycursor.execute(query)
                                        row = mycursor.fetchone()                        
                                        mydict={}
                                        mydict['eno']=str(row[0])
                                        mydict['name']=row[1]
                                        mydict['dept']=row[2]
                                        mydict['salary']=str(row[3])
                                        return render(request,'editemp.html',mydict)
                                                   
                    except Exception as e:
                              #print(e)
                              output="<p align='center'><font color='red' size='7'> Employee Number not found </font></a>"
                              output+="<p align='center'><a href='/mainpage/'>BACK</a></p>"
                              return HttpResponse(output)
          else:
                    return render(request,'editempno.html')

def deleteEmp(request):
          con = connect()
          mycursor=con.cursor()
          if request.method=="POST":
                    try:
                              formdata = request.POST
                              eno = int(formdata['empno'])
                              q="select * from emp where empno={}".format(eno)
                              mycursor.execute(q)
                              r = mycursor.fetchall()
                              if mycursor.rowcount==1:
                                        query="delete from emp where empno={}".format(eno)
                                        mycursor.execute(query)
                                        con.commit()
                                        output="<p align='center'><font color='green' size='7'> Record Deleted Successfully! </font></a>"
                                        output+="<p align='center'><a href='/mainpage/'>BACK</a></p>"
                                        return HttpResponse(output)
                              else:
                                        output="<p align='center'><font color='red' size='7'> Employee Number not found </font></a>"
                                        output+="<p align='center'><a href='/mainpage/'>BACK</a></p>"
                                        return HttpResponse(output)  
                    except:
                              output="<p align='center'><font color='red' size='7'> Employee Number not found </font></a>"
                              output+="<p align='center'><a href='/mainpage/'>BACK</a></p>"
                              return HttpResponse(output)
          else:
                    return render(request,'delsearchempno.html')          
          
          
          
                    
                    
                    
          

                    
          
          
                    
          

