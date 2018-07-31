from sinventory import product as dbproduct

product = dbproduct.Product('8906017290026')
product_data = product.get_data()
print(product_data)