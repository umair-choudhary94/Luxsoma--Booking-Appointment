from django.urls import path
from .views import *

urlpatterns = [
    path("",index),
    path('register/',sign_up , name='sign_up'),
    path('profile/',profile , name='profile'),
    path('login/',user_login, name='login'),
    path('logout/',user_logout, name='logout'),
    
    path("services/",services),
    path("gallery/",gallery),
    path("services/category/<str:category>/",subcategories),
    path("services/category/info/<str:title>/",subcategoriesinfo),
    path('contact/', contact_view, name='contact'),
    path('faq/', faq_view, name='faq'),
    path("book-appointment/",book_appointment),
    path('services-json/', services_json, name='services_json'),
    path('make-appointment/', make_appointment, name='make_appointment'),
    path('success/<int:id>/', SuccessView, name='success'),
    path("getcard/",credit_card_view,name="getcard"),
    path('store_stripe_token/', store_stripe_token, name='store_stripe_token'),
    path("process_payment/<int:id>/",process_payment,name="process_payment"),
    path("cancel_appointment/<int:id>/",cancel_appointment),

]
