from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # remove this
    # is_superuser = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_permissions(self):
        # Your custom logic to retrieve permissions for the user
        # For example, you might want to return a queryset of permissions related to this user
        # This method should return a queryset of Permission objects
        # This is just a placeholder, you need to implement this according to your requirements
        return True

    class Meta:
        managed = True


# class Role(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     descs = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         managed = False


# # class Permission(models.Model):
# #     name = models.CharField(max_length=100, unique=True)
# #     desc = models.TextField(max_length=100 ,null=True)
# #     functionname = models.CharField(max_length=100 ,null=True)
# #     def __str__(self):
# #         return self.name
# #     class Meta:
# #             managed = True


# class RolePermission(models.Model):
#     role_id = models.IntegerField()
#     permission_id = models.IntegerField()

#     class Meta:
#         managed = False


# class permissiosnDummy(models.Model):
#     class Meta:
#         managed = False  # No database table creation or deletion  \
#         # operations will be performed for this model.

#         default_permissions = ()  # disable "add", "change", "delete"
#         # and "view" default permissions

#         permissions = (
#             ("order Management", "Order Management"),
#             ("invoice management", "Invocie Managemnt "),
#         )


# class demo(models.Model):
#     name = models.IntegerField()
#     nam2 = models.IntegerField()
#     name3 = models.IntegerField(null=True, db_index=True)


# class demo2(models.Model):
#     name = models.IntegerField()
#     nam2 = models.IntegerField()
#     nam3 = models.IntegerField()

#     class Meta:
#         managed = False


# from django.contrib.auth.models import Group


# class CustomGroup(Group):
#     description = models.CharField(max_length=255, blank=True, null=True)
#     # Add more custom fields as needed

#     class Meta:
#         verbose_name = "Custom Group"
#         verbose_name_plural = "Custom Groups"


# from django.contrib.auth.models import Permission


# class CustomPermission(Permission):
#     # Add custom fields as needed
#     description = models.CharField(max_length=255)

#     class Meta:
#         verbose_name = "Custom Permission"
#         verbose_name_plural = "Custom Permissions"


# class CustomPermission2(models.Model):
#     permission = models.OneToOneField(
#         Permission, on_delete=models.CASCADE, related_name="custom_permission"
#     )
#     description = models.CharField(max_length=255)

#     class Meta:
#         verbose_name = "Custom Permission2"
#         verbose_name_plural = "Custom Permissions2"


# class dummymodel(models.Model):
#     class Meta:
#         managed = True  # No database table creation or deletion  \
#         # operations will be performed for this model.

#         default_permissions = ()  # disable "add", "change", "delete"
#         # and "view" default permissions

#         permissions = (
#             ("order Management", "Order Management"),
#             ("invoice management", "Invocie Managemnt "),
#         )


# class hello(models.Model):
#     class Meta:
#         managed = True  # No database table creation or deletion  \
#         # operations will be performed for this model.

#         default_permissions = ()  # disable "add", "change", "delete"
#         # and "view" default permissions

#         permissions = (("hello_add", "hello Management"),)

# # class order(models.Model):
# #     permission = models.OneToOneField(
# #         Permission, on_delete=models.CASCADE, related_name="custom_permission"
# #     )
# #     description = models.CharField(max_length=255)

# #     class Meta:
# #         verbose_name = "Custom Permission2"
# #         verbose_name_plural = "Custom Permissions2"


# from django.db import models

# class Author(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()

#     def __str__(self):
#         return self.name
#     class Meta:
#         managed = False

# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)


#     def __str__(self):
#         return self.title
#     class Meta:
#         managed = True

# class Post(models.Model):
#     name = models.CharField(max_length=100)
#     body = models.EmailField()

#     def __str__(self):
#         return self.name
#     class Meta:
#         managed = False
# class Comments(models.Model):
#     comment = models.CharField(max_length=200)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)


#     def __str__(self):
#         return self.title
#     class Meta:
#         managed = False


# from django.db import models

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()

#     def __str__(self):
#         return self.name

# class Skill(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class StudentSkill(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.PROTECT)
#     skill = models.ForeignKey(Skill, on_delete=models.PROTECT)

#     def __str__(self):
#         return f"{self.student.name} - {self.skill.name}"

# from django.db import models

# class Order(models.Model):
#     order_number = models.CharField(max_length=100)
#     date_ordered = models.DateField()
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"Order #{self.order_number}"

# class OrderDetail(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, db_constraint=False)
#     product_name = models.CharField(max_length=200)
#     quantity = models.IntegerField()
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"Order Detail: {self.product_name} (Order: {self.order.order_number})"
# from django.db.models.signals import post_delete
# from django.dispatch import receiver
# @receiver(post_delete, sender=OrderDetail)
# def my_model_post_delete_handler(sender, instance, **kwargs):
#     # Perform actions after MyModel instance is deleted
#     print(f"MyModel instance {instance.pk} has been deleted.")

# from django.db import models

# class Parent(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Child(models.Model):
#     name = models.CharField(max_length=100)
#     parent_id = models.IntegerField(db_index=True)

#     def __str__(self):
#         return self.name

# from simple_history.models import HistoricalRecords

# class Choice(models.Model):
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#     history = HistoricalRecords()

# ## Model Definition
# Managed_MODEL = True
# REMOVE_DEFAULT_PERMISSIONS = ()
# class samplec(models.Model):
#     name = models.CharField(max_length=200)
#     number = models.IntegerField(default=0)
#     history = HistoricalRecords()
#     class Meta:
#         managed = Managed_MODEL
#         default_permissions = REMOVE_DEFAULT_PERMISSIONS


# from django.db import models
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.fields import GenericRelation


# class AppPermission(models.Model):
#     name = models.CharField(max_length=100)
#     codename = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name

# class AppRole(models.Model):
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name

# class AppRolePermission(models.Model):
#     role = models.ForeignKey(AppRole, on_delete=models.CASCADE)
#     permission = models.ForeignKey(AppPermission, on_delete=models.CASCADE)
#     # def __str__(self):
#     #     return self.role

# class AppUserRole(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     role = models.ForeignKey(AppRole, on_delete=models.CASCADE)
#     # def __str__(self):
#     #     return self.user

# class AppPage(models.Model):
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name

# class AppPagePermission(models.Model):
#     page = models.ForeignKey(AppPage, on_delete=models.CASCADE)
#     permission = models.ForeignKey(AppPermission, on_delete=models.CASCADE)
#     # def __str__(self):
#     #     return self.page


# from django.db import models

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     inventory = models.IntegerField(default=0)
#     cost = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


from django.db import models

class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    coupon_code = models.CharField(max_length=100)
    effective_from = models.DateTimeField()
    effective_till = models.DateTimeField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.coupon_code
