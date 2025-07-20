from rest_framework import routers
from chats import views

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet)
router.register(r'conversation', views.ConversationViewSet)
