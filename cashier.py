

def vailidate_item (item_name,quantity):
    import sqlite3 as sql
    dp=sql.connect('database.db')
    cr=dp.cursor()
    cr.execute("SELECT quantity from items WHERE item_name=?",(item_name,))
    result=cr.fetchone()
    dp.close()
    if result and result[0]>=quantity:
        return True
    return False

def add_item_to_cart(cart, item, quantity):
    if not vailidate_item(item,quantity):   
        raise ValueError("Item not available in sufficient quantity")
    if item not in cart:
        cart[item] = 0
    cart[item] += quantity
    
    return cart
def remove_item_from_cart(cart, item, quantity):
    if item in cart:
        cart[item] -= quantity
        if cart[item] <= 0:
            del cart[item]
    return cart

def calculate_total(cart): 
    import sqlite3 as sql
    total = 0
    dp=sql.connect('database.db')
    cr=dp.cursor()
    for item, quantity in cart.items():
        cr.execute("SELECT price from items WHERE item_name=?",(item,))
        result=cr.fetchone()
        if result:
            price = result[0]
            total += price * quantity

        cr.execute("UPDATE items SET quantity = quantity - ? WHERE item_name = ?", (quantity, item))
        cr.execute("INSERT INTO sales (item_name, quantity, total_price) VALUES (?, ?, ?)", (item, quantity, price * quantity))
    dp.commit()
    dp.close()

    return total
