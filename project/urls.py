from django.urls import path
from .views import ShareholderListView, ShareholderDetailView, ProjectListView,  ProjectDetailView

urlpatterns = [
    # Shareholder
    path('balance/', ShareholderListView.as_view(), name='balance_user'),
    path('create_shareholder/', ShareholderListView.as_view(), name='create_shareholder'),
    path('delete_shareholder/<int:pk>/', ShareholderDetailView.as_view(), name='delete_shareholder'),
    # Project
    path('list/', ProjectListView.as_view(), name='list_project'),
    path('create/', ProjectListView.as_view(), name='create_project'),
    path('delete/<int:pk>/', ProjectDetailView.as_view(), name='delete_project'),
    path('detail/<int:pk>/', ProjectDetailView.as_view(), name='detail_project'),
    path('update/<int:pk>/', ProjectDetailView.as_view(), name='update_project'),
]
