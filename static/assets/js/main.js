$.ajaxSetup({
	cache : false
});
var showTopAlert = function(level, title, content) {
	var levelCls = level == 'success' ? "alert alert-block alert-success" : "alert alert-block alert-danger";
	var alerts = $("#alerts");

	var c = [];
	// c.push('<button type="button" class="close" data-dismiss="alert">');
	// c.push('<i class="ace-icon fa fa-times"></i>');
	// c.push('</button>');
	c.push('<strong>');
	c.push(level == 'success' ? '<i class="ace-icon fa fa-check"></i>' : '<i class="ace-icon fa fa-times"></i>');
	c.push(title);
	c.push('</strong>\n');
	c.push(content);
	c.push('<br/>')
	alerts.removeClass().addClass(levelCls);
	alerts.html(c.join('\n'));
	alerts.css({
		position: 'absolute',
		top: 50,
		right:0,
		opacity : 0,
		"z-index" : 100000
	});
	alerts.show(function(){
		alerts.animate({
			opacity : 1
		},100,function(){
			var self = this;
			var timroutId = window.setTimeout(function() {
				$(self).animate({
					opacity : 0
				},1000, function() {
					$(self).hide(function(){
						window.clearTimeout(timroutId);
					});
				});
			}, 2000);
		});
	});
}

var serviceResponseJsonHandler = function(data, form) {
	if (data.alert && data.alert.title) {
		var alert = data.alert;
		showTopAlert(alert.level, alert.title, alert.content);
	}
	if (data.fieldValidations != null && data.fieldValidations.length > 0 && form) {
		data.fieldValidations.map(function(d) {
			var group = form.find("[name='" + d.fieldName + "']").parents("div.control-group");
			group.find("span.field-error").remove();
			group.find("div.controls2").append("<span class='field-error'>" + d.message + "</span>");
		});
	}
	if (data.callBack) {
		eval(data.callBack);
	}
};

var optionFiledValueInit = function(node){
	node.find("select[data-selectinit-value]").each(function() {
    var selectNode = $(this);
    var initValue = selectNode.attr("data-selectinit-value").split(",");
    initValue.map(function(d) {
      selectNode.find("option[value='" + d + "']").attr("selected", "selected");
    });
  });
  // 处理checkBox
	node.find("div[data-checkboxinit-value]").each(function() {
    var checkBoxNode = $(this);
    var initValue = checkBoxNode.attr("data-checkboxinit-value");
    var disable = checkBoxNode.attr("data-disabled");
    var inputName = checkBoxNode.attr("data-input-name");
    var values = JSON.parse(initValue);
    values.map(function(value) {
      var checkboxs = checkBoxNode.find("input[name='" + inputName + "']:checkbox[value='" + value + "']").attr("checked", true);
      if (disable == "true") {
        checkboxs.attr("disabled", "disabled");
      }
    });
  });
}

var registAjaxModal = function(){
	$(document).on('click.modal.api','[data-ajax-modal]',function(){
		var $this = $(this);
        var href = $this.attr("data-ajax-modal");

		Action.htmAsyncAct(href,function(data){

		},function(data){
			bootbox.dialog({
					size: "large",
					title: "Edit Job",
					message: data,
					buttons:{
						cancel: {
							label: "Cancel", // 自定义按钮名字
							className: "btn-default",  // 自定义类名
							callback: function(){  // 自定义回调函数

							}
						},
						ok: {
							label: "Save",
							className: "btn-primary",
							callback: function(){

							}
						}
					}
			})
		});
	});
}



var registAjaxService = function(){
	$(document).on('click.modal.api','[data-ajax-service]',function(){
		var self = $(this);
		var confirm = self.attr("data-confirm");
		var sendUrl = self.attr('data-ajax-service');
		var callback = self.attr('data-callback');
		bootbox.confirm({
				message: confirm,
				callback: function(result){
					if(result === true) {
						Action.jsonAsyncAct(sendUrl,function(data){
							if (data) {
								showTopAlert(data.level, data.title, data.msg);
							}
							if (callback) {
								eval(callback);
							}
						});
					}
				}
			})
	});
}

function regeditAjaxPage() {
	  $(document).on("click", "[data-ajax-page]", function(event) {
	    event.preventDefault();
	    var _cp_h = $(this).attr('data-ajax-page');
	    Action.htmAsyncAct(_cp_h,function(data){
			$("#_content_").html("<div class=\"loading\"></div>");
		},function(data){
			$("#_content_").empty().hide().html(data).slideDown();
			optionFiledValueInit($("#_content_"));
		});
	  });
	}

var registAjaxFormSubmit = function(){
	$(document).on('submit.data-api','form',function(event){
		var self = $(this);
		self.find("div.control-group").find("span.field-error").detach();
	    event.preventDefault();
	    Action.jsonAsyncActByData(self.attr("action"), self.serialize(), function(data) {
	    	serviceResponseJsonHandler(data,self);
	    });
	});
}

var initDataTable = function(id, param, ajaxUrl, serverSite){
	var params = {
		"sErrMode":"throw",
		"sServerMethod" : "POST",
		"bDeferRender" : true,
		"fnDrawCallback" : function() {
		},
		"sScrollXInner" : "110%", // 表格的内容宽度
		"bScrollCollapse" : false, // 当显示的数据不足以支撑表格的默认的高度时，依然显示纵向的滚动条。(默认是false)
		"bPaginate" : true, // 是否显示分页
		"bLengthChange" : true, // 每页显示的记录数
		"bFilter" : true, // 搜索栏
		"bSort" : true, // 是否支持排序功能
		"bInfo" : true, // 显示表格信息
		"bAutoWidth" : false, // 自适应宽度
		"bStateSave" : true, // 保存状态到cookie *************** 很重要 ， 当搜索的时候页面一刷新会导致搜索的消失。使用这个属性就可避免了
		"sPaginationType" : "full_numbers", // 分页，一共两种样式，full_numbers和two_button(默认),这里采用自定义的
		"bProcessing" : true,
		"iDisplayLength": 10,
		"ordering":false
	};
	if (param != null) {
		for ( var i in param) {
			params[i] = param[i];
		}
	}
	if (ajaxUrl != null) {
		params.bProcessing = true, params.sAjaxSource = ajaxUrl;
	}
	if (serverSite != null) {
		params.bProcessing = true, params.bServerSide = true, params.sAjaxSource = ajaxUrl;
	}
	return $('#' + id).dataTable(params);
}


var dateFtt = function(fmt,date) {
  var o = {
    "M+" : date.getMonth()+1,//月份
    "d+" : date.getDate(),//日
    "h+" : date.getHours(),//小时
    "m+" : date.getMinutes(),//分
    "s+" : date.getSeconds(),//秒
    "q+" : Math.floor((date.getMonth()+3)/3),//季度
    "S"  : date.getMilliseconds()//毫秒
  };
  if(/(y+)/.test(fmt))
    fmt=fmt.replace(RegExp.$1, (date.getFullYear()+"").substr(4 - RegExp.$1.length));
  for(var k in o)
    if(new RegExp("("+ k +")").test(fmt))
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
  return fmt;
};

$(function() {
	// registAjaxModal();
	registAjaxService();
	regeditAjaxPage();
	registAjaxFormSubmit();
});