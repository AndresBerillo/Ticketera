import os
from django.db import models
from django.contrib.auth.models import User
from .validators import validate_pdf_file,validate_image_file_extension

class Concert(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='concert_images/', null=True, blank=True, validators=[validate_image_file_extension])

    def __str__(self):
        return self.name


class Ticket(models.Model):
    concert = models.ForeignKey(Concert, related_name='tickets', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_sold = models.BooleanField(default=False)
    pdf_file = models.FileField(upload_to='tickets/', null=True, blank=True, validators=[validate_pdf_file])  # Aplica el validador

    def __str__(self):
        return f"Seat {self.seat_number} - {self.concert.name}"
    
    def save(self, *args, **kwargs):
        if self.pdf_file:
            # Obtener la extensión del archivo
            ext = os.path.splitext(self.pdf_file.name)[1]
            # Crear el nuevo nombre del archivo
            new_filename = f"{self.concert.name}_{self.seat_number}{ext}".replace(" ", "_")
            # Asignar el nuevo nombre al archivo
            self.pdf_file.name = new_filename
        super(Ticket, self).save(*args, **kwargs)


class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket, related_name='in_cart', blank=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"


class Transaction(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='sold_tickets', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Transaction {self.id} - Ticket {self.ticket.seat_number}"
