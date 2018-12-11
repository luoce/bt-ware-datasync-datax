var a, Action = {
	ajsxSucc : function(b, c) {
		// b.msg && alert(b.msg);
		// b.callbackFun && eval(b.callbackFun);
		c && c(b)
	},
	jsonAsyncAct : function(b, c) {
		$.ajax({
					type : "POST",
					url : b,
					async : true,
					dataType : "json",
					success : function(d) {
						Action.ajsxSucc(d, c)
					},
					error : function() {
						alert("\u540e\u53f0\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
					}
				})
	},
	jsonAsyncActByData : function(b, c, d) {
		$.ajax({
					type : "POST",
					url : b,
					async : true,
					dataType : "json",
					data : c,
					success : function(e) {
						Action.ajsxSucc(e, d)
					},
					error : function(e) {
						alert(e.msg);
						alert("\u540e\u53f0\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
					}
				})
	},
	jsonAct : function(b, c) {
		$.ajax({
					type : "POST",
					url : b,
					async : false,
					dataType : "json",
					success : function(d) {
						Action.ajsxSucc(d, c)
					},
					error : function() {
						alert("\u540e\u53f0\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
					}
				})
	},
	jsonActByData : function(b, c, d) {
		$.ajax({
					type : "POST",
					url : b,
					async : false,
					dataType : "json",
					data : c,
					success : function(e) {
						Action.ajsxSucc(e, d)
					},
					error : function() {
						alert("\u540e\u53f0\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
					}
				})
	},
	getAsyncData : function(b) {
		var c;
		$.ajax({
					type : "POST",
					url : b,
					dataType : "json",
					async : true,
					success : function(d) {
						Action.ajsxSucc(d, null);
						c = d.rows
					},
					error : function() {
						alert("\u540e\u53f0\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
					}
				});
		return c
	},
	getAsyncData2 : function(b, c, d, e) {
		$.ajax({
					type : "POST",
					url : b,
					dataType : "json",
					async : true,
					data : c,
					success : function(f) {
						Action.ajsxSucc(f, e)
					},
					beforeSend : function(f) {
						d(f)
					},
					error : function() {
						alert("\u5f02\u6b65\u8bfb\u53d6\u6570\u636e\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
					}
				})
	},
	getData : function(b) {
		var c;
		$.ajax({
					type : "POST",
					url : b,
					dataType : "json",
					async : false,
					success : function(d) {
						Action.ajsxSucc(d, null);
						c = d.rows
					},
					error : function() {
						alert("\u540e\u53f0\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
					}
				});
		return c
	},
	getObjByUrl : function(b) {
		var c;
		$.ajax({
					type : "POST",
					url : b,
					dataType : "json",
					async : false,
					success : function(d) {
						Action.ajsxSucc(d, null);
						c = d
					},
					error : function() {
						alert("\u540e\u53f0\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
					}
				});
		return c
	},
	getObjByUrlandConditon : function(b, c) {
		var d;
		$.ajax({
					type : "POST",
					url : b,
					data : c,
					dataType : "json",
					async : false,
					success : function(e) {
						Action.ajsxSucc(e, null);
						d = e
					},
					error : function() {
						alert("\u540e\u53f0\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
					}
				});
		return d
	},
	htmAsyncAct : function(b, c, d){
		$.ajax({
			type : "GET",
			url : b,
			async : true,
			dataType : "html",
			beforeSend : function(e) {
				c(e)
			},
			success : function(e) {
				Action.ajsxSucc(e, d)
			},
			error : function() {
				alert("\u540e\u53f0\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
			}
		});
	},
	htmAct  : function(b, c, d){
		$.ajax({
			type : "GET",
			url : b,
			async : false,
			dataType : "html",
			beforeSend : function(e) {
				c(e)
			},
			success : function(e) {
				Action.ajsxSucc(d, e)
			},
			error : function() {
				alert("\u540e\u53f0\u51fa\u9519\uff0c\u8bf7\u67e5\u770b\u65e5\u5fd7")
			}
		});
	},
	getOptionsByUrl : function(b, c, d) {
		b += b.indexOf("?") == -1 ? "?rp=0" : "&rp=0";
		var e = [];
		b = Action.getObjByUrl(b);
		for ( var f = 0; f < b.rows.length; f++) {
			var g = {}, h = b.rows[f].cell;
			g.text = h[c];
			g.value = h[d];
			e.push(g)
		}
		return e
	},
	getParameter : function() {
		var b = new String(document.location), c = b.indexOf("?");
		return ret = c == -1 ? "" : b.substring(1 + c)
	},
	addParameter : function(b, c) {
		var d = "";
		return d = b.indexOf("?") == -1 ? b + "?" + c : b + "&" + c
	},
	getItemsByUrl : function(b, c, d) {
		if (b.indexOf("?") == -1)
			b += "?rp=0";
		else if (b.indexOf("rp=0") == -1)
			b += "&rp=0";
		b += "&needCloth=false";
		b = Action.getData(b);
		for ( var e = [], f = 0; f < b.length; f++) {
			var g = {};
			g.value = b[f].cell[c];
			g.text = b[f].cell[d];
			g.data = b[f].cell;
			e.push(g)
		}
		return e
	},
	getQueryString : function(b) {
		var c = location.href;
		c = c.toLowerCase();
		b = b.toLowerCase();
		if (c.indexOf("?") == -1)
			return "";
		c = c.split("?");
		c = c[c.length - 1];
		c = c.split("&");
		for ( var d = 0; d < c.length; d++) {
			var e = c[d].split("=");
			if (e[0] == b)
				return e[1]
		}
		return ""
	}
}