/**
 * Created by Administrator on 2017/10/11 0011.
 */


(function (jq) {
    var requestURL='';
    var GLOBAL_CHOICES_DICT={};
    // alert(GLOBAL_CHOICES_DICT)//设置一个全局变量，如果是@@就从这里面取值

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // 请求头中设置一次csrf-token
            if(!csrfSafeMethod(settings.type)){
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });





   /*动态生成数据库里面的文字，比如上架，在线等*/
    function  getChoiceNameById(choice_name,id) {
        var val;

        var status_choices_list = GLOBAL_CHOICES_DICT[choice_name];
        $.each(status_choices_list,function (kkkk,vvvv) {
              if(id == vvvv[0]){
                  val = vvvv[1];
              }
        });
        return val;
    }

    /* 字符串拼接*/
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
     };

    //执行函数的相关操作
    function init(pageNum) {
        $('#loading').removeClass('hide');
        /*获取搜索条件*/
        var condition = getSearchCondition();
        $.ajax({
            url: requestURL,
            type: 'GET',
            data: {'pageNum':pageNum,'condition':JSON.stringify(condition)},
            dataType: 'JSON',
            success: function (response) {


                /* 处理搜索框的动态生成搜索内容*/
                initSearchCondition(response.search_config);
                //处理服务器状态信息
                GLOBAL_CHOICES_DICT = response.global_choices_dict;
                //动态生成标头，和数据函数
                initTableHead(response.table_config);
                //动态生成数据内容
                initTableBody(response.server_dict, response.table_config);

                bindSearchConditionEvent();
                /* 处理页码*/
                initPageHtml(response.page_html);
                $('#loading').addClass('hide')
            },
            error: function () {
                $('#loading').addClass('hide');
            }

        })
    }

    /*获取搜索条件*/
    function getSearchCondition() {
        var result={};

        $('#searchCondition').find('input[type="text"],select').each(function () {
            var name=$(this).attr('name');
            var values=$(this).val();
            if (result[name]){
                result[name].push(values);
            }
           else {
                result[name]=[values ]
            }

        })
        return result
    // console.log(result)
    }
    // 绑定搜索事件
    function bindSearchConditionEvent() {
            $('#searchCondition').on('click','li',function () {
            // $(this) = li标签

            // 找到文本修改
            $(this).parent().prev().prev().text($(this).text());

            // 找input标签
            $(this).parent().parent().next().remove();

            var name = $(this).find('a').attr('name');
            var type = $(this).find('a').attr('type');
            if(type=='select'){
                var choice_name = $(this).find('a').attr('choice_name');
                var tag = document.createElement('select');
                tag.className = "form-control no-radius";
                tag.setAttribute('name',name);
                $.each(GLOBAL_CHOICES_DICT[choice_name],function(i,item){
                    var op = document.createElement('option');
                    op.innerHTML = item[1];
                    op.setAttribute('value',item[0]);
                    $(tag).append(op);
                })
            }else{
                // <input class="form-control no-radius" placeholder="逗号分割多条件" name="hostnmae">
                var tag = document.createElement('input');
                tag.setAttribute('type','text');
                tag.className = "form-control no-radius";
                tag.setAttribute('placeholder','请输入条件');
                tag.setAttribute('name',name);
            }

            $(this).parent().parent().after(tag);

        });
        //点击增加按钮增加，删除按钮删除
        $('.add-condition').click(function () {
            var $tag=$(this).parent().parent().clone();
            $tag.find('.add-condition').removeClass('add-condition').addClass('del-condition').find('i').attr('class','fa fa-minus-square')
            $('#searchCondition').append($tag)
        });
        $('#searchCondition ').on('click','.del-condition',function () {
            $(this).parent().parent().remove()
        });
        //绑定搜索按钮事件
        $('#doSearch').click(function () {
            init(1);
        })
    }
    /* 处理搜索内容*/
    function initSearchCondition(search_config) {
        if(!$('#searchCondition').attr('init')){
            // 找到页面上的搜索条件标签
            // 根据searchConfig生成li
            var $ul = $('#searchCondition :first').find('ul');
            $ul.empty();

            initDefaultSearchCondition(search_config[0]);

            $.each(search_config,function (i,item) {
                var li = document.createElement('li');
                var a =  document.createElement('a');
                a.innerHTML = item.title;
                a.setAttribute('name',item.name);
                a.setAttribute('type',item.type);
                if(item.type == 'select'){
                    a.setAttribute('choice_name',item.choice_name);
                }

                $(li).append(a);
                $ul.append(li);

            });

            $('#searchCondition').attr('init','true');

        }



    }
    /*处理搜索标签input*/
    
    function initDefaultSearchCondition(item) {
        // <input class="form-control no-radius" placeholder="逗号分割多条件" name="hostnmae">#}
        if(item.type == 'input'){
            var tag = document.createElement('input');
            tag.setAttribute('type','text');

            tag.className = "form-control no-radius";
            tag.setAttribute('placeholder','请输入条件');
            tag.setAttribute('name',item.name);

        }else{
            var tag = document.createElement('select');
            tag.className = "form-control no-radius";
            tag.setAttribute('name',item.name);
            $.each(GLOBAL_CHOICES_DICT[item.choice_name],function(i,row){
                var op = document.createElement('option');
                op.innerHTML = row[1];
                op.setAttribute('value',row[0]);
                $(tag).append(op);
            })
        }

        $('#searchCondition').find('.input-group').append(tag);
        $('#searchCondition').find('.input-group label').text(item.title);
    }


    /* 处理分页*/
    function initPageHtml(page_html) {
        $('#pagination').empty().append(page_html)

    }

    //获取表头
    function initTableHead(table_config) {
        $('#tHead tr').empty();
            $.each(table_config,function (k,values) {
                if (values.display){
                     var th=document.createElement('th');
                    th.innerText=values.title;
                    $('#tHead tr').append(th)
                }


            })
    }

    //获取表格内容
    function initTableBody(server_dict,table_config) {
        $('#tBody').empty()
        $.each(server_dict,function (k,v_dict) {

            var tr=document.createElement('tr');
            $.each(table_config,function (kk,vv) {
                if (vv.display) {
                    var td = document.createElement('td');
                    format_dict = {};
                    $.each(vv.text.kwargs, function (kkk, vvv) {
                        if (vvv.substring(0,2) == '@@') {
                            var name = vvv.substring(2, vvv.length);

                            var status_choice_list=GLOBAL_CHOICES_DICT[name];//取出来的是数据库的列表
                            var val = getChoiceNameById(name,v_dict[vv.p]);
                            format_dict[kkk] = val;


                        }
                        else if (vvv[0] == "@") {

                            var name = vvv.substring(1, vvv.length);
                            format_dict[kkk] = v_dict[name];
                        }
                        else {

                            format_dict[kkk] = vvv;
                        }
                    });
                    td.innerHTML = vv.text.tpl.format(format_dict);
                    /* 位td标签添加属性操作*/
                    $.each(vv.attr,function (attrname,attrvalues) {
                        if(attrvalues[0]=='@'){
                            attrvalues=v_dict[attrvalues.substring(1,attrvalues.length)]
                        }
                        td.setAttribute(attrname,attrvalues)

                    });
                    $(tr).append(td)
                }
            });

            $('#tBody').append(tr)
        })

    }

    /*为单独的checkbox绑定事件*/
    function bindEditModeEvent() {
        $('#tBody').on('click',':checkbox',function () {
            if ($('#editModeStatus').hasClass('btn-class')) {
                        alert(2342)
                if ($(this).prop('checked')) {
                    //选中进入编辑模式
                    var $tr = $(this).parent().parent();
                    $tr.addClass('success')
                    //找到所有的tr标签，进行td的循环
                    $tr.find('td[edit="true"]').each(function () {
                        //进入编辑模式，生成input标签
                        tdIntoEditMode($(this))//this 指的是td标签
                    })

                } else {
                    var $tr = $(this).parent().parent();
                    $tr.removeClass('success')
                    $tr.find('td[edit="true"]').each(function () {
                        if (tdOutEditMode($(this))) {
                            $tr.attr('edit-status', 'true');
                        }

                    })

                }
        }
        })
    }


    function tdIntoEditMode($td) {
            //循环出所有的td标签，取出相应的文本进行select和input的替换

            if ($td.attr('edit-type') == 'select') {
                var attr = $td.attr('choice-key');
                var status_choice = GLOBAL_CHOICES_DICT[attr];
                var tag = document.createElement('select');
                var origin = $td.attr('origin');
                $.each(status_choice, function (k, v) {
                    var option = document.createElement('option');
                    option.innerHTML = v[1];
                    option.value = v[0];
                    if (option.value == origin) {
                        option.setAttribute('selected', 'selected')
                    }
                    tag.append(option)
                });
                $td.html(tag)

            } else {
                //走input标签
                var text = $td.text();
                var tag = document.createElement('input');
                tag.value = text;
                $td.html(tag)
            }


    }

    function tdOutEditMode($td) {
            var editStatus=false;//判断有没有更改，更改变化成true
            var origin=$td.attr('origin')

            if ($td.attr('edit-type') == 'select') {
                var val = $td.find('select').val();
                var values = $td.find('select option[value="' + val + '"]').text();
                $td.attr('new_values',val)
                $td.html(values)


            } else {
                var val = $td.find('input').val();
                $td.html(val)
            }
            if(origin != val){
                editStatus=true
            }
            return editStatus
    }

    /*
    按钮组绑定事件
     */
    function bindBtnGroupEvent(){

        //编辑
        $('#editModeStatus').click(function () {
            //进入和退出编辑模式
            if($(this).hasClass('btn-warning')) {
                //退出编辑模式
                $(this).removeClass('btn-warning');
                $(this).text('进入编辑模式');

                $('#tBody :checked').each(function () {
                   var $tr=$(this).parent().parent();
                   $tr.find('td[edit="true"]').each(function () {
                       if (tdOutEditMode($(this))) {
                            // alert(3435)
                            $tr.attr('edit-status', 'true');
                        }
                   })
               })

            }
            else {
                //进入编辑模式

                $(this).addClass('btn-warning');
                $(this).text('退出编辑模式');
                $('#tBody :checked').each(function () {

                    var $tr = $(this).parent().parent();
                    $tr.find('td[edit="true"]').each(function () {
                       tdIntoEditMode($(this))
                   })
                });

            }


        });

        //全选
        $('#checkAll').click(function () {
            $('#tBody :checkbox').each(function () {
                if(!$(this).prop('checked')){
                    $(this).prop('checked','true');
                    //之后进入编辑模式
                     if ($('#editModeStatus').hasClass('btn-warning')) {
                         var $tr = $(this).parent().parent();
                         $tr.find('td[edit="true"]').each(function () {
                             tdIntoEditMode($(this))
                         })
                     }
                }
            })

        });

        //取消
        $('#checkCancel').click(function () {
            $('#tBody :checkbox').each(function () {

                    $(this).prop('checked',false);
                    if($('#editModeStatus').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        $tr.find('td[edit="true"]').each(function () {
                            if (tdOutEditMode($(this))) {
                            alert(3435)
                            $tr.attr('edit-status', 'true');
                        }
                        })
                    }
            })
        });
        
        //反选
        $('#resverChall').click(function () {
                $('#tBody :checkbox').each(function () {
                if(!$(this).prop('checked')){
                    $(this).prop('checked','true')

                     if ($('#editModeStatus').hasClass('btn-warning')) {
                         var $tr = $(this).parent().parent();
                         $tr.find('td[edit="true"]').each(function () {
                             tdIntoEditMode($(this))
                         })
                     }

                }else {
                    $(this).prop('checked',false)
                    if($('#editModeStatus').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        $tr.find('td[edit="true"]').each(function () {
                            if (tdOutEditMode($(this))) {
                            alert(3435)
                            $tr.attr('edit-status', 'true');
                        }
                        })
                    }

                }
            })
        });


        //删除
        $('#delMulti').click(function () {
            $('#tBody :checkbox').each(function () {
               if($(this).prop('checked')){
                  $(this).val()
               }
            })
        });
        //删除模态框确认
        $('#sure').click(function () {
            tmp=[];
            $('#tBody :checked').each(function () {
                tmp.push($(this).val())
            });
            $.ajax({
                url:requestURL,
                type:'DELETE',
                data:JSON.stringify(tmp),
                traditional:true,
                dataType: 'JSON',
                success:function (arg) {
                    if(arg.status){

                        $('#handleStatus').text('执行成功');
                        $('#tBody :checked').parent().parent().remove();
                        setTimeout(function () {
                            $('#handleStatus').empty()
                        },5000);
                        $('#delMulti').modal('hide')
                    }else {
                        $('#handleStatus').text('执行错误')
                        $('#delMulti').modal('hide')
                    }
                }




            })


        })



        //保存
        $('#saveMulti').click(function () {
            var update_dict=[];


            $('#tBody tr[edit-status="true"]').each(function () {
               var tmp={};
               var nid=$(this).children().attr('nid');
                tmp['nid']=nid;
                $(this).children('[edit="true"]').each(function () {
                    var name=$(this).attr('name');

                    var origin=$(this).attr('origin');
                    if ($(this).attr('edit-type')=='select'){
                        var Newvalue=$(this).attr('new_values')
                    }else {
                        var Newvalue=$(this).text()
                    }
                    if (origin != Newvalue){
                        tmp[name]=Newvalue
                    }
                });
                update_dict.push(tmp)
            });

            $.ajax({
                url: requestURL,
                type: 'PUT',
                data: JSON.stringify(update_dict),
                traditional:true,
                dataType: 'JSON',
                success:function (arg) {
                  if(arg.status){
                        $('#handleStatus').text('执行成功');
                        setTimeout(function () {
                            $('#handleStatus').empty()
                        },5000)
                    }else {
                        $('#handleStatus').text('执行错误')
                    }

                }
            })
        });

        //模态取消绑定
        $('#ffff').click(function () {
            $('#delMulti').modal('hide')
        })


    }



    jq.extend({
        'nBlist':function (url) {
            requestURL=url;
            init(1);
            // alert(213)
            bindEditModeEvent()

            bindBtnGroupEvent()
        },

        /*调用分页的函数*/
        'changePage':function (pageNum) {
            init(pageNum)
        }
    })

})(jQuery);










