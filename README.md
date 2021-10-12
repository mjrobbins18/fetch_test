# fetch rewards test problem

This is a simple web service that uses three routes to mimic mock transactions, spending of points, and checking point balance by payer.

## Language/Framework

This webservice is written in python, using django. This current iteration of this test runs on the local server. All of the code is located in the ```/points/urls.py``` file. I used pipenv for this project and have included a Pipfile. Django must be installed. It can be installed using ```pip install``` in the root directory once the repository has been cloned.

## Steps of Operation
### Please note that these routes must be accessed in the proper succession in order to get the desired results, otherwise there are no transactions to populate the balance and points cannot be spent.

1. The first step is to launch the local server.In the terminal, navigate into the root directory of the repository and run the command: ```python3 manage.py runserver```. The webservice will now be able to be accessed at [Local Host](http://127.0.0.1:8000).

2. Next, the order of operations is to start with the transaction route (The balance and spend route can be accessed, but with no transactions there is no balance). The route to fill the transaction list is ```/transaction``` and can be accessed here: [Transaction Route](http://127.0.0.1:8000/transaction)

3. After the transaction list has been populated, the spend route will spend the amount of points defined on line 27 in ```/points/urls.py.``` The route is ```/spend``` and can be accessed here: [Spend Route](http://127.0.0.1:8000/spend). The points will be spent first based on the oldest transaction, and not allow any balances to dip below 0. The response to the spend route is a dictionary with the amount removed from each payer balance.

4. The last step is to run the balance route. The response to the balance route is the ending balance per payer after points have been spent. It is possible to check balance before calling the spend route, but only after the transaction route has been called. The balance route is ```/balance``` and can be accessed here: [Balance Route](http://127.0.0.1:8000/balance)

## Notes

- This is the most simple way I was able to solve this problem, but I would do it differently if there were other factors to consider.
- If the average transaction list was much larger I would spend time to organize the transactions in a way that I didn't have to filter through each one every time in order to find the oldest timestamps.
- Also, in a scenario where two people are using the same account and spending points at the very same time, this model would produce issues. 
- Lastly, I think that I came to the correct conclusion about transactions with negative points, but wanted to explain how I think they are utilized and expressed in my solution. I beleive that negative points are listed in the transaction list to show the remainder of points left in a specific transaction if the amount of points spent do not exhaust the amount in the transaction. I solved this problem in my answer by appending the remainder back to the transaction list. 