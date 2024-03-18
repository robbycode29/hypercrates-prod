from rest_framework import permissions

class IsGeneralManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='General Manager').exists()

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Doctor').exists() or request.user.groups.filter(name='General Manager').exists()

class IsAssistant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Assistant').exists() or request.user.groups.filter(name='General Manager').exists()
    

## Testing password hashing
    
# from django.contrib.auth.hashers import make_password, check_password

# password = make_password('pass3')
# print(password)

# is_match = check_password('pass2', 'pbkdf2_sha256$600000$nc513OzSAv9X4zF8s9rqJm$Wbs+NstUGd2R+/XquHqu/1NVCBtKbZQuF4shbZWiVwc=')
# print(is_match)