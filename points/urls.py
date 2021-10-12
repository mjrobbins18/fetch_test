"""points URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import Counter, DefaultDict
from django.contrib import admin
from django.http.response import JsonResponse
from django.urls import path
from django.http import HttpResponse
from datetime import datetime

def app(environ, start_response):
    """Simplest possible application object"""
    data = b'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])


# Transaction list
transactions = []

# spend dict. 
spends= {'points': 5000}

# dictionary to hold balance list
c = DefaultDict(int)

        
# dictionary to hold the response of spending points
z = DefaultDict(int)

# get transactions
def transaction(request):
    transactions.append({'payer': 'DANNON', 'points': 300, 'timestamp': datetime(2020, 11, 5) })
    transactions.append({'payer': 'MILLER COORS', 'points': 10000, 'timestamp': datetime(2020, 11, 6) })
    transactions.append({'payer': 'DANNON', 'points': -200, 'timestamp': datetime(2020, 11, 5) })
    transactions.append({'payer': 'UNILEVER', 'points': 200, 'timestamp': datetime(2020, 11, 4) })
    transactions.append({'payer': 'DANNON', 'points': 1000, 'timestamp': datetime(2020, 11, 8) })
    for d in transactions:
        c[d['payer']] += d['points']
    return JsonResponse(transactions, safe=False)

# spend points
def spend(request):
   
    # sort transactions by timestamp and then points
    sorted_transactions = sorted(transactions, key=lambda x:(x['timestamp'], x['points']))  
  
    # balance tally
    balance = 0

    # response array
    res = []

    # loop to get initial balance
    for i in sorted_transactions:
        balance += i['points']

    # points variable
    points = spends['points']
    
    # conditional to find if there is a transaction history, balance, or if the amount of points that you are trying to spend are greater than the balance.
    if points == 0 or len(transactions) == 0 or balance <= 0 or points > balance: return HttpResponse("There is no balance")
    
    # tally of points as we're iterating
    tally = points
    
    # iterating through the sorted transaction list
    for i in sorted_transactions:
        
        # base case, if the amount of points left to spend is less than the amount available in the transaction
        if i['points'] > points:
            tally =  abs(tally - i['points'])
            # the amount of points taken out of the amount available per transaction
            neg_points = i['points'] - tally
            # adds a negative transaction to the transaction list in order to keep track of the remaining transaction balance
            transactions.append({'payer': i['payer'], 'points': -tally, 'timestamp': datetime.now()})
            res.append({'payer': i['payer'], 'points': -neg_points})
            print(i, 'spent and last')
            break
        # recursive case, if the amount of points available to spend is larger than the amount per transaction
        else:   
            tally -= i['points']
            res.append({'payer': i['payer'], 'points': -(i['points'])})
            print(i, 'spent')
    
    # dictionary to display the amount of points taken from each payer
    for y in res:
        z[y['payer']] += y['points']
    
    # ending total balance 
    balance -= points


    return JsonResponse(z, safe=False)

  

# check balance
final_balance = []

def balance(request):
    
    # if no transactions have been made, there is no balance
    if z == {} and c == {}:
        return HttpResponse("There is no balance")
    
    # can check balance once transactions have been made 
    if z == {}:
        return JsonResponse(c, safe=False)
    # gives balance after points have been spent
    else:    
        for i in c:
            final_balance.append({i:c[i]+z[i]})
            
        return JsonResponse(final_balance, safe=False)


# urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('transaction', transaction),
    path('spend', spend),
    path('balance', balance),
]
