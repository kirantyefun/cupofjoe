from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cafe(models.Model):
    name = models.CharField(verbose_name="Name of the cafe", max_length=64)
    description = models.TextField(verbose_name="Short bio of the cafe", blank=True, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cafe')

    def __str__(self) -> str:
        return f"<Cafe: {self.name}>"
    
    @property
    def menu(self):
        return self.menu_items.all()
    

class MenuItem(models.Model):
    name = models.CharField(verbose_name="Menu Item name", max_length=64)
    ingredients = models.CharField(
        verbose_name="Ingredients used", max_length=256, blank=True, null=True
    )
    description = models.TextField(
        verbose_name="Short description of menu item", blank=True, null=True
    )
    price = models.FloatField(verbose_name="Price")
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='menu_items')
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['name', 'cafe']

    def __str__(self) -> str:
        return f"<MenuItem: {self.name}>"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='orders')
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, null=True, related_name='orders')
    date_ordered = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    additional_instructions = models.TextField(blank=True, null=True)
    # order_placed = models.DateTimeField(verbose_name='Order Placed Datetime')

    def __str__(self):
        return f"{self.user.username} - {self.cafe} - {self.date_ordered.strftime('%Y-%m-%d %H:%M:%S')}"


class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(verbose_name='quantity of item')

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"