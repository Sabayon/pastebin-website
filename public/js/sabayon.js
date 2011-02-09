var packages_loading_html = '<div style="width: 100%; margin-left: auto; margin-right: auto; text-align: center; margin-top: 40px; margin-bottom: 40px"><img border="0" src="/images/packages/wait.gif" alt="please wait" /></div>';

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


function do_login(form_name,dest_div) {
    completeAHAH.likeSubmit('/login/submit', 'POST', form_name, dest_div);
}

function do_logout_get(dest_div) {
    completeAHAH.ahah('/login/logout', dest_div, null, 'get', null);

}

function do_logout(form_name,dest_div) {
    completeAHAH.likeSubmit('/login/logout', 'POST', form_name, dest_div);
}

function give_comment_point(user_id, comments_id, dest_div) {
    completeAHAH.ahah('/comments/set_point?user_id=' + user_id + '&comments_id=' + comments_id, dest_div, null, 'get', null);
}

var new_comments_div_counter = 0;
function send_comment(form_name, text_area, dest_div, error_div) {
    text_data = document.getElementById(text_area).value;
    if (text_data) {
        dest_div_obj = document.getElementById(dest_div);
        new_comments_div_counter += 1;
        newdiv = document.createElement('div');
        newdiv.setAttribute('id', new_comments_div_counter);
        dest_div_obj.appendChild(newdiv);
        completeAHAH.likeSubmit('/comments/insert', 'POST', form_name, new_comments_div_counter);
    } else {
        obj = document.getElementById(error_div);
        if (obj) { obj.innerHTML = '${_("Hey! Write something!")}'; }
    }
}

function delete_comment(comments_id, dest_div) {
    completeAHAH.ahah('/comments/delete?comments_id=' + comments_id, dest_div, null, 'get', null);
}

function edit_comment(form_name, text_area, dest_div, error_div) {
    text_data = document.getElementById(text_area).value;
    if (text_data) {
        completeAHAH.likeSubmit('/comments/edit', 'POST', form_name, dest_div);
    } else {
        obj = document.getElementById(error_div);
        if (obj) { obj.innerHTML = '${_("Hey! Write something!")}'; }
    }
}

function show_edit_comment(comments_id, dest_div) {
    completeAHAH.ahah('/comments/show_edit?comments_id=' + comments_id, dest_div, null, 'get', null);
}

function set_text_on_element(elem_id,error) {
    document.getElementById(elem_id).innerHTML = error;
}

function register_user(form_name,reload_ok_div,dest_div,submit_button) {
    // check username
    user_len = document.getElementById('username').value.length;
    if ((user_len > 20) || (user_len < 3)) {
        set_text_on_element('registration-error-box','${_("Wrong username!")}');
        return;
    }

    // check email
    email = document.getElementById('email').value;
    email_confirm = document.getElementById('email_confirm').value;
    if (!(check_email(email) && check_email(email_confirm)) || (email != email_confirm)) {
        set_text_on_element('registration-error-box','${_("Wrong e-mail!")}');
        return;
    }

    // check password
    password = document.getElementById('new_password').value;
    password_confirm = document.getElementById('password_confirm').value;

    if (password != password_confirm) {
        set_text_on_element('registration-error-box','Password mismatch between fields!');
        return;
    }

    if ((password.length < 6) || (password.length > 30)) {
        set_text_on_element('registration-error-box','${_("Wrong password length!")}');
        return;
    }

    // checkbox check
    cbox = document.getElementById('registration_agreement_check').checked;
    if (!cbox) {
        set_text_on_element('registration-error-box','${_("You must accept the Registration Agreement")}');
        return;
    }

    dest_obj = document.getElementById(dest_div);
    submit_obj = document.getElementById(submit_button);
    reload_obj = document.getElementById(reload_ok_div);
    submit_obj.disabled = true;

    function do_et_complete(valid, resp_txt, resp_code) {
        submit_obj.disabled = false;
        if ((valid) && (!string_startswith(resp_txt.toLowerCase(),"invalid"))) {
            dest_obj.innerHTML = '';
            reload_obj.innerHTML = resp_txt;
        } else {
            // reload recaptcha
            Recaptcha.reload();
        }
    }

    completeAHAH.likeSubmit('/login/register_submit', 'POST', form_name, dest_div, undefined, do_et_complete);

}

function search_users(form_name, dest_div, spin_div) {

    spin_obj = document.getElementById(spin_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        spin_obj.innerHTML = '';
    }

    completeAHAH.likeSubmit('/community/search_users', 'POST', form_name, dest_div, undefined, do_et_complete, true, spin_div);
}

function registration_advantages() {
    show_info("${_('Register today, make your opinion count!')}","<br/>${_('By registering, you will be able to access to <b>many advantages</b>, like writing <b>your opinions</b> on our pages, finding <b>the help you need</b> on the forums, <b>contributing</b> to our Wiki, <b>voting</b> your favourite applications, <b>adding</b> comments, screenshots and owning <b>your blog</b> and <b>exclusive online clipboard</b> (Pastebin and Pixdiff). So, what are you waiting for? Enter <b>the Sabayon experience</b>!')}");
}

function where_to_buy() {
    show_info("${_('Online Stores')}","${_("You can find our Online Stores on the right column of <a href='/'>our front page</a>. If you want to become one, send an e-mail to <b><a href='mailto:lxnay@sabayonlinux.org'>lxnay at sabayonlinux dot org</a></b>.")}");
}

function div_toggle_slide(div_id) {
    mydiv = document.getElementById(div_id);

    mydisp = mydiv.style.display;
    visible = true;
    if (mydisp == 'none') { visible = false; };
    if (visible) {
        mydiv.style.display = 'none';
    } else {
        mydiv.style.display = '';
    }
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
