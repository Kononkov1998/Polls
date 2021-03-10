import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework.authtoken import views

from polls.viewsets import PollViewSet, QuestionViewSet, AnswerViewSet, UserPollViewSet, UserAnswerViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Polling API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register('polls', PollViewSet)
router.register('questions', QuestionViewSet)
router.register('answers', AnswerViewSet)
router.register('user_polls', UserPollViewSet)
router.register('user_answers', UserAnswerViewSet)

urlpatterns = [
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('login/', views.obtain_auth_token),
    path('debug/', include(debug_toolbar.urls)),
]

urlpatterns += router.urls
