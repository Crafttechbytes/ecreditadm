from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('personal_details/', views.personal_details, name='personal_details'),
    path('documents_approve/', views.documents_approve, name='documents_approve'),
    path('loan-requests/', views.loan_requests, name='loan_requests'),
    path('payment_details/', views.payment_details, name='payment_details'),
    path('login/', views.user_login, name='login'),
    path('upload_task_data', views.upload_task_data, name='upload_task_data'),
    path('messages/', views.messages, name='messages'),
    path('upload_image_to_storage', views.upload_image_to_storage, name='upload_image_to_storage'),
    path('auth-email/', views.auth_email, name='auth-email'),
    path('history-activities', views.recent_activities, name='history_activities'),
    path('transaction-history', views.transaction_history, name='transaction-history'),
    path('tasks_attempts', views.tasks_attempt_stats, name='tasks_attempts'),
    path('promo-codes', views.promo_code, name='promo-codes'),
    path('promo_code_update', views.promo_code_update, name='promo_code_update'),
    path("notifications/<str:uid>/", views.notifications_send, name='notifications'),
    path('delete_notification', views.delete_notification, name='delete_notification'),
    path('clicks_add', views.clicks_add, name='clicks_add'),
    path('add_faq_get', views.add_faq_get, name='add_faq_get'),
    path('sms-view', views.sms_view, name='sms_view'),
    path('mobile-contacts', views.contact_view, name='mobile-contacts'),
    path('version-check', views.version_check, name='version-check'),
    path('social-links-update', views.social_links_update, name='social-links-update'),
    path('settings-links', views.settings_links, name='settings-links')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
