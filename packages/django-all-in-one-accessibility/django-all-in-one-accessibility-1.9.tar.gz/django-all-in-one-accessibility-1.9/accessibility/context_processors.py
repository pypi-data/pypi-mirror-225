import json
import random
from django.conf import settings
from .models import all_in_one_accessibility
from django.utils.html import format_html
from.admin import aioa_admin_form

def admin_AIOA(request):

    aioa_BaseScript = ''
    
    for a in all_in_one_accessibility.objects.all():
        # print(a.aioa_license_Key,"00000000000000000")
        
        a_LK =a.aioa_license_Key.replace(']','').replace('[','').replace("'","")
        a_CC =a.aioa_color_code.replace(']','').replace('[','').replace("'","")
        a_AP =str(a.aioa_place).replace(']','').replace('[','').replace("'","")
        icon_type = str(a.aioa_icon_type)
        ICON = icon_type.replace(']','').replace('[','').replace("'","")
        icon_size = str(a.aioa_icon_size)
        SIZE = icon_size.replace(']','').replace('[','').replace("'","")
     
      
        if a_LK == '':
            aioa_BaseScript = 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode='+ a_CC + '&token=' + a_LK+'&t='+str(random.randint(0,999999))+'&position=' + a_AP+'.'+''+'.'+''+'.'+''
            
        else:
            aioa_BaseScript = 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode='+ a_CC + '&token=' + a_LK+'&t='+str(random.randint(0,999999))+'&position=' + a_AP+'.'+ICON+'.'+SIZE
            format_icon = ICON.split(',')
            print(format_icon[0],"00000000000000000")
            value_i = format_icon[0]+".svg"
            
            all_in_one_accessibility._meta.get_field('aioa_icon_size').values = [('aioa-big-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="75" height="75" />',value_i)), ('aioa-medium-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="65" height="65" />',value_i)), ('aioa-default-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="55" height="55" />',value_i)), ('aioa-small-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="45" height="45" />',value_i)), ('aioa-extra-small-icon',format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="35" height="35"/>',value_i))]
            

    return {'AIOA_URL': aioa_BaseScript}

