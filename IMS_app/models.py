class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    orderdate = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Order # {self.id} - {self.customer.name}"
    
    def total_amount(self):
        return sum(item.totalprice() for item in self.orderitem_set.all())
    
class Orderitem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def totalprice(self):
        return self.product.price * self.quantity 