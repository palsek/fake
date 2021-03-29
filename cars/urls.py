from django.conf.urls import include, url
from django.urls import path, re_path

from cars.views_api import get_user_cars_api, add_car_api, edit_car_api, get_car_vin_details_api, delete_car_api, add_service_api, get_car_services_api, edit_service_api, delete_service_api

app_name = 'cars'

urlpatterns = [

    #path("car_list_api", CarList.as_view(), name='car-list-api'),
    
    re_path(r"get_user_cars_api", get_user_cars_api),
    re_path(r"add_car_api", add_car_api),
    re_path(r"edit_car_api", edit_car_api),
    #re_path(r"get_car_vin_details_api/<int:car_id>", get_car_vin_details_api),
    path(r"get_car_vin_details_api/<int:car_id>", get_car_vin_details_api),
    path(r"delete_car_api/<int:car_id>", delete_car_api),
    re_path(r"add_service_api", add_service_api),
    path(r"get_car_services_api/<int:car_id>", get_car_services_api),
    re_path(r"edit_service_api", edit_service_api),
    path(r"delete_service_api/<int:service_id>", delete_service_api),

]