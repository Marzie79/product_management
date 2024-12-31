import datetime

from django.conf import settings
from django.db import models

from products.managers import (ProductManager, AllProductManager)


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        help_text='The name of the product.'
    )
    quantity = models.PositiveIntegerField(
        help_text='The quantity of the product available in stock.'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='The total price of the product (e.g., in USD).'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        help_text='The user who owns this product.'
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text='Indicates whether the product is deleted.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='The date and time when the product was created.'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='The date and time when the product was last updated.'
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date and time when the product was deleted.'
    )

    objects = ProductManager()
    all_objects = AllProductManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def delete(self, force_delete=False, *args, **kwargs):
        """Soft delete the product if force_delete is not True."""
        if force_delete:
            super().delete(*args, **kwargs)
        else:
            self.is_deleted = True
            self.deleted_at = datetime.datetime.now()
            self.save(force_update=True)
