from django.shortcuts import render, redirect
from django.http import HttpResponse
import pymysql
from django.db import connection
from django.contrib import messages
from django.conf import settings
import os

from django.shortcuts import render
from django.db import connection

def index(request):
     return render(request ,'index.html')


def home(request):
     return render(request ,'home.html')


     
  



def submitreq(request):
    if request.method == 'POST':
        # Extract data from the POST request
        description = request.POST.get('description')
        service_request = request.POST.get('service_request')
        image = request.FILES.get('image')  # Retrieve uploaded image file
        customer_id = request.POST.get('customer_id')  # Assuming you pass the CustomerID from the form
        
        # Save the uploaded image to a location on the server
        image_path = os.path.join(settings.MEDIA_ROOT, image.name)
        with open(image_path, 'wb') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Execute raw SQL to insert data into the MySQL database
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO ServiceReq (CustomerID, Description, ServiceRequest, Image) VALUES (%s, %s, %s, %s)",
                (customer_id, description, service_request, image_path)
            )
        
        # Redirect to a success page or display a success message
        return HttpResponse('Service request submitted successfully!')
    
    # If request method is not POST, render the form
    return render(request, 'service_request_form.html')






def track(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        
        # Fetch service requests from the database based on the provided contact number
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM ServiceReq WHERE CustomerId = %s", [customer_id]
            )
            service_requests = cursor.fetchall()
        
        # Render a template with the fetched service requests
        return render(request, 'tracking.html', {'service_requests': service_requests})
    
    # If request method is not POST, render the form
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if username and password are 'admin'
        if username == 'admin' and password == 'admin':
            # If credentials are correct, redirect to service.html
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM ServiceReq"
                )
                service_requests = cursor.fetchall()  # Fetch service requests

            if service_requests:  # Check if there are any service requests
                # Render a template with the fetched service requests
                return render(request, 'service.html', {'service_requests': service_requests})
            else:
                # If there are no service requests, render the template without any data
                return render(request, 'service.html')
        else:
            # If credentials are incorrect, render the login page again with an error message
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    # If request method is not POST or if it's a GET request, render the login page
    return render(request, 'login.html')







from datetime import datetime

def update_status(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('new_status')

        # Update the status of the service request in the database
        with connection.cursor() as cursor:
            if new_status == 'Resolved':
                cursor.execute(
                    "UPDATE ServiceReq SET Status = %s, DateResolved = %s WHERE RequestID = %s",
                    [new_status, datetime.now(), request_id]
                )
            else:
                cursor.execute(
                    "UPDATE ServiceReq SET Status = %s WHERE RequestID = %s",
                    [new_status, request_id]
                )
        
        # Fetch updated service requests
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM ServiceReq"
            )
            service_requests = cursor.fetchall()  # Fetch service requests

        # Render the service page with the updated service requests
        return render(request, 'service.html', {'service_requests': service_requests})

    # If the request method is not POST, redirect to the service page
    return redirect('service_page')


def register_customer1(request):
   if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')

        # Connect to the MySQL database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database='gas',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a SQL query to insert the data into the database
                sql = "INSERT INTO Customer (Name, Email, Phone, Address, PasswordHash) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, email, phone, address, password))

            # Commit the transaction
            connection.commit()
            return render(request,'home.html')
        finally:
            # Close the database connection
            connection.close()




def logincust1(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        
        # Query the database to check if the phone number and password match
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Customer WHERE Phone = %s AND PasswordHash = %s", (phone, password))
            user = cursor.fetchone()
        
        if user:
            # If user exists, extract the CustomerID
            customer_id = user[0]  # Assuming the CustomerID is at index 0 in the database row

            # Redirect to the submit service request page and pass the CustomerID as a parameter
            return render(request, 'index.html', {'customer_id': customer_id})
        
     #   contact_number = request.POST.get('contact_number')
        
        # Fetch service requests from the database based on the provided contact number
            with connection.cursor() as cursor:
                cursor.execute(
                 "SELECT * FROM ServiceReq WHERE CustomerId = %s", [customer_id]
                )
                user = cursor.fetchall()
        
        # Render a template with the fetched service requests
            return render(request, 'index.html', {'user': user})
    
        else:
            # If user does not exist or password is incorrect, show error message
            messages.error(request, 'Invalid phone number or password')
            return render(request,'home.html')
    else:
        return render(request, 'logincust1.html')



def account(request):
    # Fetch the account details of the user with the provided customer_id
    customer_id = request.POST.get('customer_id')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Customer WHERE CustomerID = %s", [customer_id]
        )
        user = cursor.fetchone()

    # Render the template with the fetched user details
    return render(request, 'account.html', {'user': user})