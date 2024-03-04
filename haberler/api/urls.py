from django.urls import path
from haberler.api import views as api_views

urlpatterns = [
    path("makaleler/", api_views.MakaleView.as_view(), name="makale"),
    path(
        "makaleler/<int:pk>/",
        api_views.MakaleDetailView.as_view(),
        name="makale-detay",
    ),
    path("gazeteci/", api_views.GazeteciView.as_view(), name="gazeteci"),
    path(
        "gazeteci/<int:pk>/",
        api_views.GazeteciDetailView.as_view(),
        name="gazeteci-detay",
    ),
]


## __ FUNCTIONS __ ##
# urlpatterns = [
#     path("makaleler/", api_views.makale_list_api_view, name="makale-listesi"),
#     path(
#         "makaleler/find-by-id/<int:id>",
#         api_views.makale_get_by_id_api_view,
#         name="makale-find-by-id",
#     ),
#     path(
#         "makaleler/patch-by-id/<int:id>",
#         api_views.makale_update_api_view,
#         name="makale-patch-by-id",
#     ),
#     path(
#         "makaleler/delete-by-id/<int:id>",
#         api_views.makale_delete_by_id_api_view,
#         name="makale-delete-by-id",
#     ),
#     path("makaleler/post", api_views.makale_create_api_view, name="makale-create"),
# ]
