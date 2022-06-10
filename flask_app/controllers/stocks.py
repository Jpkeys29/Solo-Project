from crypt import methods
import json
from flask import render_template,redirect,request,flash,session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.stock import Stock
import requests


#redirect to purchase
@app.route('/purchase')
def purchase():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('purchase.html')

#render purchase 
@app.route('/purchase/gostock', methods=['POST'])
def gostock():
    if 'user_id' not in session:
        return redirect ('/logout')

    # url = "https://yahoofinance-stocks1.p.rapidapi.com/stock-prices"

    # querystring = {"EndDateInclusive":"2022-05-12","StartDateInclusive":"2022-05-12","Symbol":f"{request.form['stock_symbol']}","OrderBy":"Ascending"}

    # headers = {
    #     "X-RapidAPI-Host": "yahoofinance-stocks1.p.rapidapi.com",
    #     "X-RapidAPI-Key": "88e3695b8bmsh42ce67b8bf7a723p1d4abcjsn862b3172e524"
    # }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # data = response.json() #data is an object with all the dictionary
    # # print(data)
    # # print(data['results'][0]['adjClose'])
    
    # session['stock_diction'] ={
    #     'name': request.form['stock_symbol'],
    #     'price':data['results'][0]['adjClose'],
    #     'user_id': session['user_id']
    # }
    stock_info = Stock.api_call(request.form['stock_symbol'])
    return render_template('purchase.html', stock_info = stock_info)
    #stock_info = apit_method(request.form['Proper_name'])
    #return render_template(something.html, stock_info = stock_info)
    #return redirect('/purchase')
    

# stock purchase
@app.route('/purchases/create', methods=['POST'])
def purchase_stock():
    if 'user_id' not in session:
        return redirect('/')
    if not Stock.validate_stock(request.form):
        return redirect ('/portfolio')
    # print((int(request.form['number_of_shares']*int(session["stock_diction"]['price']))))
    
    share_quantity= (int(request.form['number_of_shares']))
    price = (int(session["stock_diction"]['price']))
    

    stock_diction = {
        'name': session["stock_diction"]['name'],
        'price': int(session["stock_diction"]['price']),
        'user_id': session["stock_diction"]['user_id'],
        'quantity':int(request.form['number_of_shares']),
        'total':int(share_quantity * price)
    }

    Stock.new_stock(stock_diction)
    return redirect('/portfolio')

# redirect to picks
@app.route('/mypick/<int:stock_id>/')
def show_pick(stock_id):
    one_pick = Stock.get_one({"id": stock_id})
    stock_info = Stock.api_call(one_pick.name)
    return render_template('picks.html',stock_info = stock_info, one_pick = one_pick ,user = User.get_by_id({'id':session['user_id']}))

# redirect to sell
@app.route('/sell/<int:pick_id>')
def sell_stock(pick_id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('sell.html', one_pick= Stock.get_one({"id": pick_id}),user = User.get_by_id({'id':session['user_id']}))


@app.route("/stock/sell/<stock_id>", methods=['POST'])
def sell_stocks(stock_id):
    if 'user_id' not in session:
        return redirect('/')
    
    shares_sold = int(request.form['shares_to_sell'])
# find the stock
    this_stock = Stock.get_one({'id':stock_id})
    new_number_of_shares = this_stock.quantity - shares_sold
    new_total = new_number_of_shares * this_stock.price
    new_stock_info = {
        'id':stock_id,
        'quantity': new_number_of_shares,
        'total': new_total
    } 
    Stock.sell_stock(new_stock_info)
    return redirect(f"/mypick/{stock_id}")


# @app.route('/mypick/<stock_name>')
# def show_pick(stock_name):
#     return render_template('picks.html', one_pick= Stock.get_one({"id": stock_id}),user = User.get_by_id({'id':session['user_id']}))




