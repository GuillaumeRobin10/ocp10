from rest_framework.permissions import IsAuthenticated


def getuser(request):
    permission_classes = (IsAuthenticated,)
    user = request.user
    return user
