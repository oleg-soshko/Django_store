from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "quantity", "category", "draft"]


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image"]


admin.site.register(models.Category)
admin.site.register(models.Order)
admin.site.register(models.OrderDetails)
admin.site.register(models.ProductReview)
admin.site.register(models.OrderReview)
admin.site.register(models.RatingStars)
admin.site.register(models.Rating)
