from django.shortcuts import HttpResponse,render,redirect
from django.conf.urls import url,include
from types import FunctionType
from django.urls import reverse
from django.utils.safestring import mark_safe
from utils.page import Pagination
from django.forms import ModelForm
import copy
from django.http import QueryDict
from django.db.models.fields.related import RelatedField
import functools

class Option(object):
    def __init__(self,name_or_func,is_multi=False):
        self.name_or_func=name_or_func
        self.is_multi=is_multi

    @property
    def name(self):
        if isinstance(self.name_or_func,FunctionType):
            return self.name_or_func.__name__
        else:
            return self.name_or_func
    # @property
    # def name_or_func(self):
    #     if isinstance(self.name_or_func,FunctionType):
    #         return True


class RowItems(object):
    def __init__(self,data_list,option,params):
        self.option=option
        self.data_list=data_list
        self.params=copy.deepcopy(params)
        self.params._mutable=True

    def __iter__(self):

        #取到选中值：
        list_play=self.params.getlist(self.option.name)#取出来所有的选择数据
        print('//////',list_play)

        #判断是否能取到值，对全部按钮就能编辑
        if list_play:
            self.params.pop(self.option.name)
            url=self.params.urlencode()
            tpl = "<a  href='?%s'>全部</a>" % (url,)
        else:
            url=self.params.urlencode()
            tpl = "<a  class='active' href='?%s'>全部</a>" % (url, )
        yield mark_safe(tpl)

        for item in self.data_list:
            params = copy.deepcopy(self.params)
            text=str(item)
            pk=str(item.pk)
            if self.option.is_multi:
                temp=[]
                temp.extend(list_play)
                temp.append(pk)
                params.setlist(self.option.name,temp)
                print('00000000000000',self.option.name)
                url=params.urlencode()
                if pk in list_play:
                    tpl = "<a class='active' href='?%s'>%s</a>" % (url, text)
                else:
                    tpl = "<a href='?%s'>%s</a>" % (url, text)
                yield mark_safe(tpl)
            else:
                params[self.option.name] = pk
                # if list_play:
                #     if list_play[0] == pk:
                #         params.pop(self.option.name)
                #         params[self.option.name]=pk
                url=params.urlencode()
                if pk in list_play:
                    tpl = "<a class='active' href='?%s'>%s</a>" % (url, text)
                else:
                    tpl = "<a href='?%s'>%s</a>" % (url, text)

                yield mark_safe(tpl)



class Changelist(object):
    def __init__(self,userinfo_obj,model_config_obj):
        self.userinfo_obj=userinfo_obj
        self.list_display=model_config_obj.get_list_display()
        self.model_config_obj=model_config_obj
        self.delter_get=model_config_obj.delter_get()
        self.list_filter=model_config_obj.get_list_filter()
        # print(self.list_filter)
        # def xxxxxx(model_config_obj):
        #     for item in model_config_obj.delter_get():
        #         yield (item.__name__,item.short_desc)
        # self.delter_get=xxxxxx(self.model_config_obj)


        #取出总的数据数量
        total_item_count=userinfo_obj.count()
        # 取出总的数据数量
        #取出单签页码
        current_page=model_config_obj.request.GET.get('page')
        #当前的起始页和结束页
        # user_list =userinfo_obj[page_obj.start:page_obj.end]
        #当前的ur；
        base_url=model_config_obj.request.path_info
        #设置url传入后面的
        # print(model_config_obj.request.GET)#<QueryDict: {'p': ['1'], 'id': ['9']}>
        request_get=copy.deepcopy(model_config_obj.request.GET)
        #设置这个为true可以更改字段
        request_get._mutable=True
        request_get['page']=1
        # print(request_get) <QueryDict: {'page': [5], 'id': ['3']}>
        # print(request_get.urlencode()) page=5&id=3

        page=Pagination(
            current_page=model_config_obj.request.GET.get('page'),
            total_item_count=userinfo_obj.count(),
            base_url=model_config_obj.request.path_info,
            request_params=request_get

        )

        self.userinfo_obj=userinfo_obj[page.start:page.end]
        self.page_html=page.page_html()

    #配置增加按钮
    def add_html(self):
        add_obj = self.model_config_obj.model_class._meta.app_label, self.model_config_obj.model_class._meta.model_name
        add_url = reverse('nb:%s_%s_add' % add_obj)
        # print(self.model_config_obj.request.GET.urlencode())
        query_dict=QueryDict(mutable=True)
        query_dict['uuuuu']=self.model_config_obj.request.GET.urlencode()
        # print(query_dict)

        add_html = mark_safe('<a class="btn btn-primary" href="%s?%s">添加</a>' % (add_url,query_dict.urlencode()))
        return add_html

    #配置组合筛选的条件函数
    def gen_list_filter(self):
        params = self.model_config_obj.request.GET
        model_class = self.model_config_obj.model_class
        for option in self.list_filter:

            field_obj = model_class._meta.get_field(option.name)

            if isinstance(field_obj, RelatedField):
                field_related_class = field_obj.rel.to
                data_list = RowItems(field_related_class.objects.all(),option,params)
            else:
                data_list = RowItems(model_class.objects.all(),option,params)

            yield data_list



class ModelNb(object):
    '''
    基础配置项
    '''
    #定制增加按钮的显示信息
    show_add_btn=True

    #定制标头的显示信息
    list_display=[]
    #定制select标签的批量增加删除
    actions=[]

    #定制组合筛选，搜索条件
    list_filter=[]

    #定制组合筛选的函数
    def get_list_filter(self):
        return self.list_filter

    #定制批量删除
    def all_delete(self):
        pass

    all_delete.short_desc='批量删除'
    #定制删除
    def deleter(self):
        '''可以直接按照pk进行删除'''
        pk_id=self.request.POST.get('pk')#一个删除可以用get，如果是多个删除可以用getlist
        self.model_class.objects.filter(id__in=pk_id).delete()

    deleter.short_desc='删除'
    #定制全部删除调用的函数
    def delter_get(self):
        result=[]
        result.extend(self.actions)
        result.append(ModelNb.all_delete)
        result.append(ModelNb.deleter)
        return result #返回的是函数列表


    def __init__(self, model_class, site,):
        self.model_class = model_class
        self.site = site

    # 定制checkbox和编辑删除显示
    def edite(self, obj=None, is_header=False):
        if is_header:
            return '选择'
        else:
            tpl = "<input type='checkbox' name='pk' value='%s' />" % (obj.pk,)
            return mark_safe(tpl)

    # 定制checkbox和编辑删除显示
    def option(self, obj=None, is_header=False):
        if is_header:
            return '选项'
        else:
            query_dict=QueryDict(mutable=True)
            # print('==========',self.request.GET.urlencode())
            query_dict['uuuuu']=self.request.GET.urlencode()
            print('-------',query_dict.urlencode())

            edit_url = reverse(
                'nb:%s_%s_edit' % (self.model_class._meta.app_label, self.model_class._meta.model_name,),
                args=(obj.pk,))

            del_url = reverse(
                'nb:%s_%s_delete' % (self.model_class._meta.app_label, self.model_class._meta.model_name,),
                args=(obj.pk,))
            tpl = "<a href='%s?%s'>编辑</a>|<a href='%s?%s'>删除</a>" % (edit_url,query_dict.urlencode(),del_url,query_dict.urlencode())
            return mark_safe(tpl)

    # 定制checkbox和编辑删除全部可以调用这样函数，不需要再去调用list_display
    def get_list_display(self):
        result = []
        if self.list_display:
            result.extend(self.list_display)
            result.insert(0, ModelNb.edite)
            result.append(ModelNb.option)
        return result

    #权限增加显示的设置
    def get_show_add_btn(self):

        return self.show_add_btn

        # 定制更改的按钮的显示信息

    show_edit_btn = True
    #权限更改的显示的设置
    def get_show_edit_btn(self):

        return self.show_edit_btn

    #定义装饰器
    def foo(self,func):
        @functools.wraps(func)
        def warpper(request,*args,**kwargs):
            self.request=request
            return func(request,*args,**kwargs)
        return warpper
    @property
    def urls(self):
        return self.get_url(),None,None
    def get_url(self):
        from django.conf.urls import url
        make_obj=self.model_class._meta.app_label , self.model_class._meta.model_name
        patterns = [
            url(r'^$', self.foo(self.changelist_view),name='%s_%s_changelist'%make_obj),
            url(r'^add/$', self.foo(self.add),name='%s_%s_add'%make_obj),
            url(r'^(.+)/delete/$', self.foo(self.delete),name='%s_%s_delete'%make_obj),
            url(r'^(.+)/edit/$', self.foo(self.edit),name='%s_%s_edit'%make_obj),
        ]
        return patterns
    #点击增加按钮走的路径
    def add(self,request,*args,**kwargs):
        # self.change_model_from()
        self.request=request
        # print('=====',request.GET.urlencode())
        tag_id=request.GET.get('_popup')
        if request.GET.get('_popup'):
            if request.method == 'GET':

                froms = self.change_model_from()()
                context = {
                    'froms': froms
                }
                return render(request, 'ninbin/add.html', context)
            elif request.method == 'POST':

                froms = self.change_model_from()(data=request.POST)

                if froms.is_valid():
                    obj=froms.save()
                    if  tag_id:
                         return render(request,'ninbin/fanhui.html',{'obj':obj,'tag_id':tag_id})
                    else:
                        context = {
                            'froms': froms
                        }
                        return render(request, 'ninbin/change.html', context)
        else:


            if request.method=='GET':
                froms=self.change_model_from()()
                context={
                    'froms':froms
                }
                return render(request,'ninbin/add.html',context)
            elif request.method=='POST':
                froms=self.change_model_from()(data=request.POST)
                if froms.is_valid():
                    froms.save()
                    #跳转到增加原路径
                    change_list=request.GET.get('uuuuu')
                    original_obj=reverse('%s:%s_%s_changelist'%(self.site.namespace,self.model_class._meta.app_label,self.model_class._meta.model_name))
                    url='%s?%s'%(original_obj,change_list)
                    return redirect(url)

                context = {
                    'froms': froms
                }
                return render(request, 'ninbin/add.html', context)

    #用户可以自定义modelfrom的设置，可以先设置一个变量
    from_model_from=None
    def change_model_from(self):
        change_model=self.from_model_from
        if not change_model:
            class Modelfrom(ModelForm):
                class Meta:
                    model = self.model_class
                    fields = '__all__'
            change_model=Modelfrom
        return change_model

    #点击删除所进行的路径
    def delete(self,request,pk,*args,**kwargs):
        self.model_class.objects.filter(pk=pk).delete()
        del_url=request.GET.get('uuuuu')
        original_obj = reverse('%s:%s_%s_changelist' % (
            self.site.namespace, self.model_class._meta.app_label, self.model_class._meta.model_name))
        url='%s?%s'%(original_obj,del_url)
        return redirect(url)


    #点击编辑修改所走的路径
    def edit(self,request,pk,*args,**kwargs):
        #首先从数据库取出要修改的值
        change_pk=self.model_class.objects.filter(pk=pk).first()
        if request.method=='GET':
            froms=self.change_model_from()(instance=change_pk)

            context={
                'froms':froms
            }

            return render(request,'ninbin/edit.html',context)
        if request.method=='POST':
            froms=self.change_model_from()(data=request.POST,instance=change_pk)
            if froms.is_valid():
                froms.save()
                #返回原来的路径
                change_obj=request.GET.get('uuuuu')
                original_obj = reverse('%s:%s_%s_changelist' % (
                self.site.namespace, self.model_class._meta.app_label, self.model_class._meta.model_name))
                url='%s?%s'%(original_obj,change_obj)
                return redirect(url)
            context={
                'froms':froms
            }

            return render(request,'ninbin/edit.html',context)

    #主页面路径
    def changelist_view(self,request,*args,**kwargs):
        userinfo_obj = self.model_class.objects.all()
        self.request=request
        if request.method=='POST':
            action_name=request.POST.get('action')#取出来的是函数的名字,类型是str，通过字符串找到这个类或者函数执行
            action_obj=getattr(self,action_name,None)
            # print(action_obj)#<bound method ModelNb.deleter of <app01.ninbin.Userinfoobj object at 0x0000000003E70F98>>
            if action_obj:
                action_obj()

        cl=Changelist(userinfo_obj,self)


        #定制标头
        # def headers():
        #     if not self.list_display:
        #         yield self.model_class._meta.model_name
        #     else:
        #         for v in self.list_display:
        #             yield v(self, is_header=True) if isinstance(v, FunctionType) else self.model_class._meta.get_field(
        #                 v).verbose_name
        #         # if isinstance(v,FunctionType):
        #         #     print('-----',v.__name__)
        #         #     headers.append(v.__name__)
        #         # else:
        #         #     headers.append(self.model_class._meta.get_field(v).verbose_name)
        #         #
        # #d定制表内容
        # def body():
        #
        #     for row in userinfo_obj:
        #         # row_data = []
        #         if not self.list_display:
        #             yield [str(row)]
        #         else:
        #         #     for name in self.list_display:
        #         #         if isinstance(name,FunctionType):
        #         #              row_data.append(name(self,row))
        #         #         else:
        #         #             row_data.append(getattr(row,name))
        #         #     yield row_data
        #             yield [name(self, obj=row) if isinstance(name, FunctionType) else  getattr(row, name) for name in
        #                self.list_display]
        #             # print(row_data)

        # add_obj=self.model_class._meta.app_label,self.model_class._meta.model_name
        # add_url=reverse('nb:%s_%s_add'%add_obj)
        # add_html=mark_safe('<a class="btn btn-primary" href="%s">添加</a>'%(add_obj,))
        context={
            'cl':cl,


        }

        return render(request,'ninbin/change.html',context)


class Nbsite(object):
    def __init__(self):
        self.name='nb'
        self.namespace = 'nb'
        self._registry={}

    def register(self,model,model_nb=None):#model_nb 相当于自己定义的类，也就是自己定义的篇配置
        if not model_nb:
            model_nb=ModelNb
        self._registry[model]=model_nb(model,self)
        # print('-----',self._registry)

    @property
    def urls(self):
        return self.get_url(),self.name,self.namespace

    def get_url(self):
        patterns=[]
        patterns+=[
            url(r'^login/',self.login)
            ]
        for class_name,class_values in self._registry.items():
            # print('class_name',class_values)
            # print('%s/%s'%(class_name._meta.app_label,class_name._meta.model_name))
            # print('class_values',class_values)

            patterns+=[
                url(r'^%s/%s/'%(class_name._meta.app_label,class_name._meta.model_name),class_values.urls)
                ]


        # print(patterns)
        return patterns

    def login(self,request):
        return HttpResponse('登录页面')



site=Nbsite()