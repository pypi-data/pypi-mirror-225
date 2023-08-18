from django.db import models
from django import forms
from django.forms.widgets import RadioSelect,HiddenInput
from wagtail.admin.panels import FieldPanel
from django.utils.safestring import SafeString
from django.core.exceptions import ValidationError
from django.utils.html import format_html,escape
from django.utils.safestring import  mark_safe
aioa_SELECT_CHOICE = [('top_left','Top left'),
      ('top_center','Top Center'),
      ('top_right','Top Right'),
      ('middel_left','Middle left'),
      ('middel_right','Middle Right'),
      ('bottom_left','Bottom left'),
      ('bottom_center','Bottom Center'),
      ('bottom_right','Bottom Right')]
def validate_token(value):
    if value is not None:
        pass
    else:
        raise ValidationError("")
ROWS = (
    (1 ,''),
)
CHOICES = [('aioa-icon-type-1', format_html('<img src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-1.svg" width="65" height="65" />')), ('aioa-icon-type-2', format_html('<img src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-2.svg" width="65" height="65" />')), ('aioa-icon-type-3', format_html('<img src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-3.svg" width="65" height="65" />'))]
class wagtail_all_in_one_accessibility(models.Model):
    # icon_change =  mark_safe(SafeString('''<script>alert("hello")</script>'''))
    icon_change = mark_safe(SafeString('''    
    <script>
    const sizeOptions = document.querySelectorAll('input[name="aioa_icon_size"]');
    const sizeOptionsImg = document.querySelectorAll('.csticontype');
    const typeOptions = document.querySelectorAll('input[name="aioa_icon_type"]');
    typeOptions.forEach(option => {
        option.addEventListener("click", (event) => {
            sizeOptionsImg.forEach(option2 => {
                var ico_type = document.querySelector('input[name="aioa_icon_type"]:checked').value;
                option2.setAttribute("src", "https://skynettechnologies.com/sites/default/files/python/" + ico_type + ".svg");
            });
        });
    });
</script>
<style>

#id_aioa_icon_type,
#id_aioa_icon_size,
#id_aioa_mobile {
  display: flex;
  flex-wrap: wrap;
  margin-left: -12px;
  margin-right: -12px;
}
#id_aioa_icon_type > div,
#id_aioa_icon_size > div,
#id_aioa_mobile > div {
  width: 130px;
  height: 130px;
  margin-left: 12px;
  margin-right: 12px;
}
#id_aioa_icon_type > div label,
#id_aioa_icon_size > div label,
#id_aioa_mobile > div label {
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-color: #fff;
  outline: 4px solid #fff;
  outline-offset: -4px;
  border-radius: 10px;
}
#id_aioa_icon_type > div label img, #id_aioa_icon_size > div label img, #id_aioa_mobile > div label img {
  position: absolute;
}
#id_aioa_icon_type > div label input,
#id_aioa_icon_size > div label input,
#id_aioa_mobile > div label input {
  width: 100%;
  height: 100%;
  left: 50%;
  top: 50%;
  appearance: none;
  border-radius: 10px;
  transform: translate(-50%, -50%);
  margin-right: 0;
}
#id_aioa_icon_type > div label input::before,
#id_aioa_icon_size > div label input::before,
#id_aioa_mobile > div label input::before {
  content: none;
  display: none;
}
#id_aioa_icon_type > div label input:checked,
#id_aioa_icon_size > div label input:checked,
#id_aioa_mobile > div label input:checked {
  box-shadow: 0 0 0 3px #8bcd55;
}
#id_aioa_icon_type > div label:hover,
#id_aioa_icon_size > div label:hover,
#id_aioa_mobile > div label:hover,
#id_aioa_icon_type > div label input:hover,
#id_aioa_icon_size > div label input:hover,
#id_aioa_mobile > div label input:hover{
  cursor: pointer
}

</style>
<script>
      if(document.querySelector("#id_aioa_license_Key").value != ' ')
      {
          document.querySelector('section[id="panel-aioa_icon_type-section"]').style.display='block';
          document.querySelector('section[id="panel-aioa_icon_size-section"]').style.display='block';
          document.querySelector('h2[id="panel-aioa_icon_size-heading"]').style.display='block';
          document.querySelector('label[id="id_aioa_mobile-label"]').style.display='block';
          document.querySelector('button[aria-describedby="panel-aioa_icon_type-heading"]').style.display='block';
          document.querySelector('button[aria-describedby="panel-aioa_icon_size-heading"]').style.display='block';
          document.querySelector('button[aria-describedby="panel-aioa_mobile-heading"]').style.display='block';

      }
      else
      {
          document.querySelector('section[id="panel-aioa_icon_type-section"]').style.display='none';
          document.querySelector('section[id="panel-aioa_icon_size-section"]').style.display='none';
          document.querySelector('h2[id="panel-aioa_icon_size-heading"]').style.display='none';
          document.querySelector('label[id="id_aioa_mobile-label"]').style.display='none';
          document.querySelector('button[aria-describedby="panel-aioa_icon_type-heading"]').style.display='none';
          document.querySelector('button[aria-describedby="panel-aioa_icon_size-heading"]').style.display='none';
          document.querySelector('button[aria-describedby="panel-aioa_mobile-heading"]').style.display='none';

      }
      </script>
'''))
   
    value_i = "aioa-icon-type-1.svg"  
    
    CHOICES1 = [('aioa-big-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="75" height="75" />',value_i)), ('aioa-medium-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="65" height="65" />',value_i)), ('aioa-default-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="55" height="55" />',value_i)), ('aioa-small-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="45" height="45" />',value_i)), ('aioa-extra-small-icon',format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="35" height="35"/>',value_i))]
   
    aioa_license_Key = models.CharField(max_length=150,blank=True,validators=[validate_token],default=' ',verbose_name='License Key')
    
    aioa_color_code = models.CharField(max_length=50,blank=True,default=' ',verbose_name ='Hex color code',help_text='You can cutomize the ADA Widget color. For example: #FF5733')
    
    aioa_place = models.CharField(max_length=100,blank=True,choices=aioa_SELECT_CHOICE,default=('bottom_right','Bottom Right'),verbose_name='Where would you like to place the accessibility icon on your site')
    
    aioa_icon_type = models.CharField(max_length=1000,choices=CHOICES,default=('aioa-icon-type-1', format_html('<img src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-1.svg" width="65" height="65" />')),verbose_name="Icon Type")
    
    aioa_icon_size = models.CharField(max_length=1000,blank=True,verbose_name="Icon Size For Desktop",default=('aioa-medium-icon', format_html('<img src="https://skynettechnologies.com/sites/default/files/python/{}" width="65" height="65" />',value_i))) 
    
    aioa_mobile = models.CharField(max_length=1000,blank=True,verbose_name="Icon Size For Mobile",default=('aioa-medium-icon', format_html('<img src="https://skynettechnologies.com/sites/default/files/python/{}" width="65" height="65" />',value_i))) 
    
    
    
    aioa_text = models.CharField(max_length=150,blank=True, help_text=icon_change,verbose_name="")
    
    panels = [
    FieldPanel('aioa_license_Key'),
    FieldPanel('aioa_color_code'),
    FieldPanel('aioa_place'),
    FieldPanel('aioa_icon_type',widget=RadioSelect),
    FieldPanel('aioa_icon_size',widget=RadioSelect),
    FieldPanel('aioa_mobile',widget=HiddenInput),
    FieldPanel('aioa_text',widget=HiddenInput),
]


    def __str__(self):    


        return '{}, {}, {}'.format(self.aioa_place,self.aioa_color_code, self.aioa_license_Key)
    
    class Meta:
        verbose_name = 'All in One Accessibility Settings'
        verbose_name_plural = 'All in One Accessibility Settings'
        
 

