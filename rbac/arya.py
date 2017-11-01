from arya.service import sites
from . import models
from django.shortcuts import render,HttpResponse,redirect
from django.urls.resolvers import RegexURLPattern
import json
from django.forms import ModelForm
from django.forms import fields
def get_all_url(patterns,prev,is_first=False, result=[]):
    if is_first:
        result.clear()
    for item in patterns:
        v = item._regex.strip("^$")
        if isinstance(item, RegexURLPattern):
            val=prev+v
            result.append((val,val))
        else:
            get_all_url(item.urlconf_name, prev + v)

    return result


sites.site.register(models.User)
sites.site.register(models.Role)

class Modelforms(ModelForm):
    url=fields.ChoiceField()
    class Meta:
        model=models.Permission
        fields='__all__'
    def __init__(self,*args,**kwargs):
        super(Modelforms,self).__init__(*args,**kwargs)
        from pro_crm.urls import urlpatterns
        self.fields['url'].choices=get_all_url(urlpatterns, '/', True)

class PermissionConfig(sites.AryaConfig):

    def dabo(self, obj=None, is_header=False):
        if is_header:
            return '其他'
        return obj.caption + "-大波"

    list_display = ['caption','url',dabo,'menu']
    model_form = Modelforms
    #
    # def get_show_list_display(self):
    #     li = []
    #     li.extend(self.list_display)
    #     return li
    #
    # def add_view(self, request, *args, **kwargs):
    #     """
    #     添加页面
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     from pro_crm.urls import urlpatterns
    #     url=get_all_url(urlpatterns, prev='/', is_first=True)
    #     model_form_cls = self.get_model_form_class()
    #     popup_id = request.GET.get(self.popup_key)
    #     if request.method == 'GET':
    #         form = model_form_cls()
    #         return render(request, "permission_add_popup.html" if popup_id else "permission_add.html", {'form': form,'url_list':url})
    #     elif request.method == "POST":
    #         form = model_form_cls(data=request.POST, files=request.FILES)
    #         if form.is_valid():
    #             obj = self.save(form, True)
    #             if obj:
    #                 if popup_id:
    #                     context = {'pk': obj.pk, 'value': str(obj), 'popup_id': popup_id}
    #                     return render(request, 'arya/popup_response.html', {"popup_response_data": json.dumps(context)})
    #                 else:
    #                     return redirect(self.changelist_url_params)
    #         return render(request, "permission_add_popup.html" if popup_id else "permission_add.html", {'form': form,'url_list':url})



sites.site.register(models.Permission,PermissionConfig)
sites.site.register(models.Menu)