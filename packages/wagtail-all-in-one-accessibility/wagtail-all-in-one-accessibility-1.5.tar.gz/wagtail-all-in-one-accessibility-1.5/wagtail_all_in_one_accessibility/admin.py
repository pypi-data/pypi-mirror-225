from urllib.parse import urlparse
import requests
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.helpers import ButtonHelper

from .models import wagtail_all_in_one_accessibility


class WagtailHomePageCarouselButtonHelper(ButtonHelper):
    def add_button(self,request, classnames_add=None, classnames_exclude=None):
        
        retVal = super().add_button(request)
        print(retVal)
        # set add permission to False, if object already exists
        if retVal and wagtail_all_in_one_accessibility.objects.exists():
            retVal = False
        return None
    
    # def save_model(self, request, obj, form, change):
    #     for data in wagtail_all_in_one_accessibility.objects.all():
    #         domain = urlparse(request.build_absolute_uri())
    #         domain_url = domain.scheme +'://'+domain.netloc
    #         print(domain_url)
    #         url = "https://ada.skynettechnologies.us/api/widget-setting-update-platform"

    #         payload = {'u': domain_url,
    #         'widget_position': data.aioa_place,
    #         'widget_color_code': data.aioa_color_code,
    #         'widget_icon_type': data.aioa_icon_type,
    #         'widget_icon_size': data.aioa_icon_size}
    #         files=[

    #         ]
    #         headers = {}

    #         response = requests.request("POST", url, headers=headers, data=payload, files=files)

    #         print(response.text)
        # super().save_model(request, obj, form, change)

class ExampleModelAdmin(ModelAdmin):
    # form = PassengerForm
    model = wagtail_all_in_one_accessibility
    list_display = ('aioa_license_Key', 'aioa_color_code', 'aioa_place')
    list_display_links  = ('aioa_license_Key', 'aioa_color_code', 'aioa_place')
    add_to_settings_menu = False 
    exclude_from_explorer = False 
    exclude = ('aioa_icon_type')
    button_helper_class = WagtailHomePageCarouselButtonHelper

    # def get_fields(self, request, obj=None):
    #     for data in wagtail_all_in_one_accessibility.objects.all():
    #         if data.aioa_license_Key != '':
    #             print("dataaaaaaaa")
    #             return ('aioa_license_Key', 'aioa_color_code', 'aioa_place','aioa_icon_type','aioa_icon_size')
    #         return ('aioa_license_Key', 'aioa_color_code', 'aioa_place')

        
modeladmin_register(ExampleModelAdmin)
