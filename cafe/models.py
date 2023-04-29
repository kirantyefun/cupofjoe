from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cafe(models.Model):
    """
    Represents a cafe in the system with its name, description, and owner.

    Attributes:
        name (str): The name of the cafe.
        description (str, optional): A short bio of the cafe. Defaults to None.
        owner (User): The owner of the cafe.

    Methods:
    __str__(): Returns a string representation of the cafe.

    """

    name = models.CharField(verbose_name="Name of the cafe", max_length=64)
    description = models.TextField(verbose_name="Short bio of the cafe", blank=True, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cafe')

    def __str__(self) -> str:
        return f"<Cafe: {self.name}>"
    
    @property
    def menu(self):
        """
        Returns:
            QuerySet: The menu of the cafe.
        """
        return self.menu_items.all()
    

class MenuItem(models.Model):
    """
    Represents a menu item in the system with its name, ingredients, description, price, cafe, and active status.

    Attributes:
        name (str): The name of the menu item.
        ingredients (str, optional): The ingredients used in the menu item. Defaults to None.
        description (str, optional): A short description of the menu item. Defaults to None.
        price (float): The price of the menu item.
        cafe (Cafe): The cafe that the menu item belongs to.
        active (bool): The active status of the menu item.

    Methods:
    __str__(): Returns a string representation of the menu item.

    """
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
    """
    Represents an order in the system with its user, cafe, date_ordered, active status, and additional instructions.

    Attributes:
        user (User): The user who placed the order.
        cafe (Cafe): The cafe where the order was placed.
        date_ordered (datetime): The date and time the order was placed.
        active (bool): The active status of the order.
        additional_instructions (str, optional): Additional instructions for the order. Defaults to None.

    Methods:
    __str__(): Returns a string representation of the order.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='orders')
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, null=True, related_name='orders')
    date_ordered = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    additional_instructions = models.TextField(blank=True, null=True)
    # order_placed = models.DateTimeField(verbose_name='Order Placed Datetime')

    def __str__(self):
        return f"{self.user.username} - {self.cafe} - {self.date_ordered.strftime('%Y-%m-%d %H:%M:%S')}"


class OrderItem(models.Model):
    """
    Represents an item in an order.

    Attributes:
        item (ForeignKey): A foreign key to the MenuItem object that this order item represents.
        order (ForeignKey): A foreign key to the Order object that this order item belongs to.
        quantity (PositiveIntegerField): The quantity of the menu item that was ordered.

    Methods:
        __str__(): Returns a string representation of the order item.

    """
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(verbose_name='quantity of item')

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"