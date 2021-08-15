from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('signup/', views.signup),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/', views.projet_get_info_or_add_a_new_project),
    path("projects/<int:pk_projet>/", views.uniqueprojet),
    path("projects/<int:pk_projet>/users", views.projetcontributor),
    path("projects/<int:pk_projet>/users/<int:pk_user>", views.deleteuser),
    path("projects/<int:pk_projet>/issues/", views.issues),
    path("projects/<int:pk_projet>/issues/<int:pk_issues>", views.editissues),
    path("projects/<int:pk_projet>/issues/<int:pk_issues>/comments", views.comments),
    path("projects/<int:pk_projet>/issues/<int:pk_issues>/comments/<int:pk_comments>", views.editcomments),

]

urlpatterns = format_suffix_patterns(urlpatterns)
