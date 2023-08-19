import json
import random
from django.conf import settings
from .models import wagtail_all_in_one_accessibility
from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel
from django.forms.widgets import RadioSelect,HiddenInput

from django.utils.html import format_html



def admin_AIOA(request):
    aioa_NOTE = ''
    aioa_BaseScript = ''
    for a in wagtail_all_in_one_accessibility.objects.all():
        print(a.aioa_icon_type,"-------------",a.aioa_icon_size)
        
        a_LK =a.aioa_license_Key.replace(']','').replace('[','').replace("'","")
        a_CC =a.aioa_color_code.replace(']','').replace('[','').replace("'","")
        a_AP =str(a.aioa_place).replace(']','').replace('[','').replace("'","")
        MOBILE_SIZE =str(a.aioa_mobile).replace(']','').replace('[','').replace("'","")
        ICON = str(a.aioa_icon_type).replace(']','').replace('[','').replace("'","")
        SIZE = str(a.aioa_icon_size).replace(']','').replace('[','').replace("'","")
        
        # print(a_LK)
        # print(a_CC)
        # print(a_AP)
        print(MOBILE_SIZE,'MOBILE_SIZE')
        print(ICON,'ICON')
        print(SIZE,'SIZE')
        
        if a_LK == "":
            print(a_LK,"---------------------------------")
            wagtail_all_in_one_accessibility._meta.get_field('aioa_license_Key').help_text = mark_safe("<span class='validate_pro'><p>You are currently using Free version which have limited features. </br>Please <a href='https://www.skynettechnologies.com/add-ons/product/all-in-one-accessibility/'>purchase</a> License Key for additional features on the ADA Widget</p></span>")
            
            aioa_BaseScript = 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode='+ a_CC + '&token=' +a_LK+'&t='+str(random.randint(0,999999))+'&position=' + a_AP+'.'+''+'.'+''+'.'+''

            
            wagtail_all_in_one_accessibility._meta.get_field('aioa_mobile').choices = None
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_type').choices = None
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_size').choices = None
            
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_type').verbose_name = ''
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_size').verbose_name = ''
            wagtail_all_in_one_accessibility._meta.get_field('aioa_mobile').verbose_name = ''
            
            wagtail_all_in_one_accessibility._meta.get_field('aioa_mobile').widget = HiddenInput
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_type').widget = HiddenInput
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_size').widget = HiddenInput
            wagtail_all_in_one_accessibility._meta.get_field('aioa_text').widget = HiddenInput
            
            wagtail_all_in_one_accessibility._meta.get_field('aioa_mobile').blank = True
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_type').blank = True
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_size').blank = True

        else:
            aioa_BaseScript = 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode='+ a_CC + '&token=' +a_LK+'&t='+str(random.randint(0,999999))+'&position=' + a_AP+'.'+ICON+'.'+SIZE+'.'+MOBILE_SIZE
            print(aioa_BaseScript,"@@@@@@@@@@@@@@@@@@")
            wagtail_all_in_one_accessibility._meta.get_field('aioa_license_Key').help_text = ""
            
            wagtail_all_in_one_accessibility._meta.get_field('aioa_mobile').widget = HiddenInput
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_type').widget = RadioSelect
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_size').widget = RadioSelect
            wagtail_all_in_one_accessibility._meta.get_field('aioa_text').widget = HiddenInput
            
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_type').verbose_name = 'Icon Type'
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_size').verbose_name = 'Icon Size For Desktop'
            wagtail_all_in_one_accessibility._meta.get_field('aioa_mobile').verbose_name = ''
            
            
            wagtail_all_in_one_accessibility._meta.get_field('aioa_mobile').blank = False
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_type').blank = False
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_size').blank = False

            value_i = ICON+".svg"
            print(value_i,"qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_size').choices = [('aioa-big-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="75" height="75" />',value_i)), ('aioa-medium-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="65" height="65" />',value_i)), ('aioa-default-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="55" height="55" />',value_i)), ('aioa-small-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="45" height="45" />',value_i)), ('aioa-extra-small-icon',format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="35" height="35"/>',value_i))]
            
            # wagtail_all_in_one_accessibility._meta.get_field('aioa_mobile').choices = [('aioa-big-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="75" height="75" />',value_i)), ('aioa-medium-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="65" height="65" />',value_i)), ('aioa-default-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="55" height="55" />',value_i)), ('aioa-small-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="45" height="45" />',value_i)), ('aioa-extra-small-icon',format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="35" height="35"/>',value_i))]
            
            wagtail_all_in_one_accessibility._meta.get_field('aioa_icon_type').choices = [('aioa-icon-type-1', format_html('<img src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-1.svg" width="65" height="65" />')), ('aioa-icon-type-2', format_html('<img src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-2.svg" width="65" height="65" />')), ('aioa-icon-type-3', format_html('<img src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-3.svg" width="65" height="65" />'))]
            
    print(aioa_BaseScript)


    return {'AIOA_URL': aioa_BaseScript}

