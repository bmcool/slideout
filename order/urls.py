from django.conf.urls.defaults import *

urlpatterns = patterns("order.views",
    url(r"^(?P<direction>up|down)/(?P<model_type_id>\d+)/(?P<model_id>\d+)/$", "admin_move_ordered_model", name="admin-move"),
)
