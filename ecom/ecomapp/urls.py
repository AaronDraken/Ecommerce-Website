from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home" ),
    path('details/<int:pk>', views.Details.as_view(), name="details" ),
    path('mob/', views.filter_mob, name="mob" ),
    path('lap/', views.filter_lap, name="lap" ),
    path('tv/', views.filter_tv, name="tv" ),
    path('filter/', views.range, name="filter" ),
    path('sort/', views.sortProds, name="sort" ),
    path('search/', views.search, name="search" ),
    path('addToCart/<int:pk>', views.addToCart, name="addToCart" ),
    path('buy/<int:pk>', views.buy, name="buy" ),
    path('delete/<int:pk>', views.deleteFromCart, name="delete" ),
    path('Cart/', views.cart, name="Cart" ),
    path('Address/', views.genAdd, name="Address" ),
    path('addAddress/', views.addAdd, name="addAddress" ),
    path('updateAddress/<int:id>', views.updateAdd, name="updateAddress" ),
    path('deleteAddress/<int:id>', views.delAdd, name="deleteAddress" ),
    path('Orders/', views.viewOrder, name="Orders" ),
    path('placeOrder/', views.placeOrder, name="placeOrder" ),
    path('payment/', views.makePayment, name="payment" ),
    path('updateQty/<int:btn>/<int:pk>', views.updateQty, name="updateQty" ),
    path('Register/', views.register, name="register" ),
    path('login/', views.loginUser, name="login" ),
    path('logout/', views.logoutUser, name="logout" ),
    path('sendMail/', views.sendUserMail, name="sendMail" ),
]