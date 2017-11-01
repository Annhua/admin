from django.template.library import Library
from django.forms.boundfield import BoundField #打印item显示信息
from django.forms.models import ModelChoiceField
from django.forms.models import ModelMultipleChoiceField
from django.urls import reverse
from django.db.models.query import QuerySet
from qi.server.V1 import site
register=Library()


def xxxx(model_form_obj):
    for item in model_form_obj:
        #判断是否是外键，如果是外键就增加增加按钮
        # print(item.field)#<django.forms.models.ModelChoiceField object at 0x00000000043CB2E8>
        tpl={'has_popup':False,'item':item,'popup_url':None}
        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in site._registry:
            tpl['has_popup']=True
            #添加增加按钮，反向生成url
            model_class=item.field.queryset.model#<class 'app01.models.UserGroup'>,<class 'app01.models.Role'>
            model_table=model_class._meta.app_label
            model_user=model_class._meta.model_name
            url=reverse('{0}:{1}_{2}_add'.format(site.namespace,model_table,model_user))
            url = "{0}?_popup={1}".format(url, item.auto_id)
            tpl['popup_url']=url
            print(url)
        yield tpl

@register.inclusion_tag('ninbin/change_form.html')
def show_from(forms):

    return {'forms':xxxx(forms)}



