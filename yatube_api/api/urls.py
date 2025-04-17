from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from .views import PostViewSet, GroupViewSet, CommentViewSet

router = SimpleRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("group", GroupViewSet, basename="group")
router.register(
    r"posts/(?P<post_id>\d+)/comments",
    CommentViewSet, 
    basename="comments"
)


urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token),
    path("", include(router.urls)),
]
