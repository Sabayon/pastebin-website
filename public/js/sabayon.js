
if(!document.getElementsByClass) document.getElementsByClass = function(className) {
    for(var r = [], e = document.getElementsByTagName("*"), i = 0, j = e.length; i < j; i++) r.push(e[i]);
    return r.filter(function(e){return e.className.split(" ").some(function(n){return n===className})});
};

function show_alert(mytitle,mytext) {
    sexy = new SexyAlertBox();
    sexy.alert("<h1>"+mytitle+"</h1>"+mytext);
}

function show_error(mytitle,mytext) {
    sexy = new SexyAlertBox();
    sexy.error("<h1>"+mytitle+"</h1>"+mytext);
}

function show_info(mytitle,mytext) {
    sexy = new SexyAlertBox();
    sexy.info("<h1>"+mytitle+"</h1>"+mytext);
}

function show_confirm(mytitle,mytext,cb) {
    sexy = new SexyAlertBox();
    sexy.confirm("<h1>"+mytitle+"</h1>"+mytext, {onComplete: cb});
}

function show_input_box(mytitle, mytext, prefix, cb) {
    sexy = new SexyAlertBox();
    sexy.prompt("<h1>"+mytitle+"</h1>"+mytext, prefix, {onComplete: cb});
}

function show_select_box(mytitle, mytext, options, cb) {
    sexy = new SexyAlertBox();
    sexy.select("<h1>"+mytitle+"</h1>"+mytext, options, {onComplete: cb});
}

function check_textarea_maxlength(elem) {
    max_len = elem.getAttribute('maxlength');
    cur_len = elem.value.length;
    if (cur_len > max_len) {
        text_data = elem.value;
        elem.value = text_data.substring(0,max_len);
    }
}

function inItem(item) {
    item.style.cursor = "pointer";
}
function outItem(item) {
    item.style.cursor = "default";
}

function check_email(str) {
    var at="@"
    var dot="."
    var lat=str.indexOf(at)
    var lstr=str.length
    var ldot=str.indexOf(dot)
    if (str.indexOf(at)==-1){
        return false;
    }
    if (str.indexOf(at)==-1 || str.indexOf(at)==0 || str.indexOf(at)==lstr){
        return false;
    }
    if (str.indexOf(dot)==-1 || str.indexOf(dot)==0 || str.indexOf(dot)==lstr){
        return false;
    }
    if (str.indexOf(at,(lat+1))!=-1){
        return false;
    }
    if (str.substring(lat-1,lat)==dot || str.substring(lat+1,lat+2)==dot){
        return false;
    }
    if (str.indexOf(dot,(lat+2))==-1){
        return false;
    }
    if (str.indexOf(" ")!=-1){
        return false;
    }
    return true;
}

function string_startswith(s,pattern) {
    return s.indexOf(pattern) === 0;
}

function string_endswith(s,pattern) {
    var d = s.length - pattern.length;
    return d >= 0 && s.lastIndexOf(pattern) === d;
}

function image_resize(which, max) {
  var elem = document.getElementById(which);
  if (max == undefined) max = 100;
  if (elem.width > elem.height) {
    if (elem.width > max) elem.width = max;
  } else {
    if (elem.height > max) elem.height = max;
  }
}
