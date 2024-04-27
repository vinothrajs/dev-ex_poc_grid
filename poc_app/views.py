import json
import re
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required

import ast


# Create your views here.
def index2(request):
    users = CustomUser.objects.all()
    return render(request, "index.html", {"users": users})


from django.contrib.auth.decorators import login_required


@login_required
def contact(request):
    users = CustomUser.objects.all()

    # content_type = ContentType.objects.get_for_model(CustomUser)
    # post_permission = Permission.objects.filter(content_type=content_type)
    # print([perm.codename for perm in post_permission])

    return render(request, "contact.html", {"users": users})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.views.decorators.cache import never_cache

@never_cache
def index(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page or wherever you want
            return redirect("home")
        else:
            # Return an error message or handle unsuccessful login
            return render(request, "index.html", {"error_message": "Invalid username or password"})

    # If the request method is GET, render the login page
    return render(request, "index.html")


from django.contrib.messages import constants as messages
from django.contrib.auth import logout
from django.shortcuts import redirect


@login_required
def logout_view(request):
    #logout(request)
    logout(request)
    # messages.success(request, 'You are now logged out')
    return redirect('index')
import time
## SPA example
@login_required
def home(request):
    users = CustomUser.objects.all()
    time.sleep(1)
    context = {
                "template": _base_template(request) ,
                "users": users,
                "role" : "Manager"
            }
    return render(request, "contact.html", context)

@login_required
def forms(request):
    data = "it is form page from template render"
    time.sleep(1)
    if request.htmx:
        print("htmx forms")
        return render(request, "form.html", {"data": data})
    else:
        print("non htmx forms")
        return render(request, "form_full.html", {"data": data})

# Python has no private access modifiers. To work around this, one adds an underscore (_) before the function
# or variable to signal to other devs that they are meant to be private. Note that they can still be accessed
# outside the module since Python does not enforce the convention. It simply trusts that everyone is a "consenting adult"
@login_required
def _base_template(request):
    return "_base_empty.html" if request.htmx else "_base.html"

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def your_api_endpoint(request):
    # Pagination parameters
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))

    # Filtering parameters
    filters = request.POST.getlist('filters[]')

    # Construct WHERE clause for dynamic filtering
    where_conditions = []
    params = []
    for filter_str in filters:
        column, condition, value = filter_str.split(',')
        if condition == 'contains':
            where_conditions.append("%s ILIKE %s")
            params.extend([column, f"'%{value}%'"])
        elif condition == 'equals':
            where_conditions.append("%s = %s")
            params.extend([column, value])

    where_clause = " AND ".join(where_conditions)
    # Your raw SQL query to fetch data with pagination and filtering
    query = f"""
        SELECT name, age
        FROM customuser
        WHERE {where_clause}
        LIMIT %s OFFSET %s
    """
    params.extend([length, start])

    # Execute the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        data = cursor.fetchall()

    # Prepare the data in a format suitable for DataTables
    response_data = []
    for row in data:
        response_data.append({
            'name': row[0],
            'age': row[1],
            # Add more fields as needed
        })

    return JsonResponse({'data': response_data})

from django.utils.encoding import uri_to_iri

def generic_sql(value):
    value = value.replace("[", "").replace("]", "").replace(",", " ").replace("'", "").replace('"', "")

    split_expression = value.split()
    # Add single quotes around values at index 2, 5, and 8
    for i in range(len(split_expression)):
        if i % 4 == 2:
            split_expression[i] = "'" + split_expression[i] + "'"

    # Reconstruct the expression
    value = ' '.join(split_expression)
    return value


# def filter_to_sql(filter_list, table_name):
#     sql_query = ""    
#     if isinstance(filter_list, list):
#         if type(filter_list[0]) == str:
#             condition = filter_list
#             if isinstance(condition, list):
#                 if condition[1] == "anyof":
#                     sql_query += "{} IN ({}) ".format(condition[0], ", ".join(["'{}'".format(value) for value in condition[2]]))
#                 elif condition[1] == "between":
#                     sql_query += "{} BETWEEN {} AND {} ".format(condition[0], condition[2][0], condition[2][1])
#                 elif condition[1] == "=":
#                     sql_query += "{} = '{}' ".format(condition[0], condition[2])
#                 elif condition[1] == "<>":
#                     sql_query += "{} <> '{}' ".format(condition[0], condition[2])
#                 elif condition[1] == "<":
#                     sql_query += "{} < '{}' ".format(condition[0], condition[2])
#                 elif condition[1] == ">":
#                     sql_query += "{} > '{}' ".format(condition[0], condition[2])
#                 elif condition[1] == "<=":
#                         sql_query += "{} <= '{}' ".format(condition[0], condition[2])
#                 elif condition[1] == ">=":
#                     sql_query += "{} >= '{}' ".format(condition[0], condition[2])
#                 elif condition[1] == "contains":
#                     sql_query += "{} LIKE '%{}%' ".format(condition[0], condition[2])
#                 elif condition[1] == "notcontains":
#                     sql_query += "{} NOT LIKE '%{}%' ".format(condition[0], condition[2])
#                 elif condition[1] == "startswith":
#                     sql_query += "{} LIKE '{}%' ".format(condition[0], condition[2])
#                 elif condition[1] == "endswith":
#                     sql_query += "{} LIKE '%{}' ".format(condition[0], condition[2])
#             elif condition == "or":
#                 sql_query += "OR "
#             elif condition == "and":
#                 sql_query += "AND "
#             pass
#         else:
#             for condition in filter_list:
                
#                 if isinstance(condition, list):
#                     if condition[1] == "anyof":
#                         sql_query += "{} IN ({}) ".format(condition[0], ", ".join(["'{}'".format(value) for value in condition[2]]))
#                     elif condition[1] == "between":
#                         sql_query += "{} BETWEEN {} AND {} ".format(condition[0], condition[2][0], condition[2][1])
#                     elif condition[1] == "=":
#                         sql_query += "{} = '{}' ".format(condition[0], condition[2])
#                     elif condition[1] == "<":
#                         sql_query += "{} < '{}' ".format(condition[0], condition[2])
#                     elif condition[1] == ">":
#                         sql_query += "{} > '{}' ".format(condition[0], condition[2])
#                     elif condition[1] == "<>":
#                         sql_query += "{} <> '{}' ".format(condition[0], condition[2])
#                     elif condition[1] == "<=":
#                         sql_query += "{} <= '{}' ".format(condition[0], condition[2])
#                     elif condition[1] == ">=":
#                         sql_query += "{} >= '{}' ".format(condition[0], condition[2])
#                     elif condition[1] == "contains":
#                         sql_query += "{} LIKE '%{}%' ".format(condition[0], condition[2])
#                     elif condition[1] == "notcontains":
#                         sql_query += "{} NOT LIKE '%{}%' ".format(condition[0], condition[2])
#                     elif condition[1] == "startswith":
#                         sql_query += "{} LIKE '{}%' ".format(condition[0], condition[2])
#                     elif condition[1] == "endswith":
#                         sql_query += "{} LIKE '%{}' ".format(condition[0], condition[2])

#                     elif isinstance(condition, list):
#                         for condition in filter_list:                
#                             if isinstance(condition, list):
#                                 if condition[1] == "anyof":
#                                     sql_query += "{} IN ({}) ".format(condition[0], ", ".join(["'{}'".format(value) for value in condition[2]]))
#                                 elif condition[1] == "between":
#                                     sql_query += "{} BETWEEN {} AND {} ".format(condition[0], condition[2][0], condition[2][1])
#                                 elif condition[1] == "=":
#                                     sql_query += "{} = '{}' ".format(condition[0], condition[2])
#                                 elif condition[1] == "<>":
#                                     sql_query += "{} <> '{}' ".format(condition[0], condition[2])
#                                 elif condition[1] == "<=":
#                                     sql_query += "{} <= '{}' ".format(condition[0], condition[2])
#                                 elif condition[1] == ">=":
#                                     sql_query += "{} >= '{}' ".format(condition[0], condition[2])
#                                 elif condition[1] == "contains":
#                                     sql_query += "{} LIKE '%{}%' ".format(condition[0], condition[2])
#                                 elif condition[1] == "notcontains":
#                                     sql_query += "{} NOT LIKE '%{}%' ".format(condition[0], condition[2])
#                                 elif condition[1] == "startswith":
#                                     sql_query += "{} LIKE '{}%' ".format(condition[0], condition[2])
#                                 elif condition[1] == "endswith":
#                                     sql_query += "{} LIKE '%{}' ".format(condition[0], condition[2])
#                             elif condition == "or":
#                                 sql_query += "OR "
#                             elif condition == "and":
#                                 sql_query += "AND "
                 
#                 elif condition == "or":
#                     sql_query += "OR "
#                 elif condition == "and":
#                     sql_query += "AND "
#     else:  # Handling single condition without list
#         sql_query += "{} = '{}' ".format(filter_list[0], filter_list[2])
    
#     return sql_query.rstrip("AND ").rstrip("OR ").rstrip() 

def filter_to_sql(filter_list):
    sql_query = ""
    
    def process_condition(condition):
        nonlocal sql_query
        if condition[1] == "anyof":
            sql_query += "{} IN ({}) ".format(condition[0], ", ".join(["'{}'".format(value) for value in condition[2]]))
        elif condition[1] == "between":
            sql_query += "{} BETWEEN {} AND {} ".format(condition[0], condition[2][0], condition[2][1])
        elif condition[1] in ("=", "<>", "<", ">", "<=", ">="):
            sql_query += "{} {} '{}' ".format(condition[0], condition[1], condition[2])
        elif condition[1] in ("contains", "notcontains", "startswith", "endswith"):
            sql_query += "{} LIKE '%{}%' ".format(condition[0], condition[2]) if condition[1] == "contains" else \
                         "{} NOT LIKE '%{}%' ".format(condition[0], condition[2]) if condition[1] == "notcontains" else \
                         "{} LIKE '{}%' ".format(condition[0], condition[2]) if condition[1] == "startswith" else \
                         "{} LIKE '%{}' ".format(condition[0], condition[2])
    
    if isinstance(filter_list, list):
        if isinstance(filter_list[0], str):
            process_condition(filter_list)
        else:
            for condition in filter_list:
                if isinstance(condition, list):
                    process_condition(condition)
                elif condition in ("or", "and"):
                    sql_query += condition.upper() + " "
    else:
        sql_query += "{} = '{}' ".format(filter_list[0], filter_list[2])
    
    return sql_query.strip("AND ").strip("OR ").strip()

@csrf_exempt
def save_custom_filter(request):
    if request.method == 'POST':
        # Handle POST request
        filter_data = request.POST.get('filter_data')
        print('Received filter data:', filter_data)
        with connection.cursor() as cursor:
            cursor.execute("""
                        INSERT INTO public.poc_app_custom_filter(filter)
                        VALUES (%s)
                    """, [filter_data])
            return JsonResponse({'message': 'Filter data received successfully.'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)
    


@csrf_exempt
def get_fields(request):
    with connection.cursor() as cursor:
        type_mapping = {
            'integer': {'dataType': 'number'},
            'character varying': {'dataType': 'string'},
            'timestamp with time zone': {'dataType': 'date', 'format': 'date'},
            'numeric': {'dataType': 'number', 'format': 'currency'}
        }

        cursor.execute("""
               SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public' AND 
                table_name = 'poc_app_coupon';
            """)

        rows = cursor.fetchall()
    
        response = []
        for field, field_type in rows:
            if field_type in type_mapping:
                response.append({
                    'dataField': field,
                    'caption': field.capitalize().replace('_', ' '),
                    **type_mapping[field_type]
                })

        cursor.execute("SELECT filter FROM public.poc_app_custom_filter")
        filterVal = cursor.fetchone()[0]
        filterVal = json.loads(filterVal)

    data = {
        "fields": response,
        "value" : filterVal
    }
    print(data)
    return JsonResponse(data)
       

@csrf_exempt
def get_couponcodes_json_paging(request):
    skip = int(request.GET.get('skip', 1))
    take = int(request.GET.get('take', 10))
    sort = request.GET.get('sort')
    filter = request.GET.get('filter')
    if sort:
        sort = json.loads(sort)
        order_val = [val for val in sort]
        selector = order_val[0]['selector']
        order = 'DESC' if order_val[0].get('desc', False) else 'ASC'
        sort = f'{selector} {order}'
    else:
        selector = "id"
        order = "asc"
        sort = f'{selector} {order}'

    if filter:
        filter = json.loads(filter)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6")  
        print(filter)
        filter = filter_to_sql(filter)
    else:
        filter = "id <> 0"

    # print(skip)
    # print(take)
    # print(sort)
    # print(filter)
    # page_number = request.GET.get('page', 1)
    # items_per_page = 10  # Adjust this as needed

    # Calculate start and end index for pagination
    # start_index = (page_number - 1) * items_per_page
    # end_index = start_index + items_per_page
    total_count = 0
    # Execute raw SQL query for paginated data
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT id, coupon_code, effective_from, effective_till, discount_percentage
                FROM public.poc_app_coupon
                WHERE {}
                ORDER BY {}
                OFFSET {} LIMIT {}
            """.format(filter,sort,skip,take))
        
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        # Convert fetched data to list of dictionaries
        data = []
        for row in rows:
            row_data = dict(zip(columns, row))
            data.append(row_data)

        cursor.execute("SELECT COUNT(*) FROM public.poc_app_coupon")
        total_count = cursor.fetchone()[0]
    # Construct response data
    response_data = {
        "totalCount": total_count,
        "coupons": data,
        "skip": skip,
        "take": take,
        "sort": sort
    }

    return JsonResponse(response_data)
