 // Disabled Tab Click Wizard
 jQuery('#disabledTabWizard').bootstrapWizard({
     tabClass: 'nav nav-pills nav-justified nav-disabled-click',
     onTabClick: function(tab, navigation, index) {
         return false;
     }
 });

 var editor = CodeMirror.fromTextArea(document.getElementById("code2"), {
     mode: {
         name: "python"
     },
     lineNumbers: true,
     theme: 'ambiance'
 });

 //代码块
 $('.code_btn').click(function() {
     $('.code_group').show();
     $('.list_group').hide();
     $('.codeview_group').hide();
     setTimeout(function() {
         editor.refresh();
     }, 200);
 })

 //导出ai.zip
 $('.aipy_btn').click(function() {
     var code_name = $('.left_parts .current').attr('_id');
     var url = '/model/download/aipy?code_name={0}'.format(code_name);
     window.open(url, '_blank');
 })

 //同步
 $('.real_btn').click(function() {
     var code_name = $('.left_parts .current').attr('_id');
     $.get('/layer/codeblock/synchro?code_name={0}'.format(code_name), function(rs) {
         editor.setValue(rs.data)
     });
 })
 $('.real_codeview').click(function() {
         var code_name = $('.left_parts .current').attr('_id');
         // $('#preview img').attr('src','static/{0}.png'.format(code_name))
         $.get('/layer/codeview?code_name={0}'.format(code_name), function(rs) {
             $('#preview img').attr('src', rs.data)
         });
     })
     // 列表
 $('.list_btn').click(function() {
     $('.code_group').hide();
     $('.list_group').show();
     $('.codeview_group').hide();
 })

 // 预览
 $('.preview_btn').click(function() {
     $('.code_group').hide();
     $('.list_group').hide();
     $('.codeview_group').show();
 })

 $('.validform').Validform(validform_conf_reload);

 //获取模型结构列表
 $('.left_parts .model_code_li').click(function() {
     var $this = $(this);
     $.cookie('next_count', null)
     $('#model_name').html($this.text())
     $this.addClass('current').siblings('li').removeClass('current');
     $.cookie('current', $this.index())
     $.get('/optimizer/html?code_name={0}'.format($this.attr('_id')), function(rs) {
         if (rs.status) {
             $('.optimizer_form').html('');
             $('.optimizer_form').append(rs.data);
             var optimizer_val = $('#optimizer_val').attr('value');
             $('#compile_opt').find('select[name=optimizer]').val(optimizer_val);
         }
     })
     location.reload();
 })

 if ($.cookie('current')) {
     $('.left_parts').find('li').eq($.cookie('current')).addClass('current');
 } else {
     $('.left_parts').find('li').eq(0).addClass('current');
 }

 $('#model_name').html($('.current').text())
 var loss_value = $('.left_parts .current').attr('loss_value')
 var metrics_value = $('.left_parts .current').attr('metrics_value')
 if (loss_value || metrics_value) {
     $('.kreas_score').text('loss_value:' + loss_value + ' metrics_value:' + metrics_value)
 } else {
     $('.kreas_score').text('暂未获得评测得分')
 }

 var code_name = $('.left_parts .current').attr('_id');
 $.get('/optimizer/html?code_name={0}'.format(code_name), function(rs) {
     if (rs.status) {
         $('.optimizer_form').html('');
         $('.optimizer_form').append(rs.data);
         var optimizer_val = $('#optimizer_val').attr('value');
         $('#compile_opt').find('select[name=optimizer]').val(optimizer_val);
     }
 })

 //删除模型
 $('.model_del').click(function(rs) {
     var code_name = $('.left_parts .current').attr('_id');
     Confirm("你确定要删除该模型吗?", function() {
         $.post('/model/del', {
             code_name: code_name,
         }, function(rs) {
             if (rs.status) {
                 $.cookie('next_count', null);
                 $.cookie('current', null)
                 location.reload()
             }
         })
     })
 })

 //添加模型
 $('.leftpanelinner').on('click', '.add_model', function() {
     $('.model_add').find('h4').text('创建模型(输入和输出不能重复)');
     $('.model_add').find('input[name=code_name]').removeAttr("readonly")
     $('.model_add').find('form').attr('action', '/model/add');
     $('.model_add').find('input').val('');
     $.cookie('current', $('.left_parts .model_code_li').length);
     $.cookie('next_count', null);

 })

 //编辑模型
 $('.pageheader').on('click', '.edit_model', function() {
     $('.model_add').find('h4').text('编辑模型(输入和输出不能重复)');
     $('.model_add').find('form').attr('action', '/model/edit');
     $('.model_add').find('input[name=code_name]').attr('readonly', true);
     $('.model_add').find('input[name=code_name]').val($('.left_parts .current').attr('_id'))
     $('.model_add').find('input[name=name]').val($('.left_parts .current').text())
     $('.model_add').find('input[name=input]').val($('.left_parts .current').attr('input'))
     $('.model_add').find('input[name=output]').val($('.left_parts .current').attr('output'))
 })

 //添加模型结构
 var layer_n = $('select[name=layer_name]').val();
 $.get('/layer/html?layer_name={0}'.format(layer_n), function(rs) {
     if (rs.status) {
         $('.add_model_struct .layer').append(rs.data)
     }
 })
 $('select[name=layer_name]').change(function() {
     var layer = $(this).val();
     $.get('/layer/html?layer_name={0}'.format(layer), function(rs) {
         if (rs.status) {
             $('.add_model_struct .layer').html('');
             $('.add_model_struct .layer').append(rs.data);
         }
     })
 })

 $('.add_struct').click(function() {
     $.cookie('next_count', 2);
     var code_name = $('.left_parts .current').attr('_id');
     $('.add_model_struct').find('input').val('');
     $('.add_model_struct').find('input[name=code_name]').val(code_name);
     $('.list').find('h4').text('添加模型结构');
     $('.list').find('form').attr('action', '/layer/add')
     $('.list').find('select[name=layer_name]').attr('disabled', false);
 })

 //模型结构-编辑结构
 $('#list_model').on('click', '.edit_struct', function() {
     $.cookie('next_count', 2);
     var oid = $(this).parents('tr').attr('oid');
     var code_name = $('.left_parts .current').attr('_id');
     var layer_name = $(this).parents('tr').find('.layerName').text();
     $('.list').find('h4').text('编辑模型结构');
     $('.list').find('form').attr('action', '/layer/edit');
     $('.add_model_struct').find('input[name=code_name]').val(code_name);
     $('.list').find('select[name=layer_name]').val(layer_name);
     $.get('/layer/html?code_name={0}&oid={1}&layer_name={2}'.format(code_name, oid, layer_name), function(rs) {
         $('.add_model_struct .layer').html('');
         $('.add_model_struct .layer').append(rs.data);
     })
 })

 //模型结构-删除结构
 $('#list_model').on('click', '.delet_struct', function() {
     var oid = $(this).parents('tr').attr('oid');
     var code_name = $('.left_parts .current').attr('_id');
     Confirm("你确定要删除该结构吗?", function() {
         $.post('/layer/del', {
             code_name: code_name,
             oid: oid
         }, function(rs) {
             if (rs.status) {
                 $.cookie('next_count', 2);
                 location.reload()
             }
         })
     })
 })


 //模型结构下载
 $('.down_load').click(function() {
     var code_name = $('.left_parts .current').attr('_id');
     var url = '/layer/download?code_name={0}'.format(code_name);
     window.open(url, '_blank');
 })

 //模型上传
 $('.import_btn').click(function() {　　　　　
     var code_name = $('.left_parts .current').attr('_id');
     $('.up_load').find('input[name=code_name]').val(code_name)
     $('#fileupload').ajaxForm({
         url: '/layer/upload',
         type: 'POST',
         error: function(data) {
             alert('导入文件格式不正确！');
             location.reload();
         },
         success: function(rs) {
             if (rs.status) {
                 $.cookie('next_count', 2);
                 location.reload();
             } else {
                 alert(rs.msg);
             }　　
         }
     })
 });

 //编译选项部分
 $('#compile_opt').find('select[name=optimizer]').change(function() {
     var optimizer = $(this).val();
     $.get('/optimizer/html?optimizer={0}'.format(optimizer), function(rs) {
         if (rs.status) {
             $('.optimizer_form').html('');
             $('.optimizer_form').append(rs.data)
         }
     })
 })
 $('.edit_optimizer').click(function() {
     var code_name = $('.left_parts .current').attr('_id');
     $('#compile_opt').find('input[name=code_name]').val(code_name)
 })

 //next
 $('.next').click(function() {
         var code_name = $('.left_parts .current').attr('_id');
         //编译选项
         if ($('#compile_opt').hasClass('active')) {
             $.get('/struct/list/html?code_name={0}'.format(code_name), function(rs) {
                     if (rs.status) {
                         $('#list_model').html('');
                         $('#list_model').append(rs.data);
                         $("#table_struct").tableDnD({
                             onDrop: function(table, row) {
                                 var struct_order = [];
                                 $('#table_struct tbody tr').each(function(i, v) {
                                     struct_order.push($(v).attr('oid'))
                                 })
                                 $.post('/layer/edit/order?struct_order={0}&code_name={1}'.format(struct_order.join(','), code_name), function(rs) {
                                     // console.log(rs)
                                 })
                             }
                         });
                         editor.setValue(rs.code)
                         $('#preview img').attr('src', rs.imgurl)
                     }
                 })
                 //训练数据
             $.get('/train/list/html?code_name={0}&handle_type=train'.format(code_name), function(rs) {
                 if (rs.status) {
                     $('#practice_data .practice_list').html(' ');
                     $('#practice_data .practice_list').append(rs.data);
                 }
             })
         }
         //模型测评
         if ($('#practice_data').hasClass('active')) {
             $.get('/evaluate/list/html?code_name={0}&handle_type=train'.format(code_name), function(rs) {
                 if (rs.status) {
                     $('#modal_measure .text_list').html(' ');
                     $('#modal_measure .text_list').append(rs.data);
                 }
             })
         }
     })
     /*训练数据-----------------------------------------------------------------------------*/
     //导入excel
 $('.import_excel').click(function() {　　　　　
     var code_name = $('.left_parts .current').attr('_id');
     $('.up_excel').find('input[name=code_name]').val(code_name)
     $('#excelupload').ajaxForm({
         url: '/train/excel/upload',
         type: 'POST',
         error: function(data) {
             alert('导入文件格式不正确！');
             location.reload();
         },
         success: function(rs) {
             if (rs.status) {
                 $.cookie('next_count', 3)
                 location.reload();
             } else {
                 alert(rs.msg);
             }　　
         }
     })
 });

 //导出excel
 $('.out_excel').click(function() {
     var code_name = $('.left_parts .current').attr('_id');
     var url = '/train/excel/download?code_name={0}&handle_type=train'.format(code_name);
     window.open(url, '_blank');
 })

 // 训练数据表格行删除
 function Confirm(content, cb) {
     if (null == document.getElementById('dialog-confirm')) {
         $(document.body).append('<div id="dialog-confirm" title="提示信息"> \
                                  <p style="line-height:24px;font-size: 14px;margin:15px;">您确认要删除吗？</p> \
                                  </div>')
     };
     $('#dialog-confirm').find('p').html(content);
     $('#dialog-confirm').dialog({
         resizable: false,
         modal: true,
         width: 350,
         height: 'auto',
         top: 256,
         buttons: {
             "取消": function() {
                 $(this).dialog("close");
             },
             "确定": function() {
                 $(this).dialog("close");
                 cb();
             }
         }
     });
 }
 $('#practice_data').on('click', '.del_train_data', function() {
     var code_name = $('.left_parts .current').attr('_id');
     var id = $(this).parents('tr').attr('_id');
     Confirm("你确定要删除本条数据吗?", function() {
         $.post('/train/del', {
             code_name: code_name,
             _id: id
         }, function(rs) {
             if (rs.status) {
                 $.cookie('next_count', 3);
                 location.reload()
             }
         })
     })
 })

 // 训练数据表格行编辑
 $('#practice_data').on('click', '.edit_train_data', function() {
     var code_name = $('.left_parts .current').attr('_id');
     var id = $(this).parents('tr').attr('_id');
     $('.inAndout ').find('input[name=code_name]').val(code_name);
     $('.inAndout ').find('input[name=_id]').val(id);
     $('.inAndout ').find('form').attr('action', '/train/edit');
     $('.inAndout ').find('h4').text('编辑输入/出模型');
     $('.inAndout .clone_box').html(' ');
     $.get('/train/edit?code_name={0}&_id={1}'.format(code_name, id), function(rs) {
         $.cookie('next_count', 3);
         $.each(rs.title, function(i, v) {
             var clone = $('.clone_input')[0].cloneNode(true);
             $(clone).find('.control-label').text(v);
             if (v in rs.data) {
                 $(clone).find('input').val(rs.data[v])
             } else {
                 $(clone).find('input').val('')
             }
             $(clone).find('input').attr("name", v);
             $(clone).css('display', 'block')
             $('.inAndout .clone_box').append(clone)
         })
     })
 })

 //训练数据从mongo导入
 $('.import_mongo').click(function() {
     var code_name = $('.left_parts .current').attr('_id');
     $('.mongo').find('input[name=code_name]').val(code_name);
     $('.mongo').find('form').attr('action', '/train/mongo/upload')
     $.cookie('next_count', 3);
     $.get('/model/data?code_name={0}'.format(code_name), function(rs) {
         //var exp=rs.data.input.concat( rs.data.output );
         $('.mongo .mogo_exports').html(' ');
         $.each(rs.data.input, function(i, v) {
             var clone = $('.clone_input')[0].cloneNode(true);
             $(clone).find('.control-label').text('输入字段-' + v);
             $(clone).find('input').attr("name", v);
             $(clone).css('display', 'block')
             $('.mongo .mogo_exports').append(clone)
         })
         $.each(rs.data.output, function(i, v) {
             var clone = $('.clone_input')[0].cloneNode(true);
             $(clone).find('.control-label').text('输出字段-' + v);
             $(clone).find('input').attr("name", v);
             $(clone).css('display', 'block')
             $('.mongo .mogo_exports').append(clone)
         })
     })
 })

 //训练数据设置
 $('.train_set').click(function() {
     var code_name = $('.left_parts .current').attr('_id');
     $('.train').find('input[name=code_name]').val(code_name);
     $.cookie('next_count', 3);
     $.get('/model/data?code_name={0}'.format(code_name), function(rs) {
         $.each(rs.data.train_setting, function(i, v) {
             if (i == 'shuffle') {
                 var radio = $('.train').find('input[name=shuffle]');
                 $.each(radio, function(k, input) {
                     if ($(input).val() == v) {
                         $(input).attr('checked', true)
                     }
                 })
             } else {
                 $('.train').find('input[name={0}]'.format(i)).val(v);
             }
         })
     })
 })

 var svg_timeout = true;
 var train_title = ''
 var code_name = $('.left_parts .current').attr('_id');
 var layout = {
     height: 260,
     width: 520,
     hovermode: 'closest',
     paper_bgcolor: '#1c1e1f',
     plot_bgcolor: '#1c1e1f',
     font: {
         color: '#fff'
     },
     xaxis: {
         type: 'category',
         gridcolor: '#adadad'
     },
     legend: {
         orientation: "h",
         y: -0.5,
     },
     yaxis: {
         gridcolor: '#adadad'
     },
     margin: {
         l: 30,
         t: 25,
         b: 45,
         r: 10
     }
 };
 //启动及关闭按钮  
 function svg_timer() {
     if (svg_timeout) return;
     $.get('/train/exec/log?code_name={0}'.format(code_name), function(rs) {
         $('.train_start .train_log').show();
         if (!rs.status) {
             svg_timeout = true;
             $('.train_result').text(rs.data)
             exec_disabled(false)
             return
         }
         try {
             console.log("data", rs.data)
             draw_line(rs.data)
         } catch (e) {
             throw e
         }

         // if(rs.data.toString().indexOf('end') > -1) {
         //     svg_timeout=true;
         //     exec_disabled(false)
         //     $('.train_result').text('训练完成')
         // }
         $.get('/model/data?code_name={0}'.format(code_name), function(rs) {
             if (rs.data.train_status == '0') {
                 $('.train_result').text('训练完成')
                 exec_disabled(false)
                 svg_timeout = true;
             } else if (rs.data.train_status == '1') {
                 $('.train_result').text('正在训练．．．')
                 exec_disabled(false)
             }
         })
     })
     setTimeout(svg_timer, 1000); //time是指本身,延时递归调用自己,100为间隔调用时间,单位毫秒  
 }

 //画图函数
 function draw_line(data) {
     var y = [
             [],
             [],
             [],
             [],
             []
         ],
         t = [],
         draw_data = [];
     if (data instanceof Array) {
         $.each(data, function(i, v) {
             var arr_v = v.split(',');
             if (i > 0) {
                 $.each(arr_v, function(index, val) {
                     if (index > 0) {
                         y[index].push((val * 1).toFixed(4))
                     } else {
                         y[index].push(val)
                     }
                 })
             } else {
                 t = arr_v;
             }

         })
         y[0].pop();
         $.each(y, function(i, v) {
             if (i > 0) {
                 var trace = {
                     x: y[0],
                     y: y[i],
                     type: 'scatter',
                     mode: 'lines',
                     name: t[i]
                 }
                 draw_data.push(trace)
             }
         })
         layout.xaxis.title = t[0];
         Plotly.newPlot('line_1', draw_data, layout, plot_config_null);
     }

 }

 //训练终止显示?
 function exec_disabled(flag) {
     $('.btn_train_exec').attr('disabled', flag);
     $('.btn_train_end').attr('disabled', flag);
 }
 //训练

 $('._train').click(function() {
         code_name = $('.left_parts .current').attr('_id');
         $('.train_start').find('input[name=code_name]').val(code_name);
         $.cookie('next_count', 3);
         $.get('/model/data?code_name={0}'.format(code_name), function(rs) {
             if (rs.data.train_status == '0') {
                 $('.btn_train_end').attr('disabled', false);
             } else if (rs.data.train_status == '1') {
                 $('.btn_train_end').attr('disabled', false);
                 $('.btn_train_exec').attr('disabled', true);
             }
         })
         $.get('/train/exec/log?code_name={0}'.format(code_name), function(rs) {
             $('.train_start .train_log').show();
             $('.train_start .train_log_title').html(' ')
             train_title = rs.title
             if (rs.data) {
                 $('.train_start .train_log_title').append($('<span>').html(train_title));
                 if (!rs.status) {
                     return
                 }
                 draw_line(rs.data)
             }
         })
     })
     // 开始训练
 $(".btn_train_exec").click(function() {
         var code_name = $('.left_parts .current').attr('_id');
         var self = this;
         $(this).attr('disabled', true);
         $('.btn_train_end').attr('disabled', false);
         $.post('/train/exec?code_name={0}'.format(code_name), function(rs) {
             alert(rs.data)
             if (rs.status) {
                 svg_timeout = false;
                 svg_timer()
                 $('.btn_train_exec').attr('disabled', true);
                 $('.train_result').text('正在训练．．．')
             }
         })
     })
     //终止
 $(".btn_train_end").click(function() {
         var code_name = $('.left_parts .current').attr('_id');
         // $(this).attr('disabled',true);
         // $('.btn_train_exec').attr('disabled',false);
         $.get('/train/exec?code_name={0}'.format(code_name), function(rs) {
             if (rs.status) {
                 alert(rs.data)
                 $('.btn_train_exec').attr('disabled', false);
             }
         })
         svg_timeout = true
     })
     /*模型测评-----------------------------------------------------------------------------*/
     //导出Excel
 $('.eva_outexl').click(function() {
     var code_name = $('.left_parts .current').attr('_id');
     var url = '/evaluate/excel/download?code_name={0}'.format(code_name);
     window.open(url, '_blank');
 })

 //导入excel
 $('.eva_inexl').click(function() {　　　　　
     var code_name = $('.left_parts .current').attr('_id');
     $('.up_excel').find('input[name=code_name]').val(code_name)
     $('#excelupload').ajaxForm({
         url: '/evaluate/excel/upload',
         type: 'POST',
         error: function(data) {
             alert('导入文件格式不正确！');
             // location.reload();
         },
         success: function(rs) {
             if (rs.status) {
                 $.cookie('next_count', 4)
                 alert(rs.data)
                 location.reload();
             }
         }
     })
 });

 //mongo导入
 $('.eva_mongo').click(function() {
     var code_name = $('.left_parts .current').attr('_id');
     $('.mongo').find('input[name=code_name]').val(code_name);
     $('.mongo').find('form').attr('action', '/evaluate/mongo/upload')
     $.cookie('next_count', 4);
     $.get('/model/data?code_name={0}'.format(code_name), function(rs) {
         var exp = rs.data.input
         $('.mongo .mogo_exports').html(' ');
         $.each(exp, function(i, v) {
             var clone = $('.clone_input')[0].cloneNode(true);
             $(clone).find('.control-label').text('输入字段-' + v);
             $(clone).find('input').attr("name", v);
             $(clone).css('display', 'block')
             $('.mongo .mogo_exports').append(clone)
         })
         $.each(rs.data.output, function(i, v) {
             var clone = $('.clone_input')[0].cloneNode(true);
             $(clone).find('.control-label').text('输出字段-' + v);
             $(clone).find('input').attr("name", v);
             $(clone).css('display', 'block')
             $('.mongo .mogo_exports').append(clone)
         })
     })
 })

 //测评设置
 $('.eva_test').click(function() {
     var code_name = $('.left_parts .current').attr('_id');
     $.post('/evaluate/exec?code_name={0}'.format(code_name), function(rs) {
         if (rs.status) {
             $('.kreas_score').text('loss_value:' + rs.score[0] + '  metrics_value:' + rs.score[1]);
             $.get('/evaluate/list/html?code_name={0}'.format(code_name), function(rs1) {
                 if (rs1.status) {
                     $('#modal_measure .text_list').html(' ');
                     $('#modal_measure .text_list').append(rs1.data);
                 }
             })
             alert(rs.data)
         }
     })
 })

 //编辑
 $('#modal_measure').on('click', '.edit_train_data', function() {
     var code_name = $('.left_parts .current').attr('_id');
     var id = $(this).parents('tr').attr('_id');
     $('.inAndout ').find('input[name=code_name]').val(code_name);
     $('.inAndout ').find('input[name=_id]').val(id);
     $('.inAndout ').find('form').attr('action', '/evaluate/edit');
     $('.inAndout ').find('h4').text('编辑输入模型');
     $('.inAndout .clone_box').html(' ');
     $.get('/evaluate/edit?code_name={0}&_id={1}'.format(code_name, id), function(rs) {
         $.cookie('next_count', 4);
         $.each(rs.title, function(i, v) {
             var clone = $('.clone_input')[0].cloneNode(true);
             $(clone).find('.control-label').text(v);
             if (v in rs.data) {
                 $(clone).find('input').val(rs.data[v])
             } else {
                 $(clone).find('input').val('')
             }
             $(clone).find('input').attr("name", v);
             $(clone).css('display', 'block')
             $('.inAndout .clone_box').append(clone)
         })
     })
 })

 //删除
 $('#modal_measure').on('click', '.del_train_data', function() {
     var code_name = $('.left_parts .current').attr('_id');
     var id = $(this).parents('tr').attr('_id');
     Confirm("你确定要删除本条数据吗?", function() {
         $.post('/evaluate/del', {
             code_name: code_name,
             _id: id
         }, function(rs) {
             if (rs.status) {
                 $.cookie('next_count', 4);
                 location.reload()
             }
         })
     })
 })

 /*页面记忆tab----------*/
 if ($.cookie('next_count')) {
     for (var i = 0; i < $.cookie('next_count'); i++) {
         $('.next').click();
     }
 }
 var w_height = $(window).height();
 // $('modal_nav .tab-pane').height(w_height-216)
 $('modal_nav').height(w_height - 217)


 // 数值量程设置
 var input_arr = $('.left_parts .current').attr('input').split(',');
 var output_arr = $('.left_parts .current').attr('output').split(',');
 var put_arr = input_arr.concat(output_arr)
 $.each(put_arr, function(i, v) {
     var str = '<div class="form-group dataset_line">' +
         '<label class="col-sm-2 control-label">' + v + '</label>' +
         ' <div class="col-sm-2">' +
         '<input type="text"  class="form-control">' + '<span class="" style="width: 30px;font-size: 25px;line-height:40px; margin-left:10px;">-</span>' +
         ' </div>' +
         // '<span class="col-sm-1" style="width: 30px;font-size: 25px">-</span>' +
         ' <div class="col-sm-2">' +
         '<input type="text"  class="form-control">' + '<span class="" style="width: 30px;font-size: 25px;line-height:40px; margin-left:10px;">-</span>' +
         ' </div>' +
         ' <div class="col-sm-2">' +
         '<input type="text"  class="form-control">' + '<span class="" style="width: 30px;font-size: 25px;line-height:40px; margin-left:10px;">-</span>' +
         ' </div>' +
         ' <div class="col-sm-2">' +
         '<input type="text"  class="form-control">' +
         ' </div>' +
         ' <div class="col-sm-1">' +
         '<button class="btn btn-primary  btn_range_extract" type="button">提取</button>' +
         ' </div>' +
         '</div>'
     $('#range_set .range').append(str)
 })

 /**数值量程设置**/
 //数据获取渲染
 if (code_name) {
     $.get('/num/data?code_name={0}'.format(code_name), function(rs) {
         if (!is_empty_object(rs.data)) {
             $('.range .dataset_line').each(function(i, v) {
                 var key = $(v).find('label').text();
                 var _data = [];
                 if (rs.data.hasOwnProperty(key)) {
                     _data = rs.data[key];
                 }
                 $(v).find('input').each(function(index, input) {
                     if (index == 0 || index == 1) {
                         $(input).val(_data[index]);
                     }
                 })
             })
         }
         if (!is_empty_object(rs.num_alarm_set)) {
             $('.range .dataset_line').each(function(i, v) {
                 var key = $(v).find('label').text();
                 var _data = [];
                 if (rs.num_alarm_set.hasOwnProperty(key)) {
                     _data = rs.num_alarm_set[key];
                 }
                 $(v).find('input').each(function(index, input) {
                     if (index == 2 || index == 3) {
                         $(input).val(_data[index - 2]);
                     }
                 })
             })
         }
     })
 }
 //数据保存
 $('.btn-setting-save').click(function() {
         var args = {}
         var code_name = $('.left_parts .current').attr('_id');
         args.code_name = code_name;
         var flag = true;
         $('.range .dataset_line').each(function(i, v) {
             var key = $(v).find('label').text();
             var input_arr = [];
             $(v).find('input').each(function(index, input) {
                 if ($(input).val()) {
                     input_arr.push($(input).val());
                 } else {
                     alert('请设置全量程信息')
                     flag = false;
                     return flag
                 }
             })
             if (!flag) {
                 return flag
             }
             args[key] = input_arr.join(',')
         })

         if (flag) {
             $.post('/num/setting?{0}'.format($.param(args)), function(rs) {
                 if (rs.status) {
                     alert("保存成功")
                 }
             })
         }

     })
     //数据提取
 $('#range_set').on('click', '.btn_range_extract', function() {
         var v = $(this).parents('.dataset_line');
         var key = $(v).find('label').text();
         $.get('/num/distill?code_name={0}&key={1}'.format(code_name, key), function(rs) {
             if (rs.status) {
                 $(v).find('input').each(function(index, input) {
                     if (index == 0) {
                         $(input).val(rs.min)
                     } else if (index == 1) {
                         $(input).val(rs.max)
                     }
                 })
                 alert('提取完成')
             }
         })
     })
     // 全部提取
 $('.all_extract').click(function() {
     $.get('/num/distill/all?code_name={0}'.format(code_name), function(rs) {
         console.log(rs)
         if (rs.status) {
             if (!is_empty_object(rs.data)) {
                 $('.range .dataset_line').each(function(i, v) {
                     var key = $(v).find('label').text();
                     var _data = [];
                     if (rs.data.hasOwnProperty(key)) {
                         _data = rs.data[key];
                     }
                     $(v).find('input').each(function(index, input) {
                         if (index == 0 || index == 1) {
                             $(input).val(_data[index]);
                         }
                     })
                 })
             }
             alert('提取完成')
         }
     })
 })

 function is_empty_object(obj) {
     for (var k in obj) {
         return false;
     }
     return true;
 }