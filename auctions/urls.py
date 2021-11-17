from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("auction/<int:auction_id>/comment", views.comments, name="comment"),
    path("auction/<int:auction_id>/bid", views.bids, name="bid"),
    path("categories", views.categories_list, name="categories"),
    path("categories/<str:category_name>", views.show_category, name="show_category"),
    path("watchlist/<int:user_id>/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("watchlist/delete/<int:watchlist_id>", views.watchlist_delete, name="watchlist_delete"),
    path("auction/<int:auction_id>/close", views.close, name="close")
]
