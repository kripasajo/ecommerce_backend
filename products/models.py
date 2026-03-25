#add custom manager to filter out deleted products and categories. This will allow us to easily get only the active products and categories without having to filter them manually every time we query the database.
from django.db import models

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


#base models for all the models in the products app to inherit from. This will have common fields like created_at and updated_at which will be automatically set when a model instance is created or updated. This will help us to keep track of when a product was created and last updated.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False) #is_deleted field to implement soft delete functionality. Instead of deleting a product from the database, we will set this field to True. This will allow us to keep the data in the database and restore it if needed.

    class Meta:
        abstract = True


#category model which will be used to categorize products. A category can have a parent category which will allow us to create a hierarchy of categories. For example, we can have a parent category called "Electronics" and child categories called "Mobile Phones", "Laptops", etc. This will help us to organize our products better and make it easier for users to find the products they are looking for.
class Category(BaseModel):
    name = models.CharField(max_length=255,unique=True) #name field is unique because we don't want to have duplicate category names in the database. This will help us to avoid confusion and maintain data integrity. For example, if we have two categories with the same name "Mobile Phones", it will be difficult for users to differentiate between them and it will also create issues when we want to filter products by category.
    slug = models.SlugField(unique=True) #slug field which will be used to create SEO friendly URLs for categories. For example, if we have a category called "Mobile Phones", the slug will be "mobile-phones". This will allow us to create URLs like "/categories/mobile-phones/" which will be more user-friendly and SEO friendly than URLs like "/categories/1/".

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    is_active = models.BooleanField(default=True) #is_active field to indicate whether a category is active or not. This will allow us to hide categories that are not active without deleting them from the database. This can be useful if we want to temporarily hide a category without losing the data associated with it.

    #  Managers
    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        indexes = [                     #indexes for slug and parent fields to improve query performance when filtering by these fields( faster queries when we have a large number of categories)
            models.Index(fields=['slug']),
            models.Index(fields=['parent']), #parent supports hierarchical queries to get all child categories of a parent category efficiently.
        ]
    
    #product model
from django.utils.text import slugify

class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True) #slug is unique because two prducts can have the same name but they will have different slugs. blank=True because we will generate the slug automatically in the save method if it is not provided.

    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  #on_delete is used because of category is deleted we don't want data to be lost
        related_name='products'
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True)

    # ✅ Managers
    objects = models.Manager()
    active_objects = ActiveManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['price']),
        ]

    