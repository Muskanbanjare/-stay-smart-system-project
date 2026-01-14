from django.shortcuts import render,redirect
import mysql.connector
from django.contrib.auth import authenticate,logout,login
from .import models
from .forms import Online_Booking_form,offline_Booking_form,Add_Employee_form,Add_Room_form,Add_salary_form
from django.http import HttpResponse
from .models import Add_Employee,Add_Salarys
# Create your views here.
def Home(request):
    return render(request,'Home.html')
def all(request):
    return render(request,'allinclude.html')

def OnlineBooking(request):
    if request.method == 'POST':
        room_number = request.POST.get('Room_Number')
        check_in = request.POST.get('Check_in')
        check_out = request.POST.get('Check_out')

        # Check for overlapping bookings
        overlapping = models.Online_Booking.objects.filter(
            Room_Number=room_number,
            Check_in__lt=check_out,
            Check_out__gt=check_in
        )

        if overlapping.exists():
            return HttpResponse(f'''
                <div style="max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid red;
                             border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); font-family: Arial, sans-serif;">
                    <h2 style="color: red;">Room Already Booked!</h2>
                    <p>Room <strong>{room_number}</strong> is already booked between those dates.</p>
                </div>
            ''')

        upload_image = request.FILES.get('Img')

        MyData = models.Online_Booking()
        MyData.Id = request.POST.get('Id')
        MyData.Room_Number = room_number
        MyData.Check_in = check_in
        MyData.Check_out = check_out
        MyData.ADULT = request.POST.get('ADULT')
        MyData.CHILDREN = request.POST.get('CHILDREN')
        MyData.Name = request.POST.get('Name')
        MyData.Surname = request.POST.get('Surname')
        MyData.Email = request.POST.get('Email')
        MyData.Phone_Number = request.POST.get('Phone_Number')
        MyData.Nid_No = request.POST.get('Nid_No')
        MyData.City = request.POST.get('City')
        MyData.Country = request.POST.get('Country')
        MyData.Img = upload_image
        MyData.Address = request.POST.get('Address')
        MyData.Date = request.POST.get('Date')
        MyData.Time = request.POST.get('Time')
        MyData.save()

        return HttpResponse(f'''
            <div style="max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; 
                         border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); font-family: Arial, sans-serif;">
                <h2 style="color: green;">Booking Successfully!</h2>
                <p>Your name: {MyData.Name} <br>
                Your ID: {MyData.Id} <br>
                Check-in time: {MyData.Check_in} <br>
                Check-out time: {MyData.Check_out}</p>
            </div>
        ''')

    return render(request, 'online_booking_page.html')

def Aothur_login(request):
    # conn = mysql.connector.connect(host='localhost', user='root', password='', database='Hotel_Management_System')
    if request.method == 'POST':
        User_email = request.POST.get('Email')
        User_password = request.POST.get('Password')
        # cur = conn.cursor()
        # quer1 = "select Email,Password from Authority_reg where Email=%s"
        # val = (User_email,)
        # cur.execute(quer1, val)
        # data = cur.fetchall()
        # print(data, User_email)
        # if User_email == data[0][0] and User_password == data[0][1]:
        if models.Authorregis.objects.filter(Email=User_email, Password=User_password):
            return redirect("Adminpage")
        else:
            return HttpResponse('user name and password not matching')
    return render(request,'Athur_login_page.html')
def auth_logout(request):
    logout(request)
    return redirect('Home')
def Aothur_Reg(request):
    if request.method == 'POST':
        Data = models.Authorregis()
        Data.Fname = request.POST.get('Fname')
        Data.Lname = request.POST.get('Lname')
        Data.Email = request.POST.get('Email')
        Data.Phone_Number = request.POST.get('Phone_Number')
        Data.Password = request.POST.get('Password')
        Con_password = request.POST.get('Con_password')
        if Data.Password == Con_password:
            Data.save()
            return redirect('Aothur_login')
        else:
           return HttpResponse('password and confirm password not matching')
    return render(request,'Athur_Register_Page.html')
def Aothur_Fotpass(request):
    return render(request,'Author_forgetpass_page.html')
def all_admin(request):
    return render(request,'admin/AdminAllinclude.html')
def Admin(request):
    data = models.Online_Booking.objects.all().order_by('-Id')
    return render(request,'admin/Admin.html',{'data':data})
def Addemployee(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Upload_Image')
        # fname = upload_image.name
        # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
        #     for ch in upload_image.chunks():
        #         location.write(ch)
        if request.method == 'POST':
            Data = models.Add_Employee()
            Data.Employee_Id = request.POST.get('Employee_Id')
            Data.First_Name = request.POST.get('First_Name')
            Data.Last_Name = request.POST.get('Last_Name')
            Data.Email = request.POST.get('Email')
            Data.Mobile_Number = request.POST.get('Mobile_Number')
            Data.Joining_Date = request.POST.get('Joining_Date')
            Data.Dateof_Birth = request.POST.get('Dateof_Birth')
            Data.Departments = request.POST.get('Departments')
            Data.Gender = request.POST.get('Gender')
            Data.Blood_Group = request.POST.get('Blood_Group')
            Data.Education = request.POST.get('Education')
            Data.Personal_Identity = request.POST.get('Personal_Identity')
            Data.Guardian = request.POST.get('Guardian')
            Data.Guardian_Number = request.POST.get('Guardian_Number')
            Data.Upload_Image = upload_image
            Data.Address = request.POST.get('Address')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('Addemployee')
        else:
            return HttpResponse("Failed")

    data = models.Add_Employee.objects.all().order_by('-Employee_Id')
    return render(request,'admin/addemployee.html',{'data':data})
def Editemployee(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    if request.method == 'POST':
        data = Add_Employee_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Upload_Image')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('Allemployee')
        else:
            return HttpResponse("Failed")

    select = data.Departments
    if select == 'Departments':
        select = 1
    elif select == 'Housekeeping':
        select = 2
    elif select == 'Manager':
        select = 3
    elif select == 'Chef':
        select = 4
    elif select == 'Food and Beverage':
        select = 5
    elif select == 'Kitchen':
        select = 6
    elif select == 'Security':
        select = 7
    else:
        select = 8

    select = data.Gender
    if select == 'Gender':
        select = 1
    elif select == 'MALE':
        select = 2
    else:
        select = 3

    return render(request,'admin/Editemployee.html',{'data': data,"select": select})
def Allemployee(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Add_Employee.objects.filter(Employee_Id=Serch) or models.Add_Employee.objects.filter(First_Name=Serch)
        return render(request, 'admin/allemployee.html', {"data": data})
    data = models.Add_Employee.objects.all().order_by('-Employee_Id')
    return render(request,'admin/allemployee.html',{'data': data})
def online_Booking_info(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        show = models.Online_Booking.objects.filter(Country =Serch) or models.Online_Booking.objects.filter(Name=Serch)
        return render(request,'admin/Online_Booking.html',{"data":show})

    data = models.Online_Booking.objects.all().order_by('-Id')
    return render(request,'admin/Online_Booking.html',{'data':data})
def Edit_online_Booking(request,id):
    data = models.Online_Booking.objects.get(Id=id)
    if request.method == 'POST':
        data = Online_Booking_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Img')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('online_Booking_info')
        else:
            return HttpResponse("Failed")

    select = data.ADULT
    if select == 'ADULT':
        select = 1
    elif select == '1 ADULT':
        select = 2
    elif select == '2 ADULT':
        select = 3
    elif select == '3 ADULT':
        select = 4
    else:
        select = 5

    select = data.CHILDREN
    if select == 'CHILDREN':
        select = 1
    elif select == '1 CHILDREN':
        select = 2
    elif select == '2 CHILDREN':
        select = 3
    elif select == '3 CHILDREN':
        select = 4
    else:
        select = 5
    return render(request,'admin/EditonlineBooking.html',{'data': data,"select":select})
def AddCustomer(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Upload_Image')

        # Get booking details from form
        room_number = request.POST.get('Room_Number')
        check_in = request.POST.get('Check_in')
        check_out = request.POST.get('Check_out')

        # 🛑 Check if the room is already booked in that date range
        overlapping = models.Offline_Booking.objects.filter(
            Room_Number=room_number,
            Check_in__lt=check_out,
            Check_out__gt=check_in
        )

        if overlapping.exists():
            # Show error in a friendly way
            return HttpResponse(f'''
                <div style="max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid red;
                             border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); font-family: Arial, sans-serif;">
                    <h2 style="color: red;">Room Already Booked!</h2>
                    <p>Room <strong>{room_number}</strong> is already booked for the selected dates.</p>
                    <a href="/AddCustomer" style="color: blue;">Go Back</a>
                </div>
            ''')

        # ✅ No overlap — save the booking
        Data = models.Offline_Booking()
        Data.Customer_Id = request.POST.get('Customer_Id')
        Data.Check_in = check_in
        Data.Check_out = check_out
        Data.First_Name = request.POST.get('First_Name')
        Data.Last_Name = request.POST.get('Last_Name')
        Data.Email = request.POST.get('Email')
        Data.Mobile_Number = request.POST.get('Mobile_Number')
        Data.ADULT = request.POST.get('ADULT')
        Data.CHILDREN = request.POST.get('CHILDREN')
        Data.Total_Person = request.POST.get('Total_Person')
        Data.Select_Room = request.POST.get('Select_Room')
        Data.Room_Number = room_number
        Data.Gender = request.POST.get('Gender')
        Data.Personal_Identity = request.POST.get('Personal_Identity')
        Data.Upload_Image = upload_image
        Data.Country = request.POST.get('Country')
        Data.Address = request.POST.get('Address')
        Data.Date = request.POST.get('Date')
        Data.Time = request.POST.get('Time')
        Data.save()
        return redirect('AddCustomer')

    # GET request — render page with existing bookings
    data = models.Offline_Booking.objects.all().order_by('-Customer_Id')
    return render(request, 'admin/AddCustomer.html', {'data': data})

def AllCustomer(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Offline_Booking.objects.filter(First_Name=Serch) or models.Offline_Booking.objects.filter( Email=Serch)
        return render(request, 'admin/AllCustomer.html', {"data": data})
    data = models.Offline_Booking.objects.all().order_by('-Customer_Id')
    return render(request,'admin/AllCustomer.html',{'data': data})
def EditCustomer(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    if request.method == 'POST':
        data = offline_Booking_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Upload_Image')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('AllCustomer')
        else:
            return HttpResponse("Failed")

    select = data.ADULT
    if select == 'ADULT':
        select = 1
    elif select == '1 ADULT':
        select = 2
    elif select == '2 ADULT':
        select = 3
    elif select == '3 ADULT':
        select = 4
    else:
        select = 5

    select = data.CHILDREN
    if select == 'CHILDREN':
        select = 1
    elif select == '1 CHILDREN':
        select = 2
    elif select == '2 CHILDREN':
        select = 3
    elif select == '3 CHILDREN':
        select = 4
    else:
        select = 5

    select = data.Select_Room
    if select == 'Select Room':
        select = 1
    elif select == 'Delux':
        select = 2
    elif select == 'Super Delux':
        select = 3
    elif select == 'Single':
        select = 4
    else:
        select = 5

    select = data.Room_Number
    if select == 'Room Number':
        select = 1
    elif select == 'Room101':
        select = 2
    elif select == 'Room102':
        select = 3
    elif select == 'Room103':
        select = 4
    else:
        select = 5

    select = data.Gender
    if select == 'Gender':
        select = 1
    elif select == 'MALE':
        select = 2
    else:
        select = 3

    return render(request,'admin/EditCustomer.html',{'data': data,"select": select})
def Delete(request,id):
    data = models.Online_Booking.objects.get(Id=id)
    data.delete()
    return redirect('online_Booking_info')

def Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        if Serch:
            data = models.Offline_Booking.objects.filter(First_Name__icontains=Serch) or models.Offline_Booking.objects.filter(Email__icontains=Serch)
        else:
            data=models.Offline_Booking.objects.all()
        print(data)
        return render(request, 'admin/AddCustomer.html', {"data": data})

def AddCustpage_Delete(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    data.delete()
    return redirect('AddCustomer')
def AllCustpage_Delete(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    data.delete()
    return redirect('AllCustomer')

def AddEmplopage_Delete(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    data.delete()
    return redirect('Addemployee')

def Add_Employee_Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        if Serch:
            data = models.Add_Employee.objects.filter(Employee_Id=Serch) or models.Add_Employee.objects.filter(First_Name=Serch)
        else:
            data = models.Add_Employee.objects.all()
        return render(request,'admin/addemployee.html', {"data": data})

def AllEmployee_Delete(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    data.delete()
    return redirect('Allemployee')


def Add_room(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Room_Image')
        # fname = upload_image.name
        # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
        #     for ch in upload_image.chunks():
        #         location.write(ch)
        if request.method == 'POST':
            Data = models.Add_Room()
            Data.Room_Number = request.POST.get('Room_Number')
            Data.Room_Type = request.POST.get('Room_Type')
            Data.Room_Floor = request.POST.get('Room_Floor')
            Data.Room_Facility = request.POST.get('Room_Facility')
            Data.Room_Price = request.POST.get('Room_Price')
            Data.Room_Image = upload_image
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('Add_room')
        else:
            return HttpResponse("Failed")

    data = models.Add_Room.objects.all().order_by('-Room_Number')
    return render(request, 'admin/AddRoom.html',{'data': data})

def Add_Room_Search(request):
    if request.method == 'POST':
        serch = request.POST.get('serch')
        print(serch)
        if serch:
            data = models.Add_Room.objects.filter(Room_Number__icontains=serch)
        else:
            data = models.Add_Room.objects.all()
        print(data)
        return render(request, 'admin/AddRoom.html',{"data": data})

def AddRooms_Delete(request,id):
    data = models.Add_Room.objects.get(Id=id)
    data.delete()
    return redirect('Add_room')

def EditRooms(request,id):
    data = models.Add_Room.objects.get(Id=id)
    if request.method == 'POST':
        data = Add_Room_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Room_Image')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('All_Room')
        else:
            return HttpResponse("Failed")


    select = data.Room_Type
    if select == 'Select Room':
        select = 1
    elif select == 'Delux':
        select = 2
    elif select == 'Super Delux':
        select = 3
    elif select == 'Single':
        select = 4
    else:
        select = 5

    select = data.Room_Number
    if select == 'Room Number':
        select = 1
    elif select == 'Room101':
        select = 2
    elif select == 'Room102':
        select = 3
    elif select == 'Room103':
        select = 4
    else:
        select = 5

    select = data.Room_Floor
    if select == 'Room Floor':
        select = 1
    elif select == 'Floor_G':
        select = 2
    elif select == 'Floor_First':
        select = 3
    elif select == 'Floor_Second':
        select = 4
    else:
        select = 5

    return render(request,'admin/EditRooms.html',{'data': data,"select": select})

def All_Room(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Add_Room.objects.filter(Room_Number=Serch) or models.Add_Room.objects.filter(Room_Type=Serch)
        return render(request, 'admin/AllRooms.html',{"data": data})

    data = models.Add_Room.objects.all().order_by('-Id')
    return render(request, 'admin/AllRooms.html',{'data': data})

def AllRooms_Delete(request,id):
    data = models.Add_Room.objects.get(Id=id)
    data.delete()
    return redirect('All_Room')

def AddEmployeeSalary(request):
    if request.method=='GET':
        print('yes')
        data=Add_Salarys.objects.all()
        return render(request,'admin/AddEmployeeSalary.html',{'data': data})
    if request.method == 'POST':
        if request.method == 'POST':
            emp=Add_Employee.objects.get(Employee_Id=request.POST.get('Employee_Id'))
            Data = models.Add_Salarys()
            Data.Employee_Id = emp
            Data.Employee_Name = emp.First_Name
            Data.Email = emp.Email
            Data.Mobile_Number =emp.Mobile_Number
            Data.Departments = request.POST.get('Departments')
            Data.Salary = request.POST.get('Salary')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('AddEmployeeSalary')
        else:
            return HttpResponse("Failed")

    return render(request, 'admin/AddEmployeeSalary.html')

def EmployeeShow(request):

    return render(request, 'admin/EmployeeShow.html')

def Add_Employee_Salary_Search(request):
    if request.method == 'POST':
        serch = request.POST.get('serch')
        print(serch)
        if serch:
            data = models.Add_Salarys.objects.filter(Employee_Id=serch)
        else:
            data = models.Add_Salarys.objects.all()
        print(data)
        return render(request,'admin/AddEmployeeSalary.html',{'data': data})
