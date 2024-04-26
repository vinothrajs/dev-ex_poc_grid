# def custom_permissions(request):
#     user_permissions = []
#     if request.user.is_authenticated:
#         # Assuming you have a custom user model with a `get_permissions()` method
#         user_permissions = request.user.get_permissions()
#     return {"user_permissions": user_permissions}
