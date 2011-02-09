var dashboard_loading_html = '<div style="width: 100%; margin-left: auto; margin-right: auto; text-align: center; margin-top: 40px; margin-bottom: 40px"><img border="0" src="/images/packages/wait.gif" alt="please wait" /></div>';

function save_user_profile(form_name, dest_div, button_id) {

    dest_obj = document.getElementById(dest_div);
    button_obj = document.getElementById(button_id);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            dest_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            dest_obj.innerHTML = "<span style='color: green; font-weight: bold'>"+resp_txt+"</span>";
        }
        button_obj.disabled = true;
    }

    completeAHAH.likeSubmit('/community/my/save_profile', 'POST', form_name, dest_div, undefined, do_et_complete, true, dest_div);

}

function save_user_email(form_name, dest_div, button_id) {

    dest_obj = document.getElementById(dest_div);
    button_obj = document.getElementById(button_id);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            dest_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            dest_obj.innerHTML = resp_txt;
        }
        button_obj.disabled = true;
    }

    completeAHAH.likeSubmit('/login/update_email', 'POST', form_name, dest_div, undefined, do_et_complete, true, dest_div);

}

function save_user_password(form_name, dest_div, button_id) {

    dest_obj = document.getElementById(dest_div);
    button_obj = document.getElementById(button_id);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            dest_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            dest_obj.innerHTML = resp_txt;
        }
        button_obj.disabled = true;
    }

    completeAHAH.likeSubmit('/login/update_password', 'POST', form_name, dest_div, undefined, do_et_complete, true, dest_div);

}

function save_document_changes(form_name, dest_div) {
    dest_obj = document.getElementById(dest_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            dest_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            dest_obj.innerHTML = resp_txt;
        }
    }

    completeAHAH.likeSubmit('/pages/edit', 'POST', form_name, dest_div, undefined, do_et_complete, true, dest_div);

}

function change_document_status(pages_id, new_state, dest_div) {
    dest_obj = document.getElementById(dest_div);
    completeAHAH.ahah('/pages/change_status?pages_id=' + pages_id + '&new_state=' + new_state, dest_div, null, 'get', null, undefined, true, dest_div);
}

function remove_document_page(pages_id, page_num, dest_div, error_div) {
    dest_obj = document.getElementById(dest_div);
    error_obj = document.getElementById(error_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            error_obj.innerHTML = '';
            dest_obj.innerHTML = '';
        }
    }

    function do_et(valid) {
        if (valid) {
            completeAHAH.ahah('/pages/delete?pages_id=' + pages_id + '&page_num=' + page_num, error_div, null, 'get', null, undefined, do_et_complete, true, error_div);
        }
    }
    show_confirm('${_("Are you sure?")}','${_("You want to <b>remove</b> this document, are you super sure?")}',do_et);

}

function add_document_page(pages_id,page_num,new_div_mtx,dest_div,tbd_div) {

    dest_div_obj = document.getElementById(dest_div);
    tbd_div_obj = document.getElementById(tbd_div);
    new_div_name = new_div_mtx+pages_id+"-"+page_num;
    newdiv = document.createElement('div');
    newdiv.setAttribute('id', new_div_name);
    dest_div_obj.appendChild(newdiv);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((valid) && (!string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            tbd_div_obj.innerHTML = '';
            tinyMCE.execCommand("mceAddControl", true, "page-docs-intro-"+pages_id+"-"+page_num);
            tinyMCE.execCommand("mceAddControl", true, "page-docs-body-"+pages_id+"-"+page_num);
        } else {
            dest_div_obj.removeChild(newdiv);
        }
    }

    completeAHAH.ahah('/pages/new_page_num?pages_id=' + pages_id + '&page_num=' + page_num, new_div_name, null, 'get', null, dashboard_loading_html, do_et_complete, true, new_div_name);
}

function insert_document(form_name,dest_div) {
    dest_obj = document.getElementById(dest_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            dest_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            dest_obj.innerHTML = resp_txt;
        }
    }

    function do_et(valid) {
        if (valid) {
            completeAHAH.likeSubmit('/pages/insert', 'POST', form_name, dest_div, undefined, do_et_complete, true, dest_div);
        }
    }
    show_confirm('${_("Are you sure?")}','${_("You want to <b>add</b> this document, are you sure?")}',do_et);

}

function reload_dashboard_pages_navigation(pages_id, dest_div) {

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((valid) && (!string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            page_num = 0;
            while (page_num < 1000) {
                intro_id = "page-docs-intro-"+pages_id+"-"+page_num;
                content_id = "page-docs-body-"+pages_id+"-"+page_num;
                if (!document.getElementById(intro_id)) {
                    break;
                }
                tinyMCE.execCommand("mceAddControl", true, intro_id);
                tinyMCE.execCommand("mceAddControl", true, content_id);
                page_num++;
            }
        }
    }

    completeAHAH.ahah('/community/my/get_page_info?pages_id=' + pages_id, dest_div, null, 'get', null, undefined, do_et_complete, true, dest_div);
}

function delete_mirror(mirrors_id,dest_div,error_div) {

    dest_obj = document.getElementById(dest_div);
    error_obj = document.getElementById(error_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((valid) && (!string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
                dest_obj.innerHTML = resp_txt;
                error_obj.innerHTML = '';
            } else {
                error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
            }
        }

    function do_et(valid) {
        if (valid) {
            completeAHAH.ahah('/mirrors/delete?mirrors_id=' + mirrors_id, error_div, null, 'get', null, undefined, do_et_complete, true, error_div);
        }
    }
    show_confirm('${_("Are you sure?")}','${_("You want to <b>remove</b> this mirror, are you sure?")}',do_et);
}

function edit_mirror(form_name,dest_div) {

    function do_et(valid) {
        if (valid) {
            completeAHAH.likeSubmit('/mirrors/edit', 'POST', form_name, dest_div, undefined, undefined, true, dest_div);
        }
    }

    show_confirm('${_("Are you sure?")}','${_("You want to <b>edit</b> this mirror, are you sure?")}',do_et);

}

function add_mirror(form_name,dest_div) {

    function do_et(valid) {
        if (valid) {
            completeAHAH.likeSubmit('/mirrors/insert', 'POST', form_name, dest_div, undefined, undefined, true, dest_div);
        }
    }

    show_confirm('${_("Are you sure?")}','${_("You want to <b>add</b> this mirror, are you sure?")}',do_et);

}

function delete_mirror_link(mirror_links_id, dest_div, error_div) {

    dest_obj = document.getElementById(dest_div);
    error_obj = document.getElementById(error_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((valid) && (!string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
                dest_obj.innerHTML = resp_txt;
                error_obj.innerHTML = '';
            } else {
                error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
            }
    }

    function do_et(valid) {
        if (valid) {
            completeAHAH.ahah('/mirrors/delete_mirror_links_id?mirror_links_id=' + mirror_links_id, error_div, null, 'get', null, undefined, do_et_complete, true, error_div);
        }
    }

    show_confirm('${_("Are you sure?")}','${_("You want to <b>delete</b> this mirror link, are you sure?")}',do_et);
}

mirror_links_counter = 0;
function add_mirror_link(mirrors_id, dest_div_container, new_div_prefix) {

    dest_obj = document.getElementById(dest_div_container);

    mirror_links_counter += 1;
    new_div_name = new_div_prefix+mirror_links_counter;
    newdiv = document.createElement('div');
    newdiv.setAttribute('id', new_div_name);
    dest_obj.appendChild(newdiv);

    function do_et(mirror_link) {
        if (mirror_link) {
            completeAHAH.ahah('/mirrors/add_mirror_link?mirrors_id=' + mirrors_id + '&mirror_link=' + escape(mirror_link), new_div_name, null, 'get', null, undefined, undefined, true, new_div_name);
        }
    }

    show_input_box('${_("New mirror link")}', '${_("Insert the mirror link you want to add")}', '', do_et);

}

function reload_shots(dest_div) {
    completeAHAH.ahah('/screenshots/show_shots?edit=1', dest_div, null, 'get', null, dashboard_loading_html, undefined, true, dest_div);
}

function insert_screenshot(form_name, dest_div) {

    form_obj = document.getElementById(form_name);
    dest_div_obj = document.getElementById(dest_div);

    function do_et_start() {
        completeAHAH.creaDIV('do-new-shots-error');
        return true;
    }

    function do_et_complete(response) {
        dest_div_obj.innerHTML = response;
        reload_shots('do-shots-show');
    }

    return AIM.submit(form_obj, {'onStart' : do_et_start, 'onComplete' : do_et_complete});

}

function remove_screenshots(shots_name, dest_div, error_div) {

    dest_obj = document.getElementById(dest_div);
    error_obj = document.getElementById(error_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((valid) && (!string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
                dest_obj.innerHTML = resp_txt;
                error_obj.innerHTML = '';
            } else {
                error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
            }
    }

    function do_et(valid) {
        if (valid) {
            completeAHAH.ahah('/screenshots/delete?name=' + escape(shots_name), error_div, null, 'get', null, undefined, do_et_complete, true, error_div);
        }
    }

    show_confirm('${_("Are you sure?")}','${_("You want to <b>delete</b> this set of screenshots, are you sure?")}',do_et);
}

function rename_screenshots(old_shots_name, dest_div, error_div) {

    error_obj = document.getElementById(error_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((valid) && (!string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
                reload_shots('do-shots-show');
            } else {
                error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
            }
    }

    function do_et(new_name) {
        if (new_name) {
            completeAHAH.ahah('/screenshots/rename?old_name=' + escape(old_shots_name) + '&new_name=' + escape(new_name), error_div, null, 'get', null, undefined, do_et_complete, true, error_div);
        }
    }

    show_input_box('${_("Rename screenshots set")}', '${_("Type the new name and cross fingers")}', old_shots_name, do_et);

}

new_pinboards_counter = 0;
function insert_pinboard(form_name,div_container,error_div) {

    error_obj = document.getElementById(error_div);
    div_container_obj = document.getElementById(div_container);

    new_pinboards_counter += 1;
    new_div_name = div_container+"-"+new_pinboards_counter;
    newdiv = document.createElement('div');
    newdiv.setAttribute('id', new_div_name);
    div_container_obj.appendChild(newdiv);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
            div_container_obj.removeChild(newdiv);
            new_pinboards_counter -= 1;
        } else {
            error_obj.innerHTML = '';
            newdiv.innerHTML = resp_txt;
        }
    }

    completeAHAH.likeSubmit('/pinboard/edit', 'POST', form_name, error_div, undefined, do_et_complete, true, error_div);

}

function edit_pinboard(form_name,dest_div,error_div) {

    dest_obj = document.getElementById(dest_div);
    error_obj = document.getElementById(error_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            dest_obj.innerHTML = resp_txt;
        }
    }

    completeAHAH.likeSubmit('/pinboard/edit', 'POST', form_name, error_div, undefined, do_et_complete, true, error_div);

}

function delete_pinboard(pinboards_id,dest_div,error_div) {

    dest_obj = document.getElementById(dest_div);
    error_obj = document.getElementById(error_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            dest_obj.innerHTML = resp_txt;
        }
    }

    function do_et(valid) {
        if (valid) {
            completeAHAH.ahah('/pinboard/delete?pinboards_id=' + pinboards_id, error_div, null, 'get', null, undefined, do_et_complete, true, error_div);
        }
    }

    show_confirm('${_("Are you sure?")}','${_("You want to <b>delete</b> this pinboard, are you sure?")}',do_et);

}

new_pinboards_elem_counter = 0;
function insert_pinboard_element(form_name,div_container,error_div,no_pin_div) {

    error_obj = document.getElementById(error_div);
    div_container_obj = document.getElementById(div_container);
    no_pin_div_obj = document.getElementById(no_pin_div);

    new_pinboards_elem_counter += 1;
    new_div_name = div_container+"-"+new_pinboards_elem_counter;
    newdiv = document.createElement('div');
    newdiv.setAttribute('id', new_div_name);
    div_container_obj.appendChild(newdiv);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
            div_container_obj.removeChild(newdiv);
            new_pinboards_elem_counter -= 1;
        } else {
            error_obj.innerHTML = '';
            newdiv.innerHTML = resp_txt;
            no_pin_div_obj.innerHTML = '';
        }
    }

    completeAHAH.likeSubmit('/pinboard/edit_element', 'POST', form_name, error_div, undefined, do_et_complete, false, error_div);

}

function edit_pinboard_element(form_name,dest_div,error_div) {

    error_obj = document.getElementById(error_div);
    dest_obj = document.getElementById(dest_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            dest_obj.innerHTML = resp_txt;
        }
    }

    completeAHAH.likeSubmit('/pinboard/edit_element', 'POST', form_name, error_div, undefined, do_et_complete, false, error_div);

}

function delete_pinboard_element(pinboards_id,pinboards_data_id,dest_div,error_div) {

    error_obj = document.getElementById(error_div);
    dest_obj = document.getElementById(dest_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            dest_obj.innerHTML = resp_txt;
        }
    }

    function do_et(valid) {
        if (valid) {
            completeAHAH.ahah('/pinboard/delete_element?pinboards_id=' + pinboards_id + '&pinboards_data_id=' + pinboards_data_id, error_div, null, 'get', null, undefined, do_et_complete, false, error_div);
        }
    }

    show_confirm('${_("Are you sure?")}','${_("You want to <b>delete</b> this pinboard element, are you sure?")}',do_et);
}

function remove_all_my_pinboard_shares(pinboards_id,dest_div,error_div) {

    error_obj = document.getElementById(error_div);
    dest_obj = document.getElementById(dest_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            error_obj.innerHTML = '';
            dest_obj.innerHTML = resp_txt;
        }
    }

    function do_et(valid) {
        if (valid) {
            completeAHAH.ahah('/pinboard/delete_pinboard_shares?pinboards_id=' + pinboards_id, error_div, null, 'get', null, undefined, do_et_complete, true, error_div);
        }
    }

    show_confirm('${_("Are you sure?")}','${_("You want to <b>delete</b> all the shares below, are you sure?")}',do_et);

}

function update_pinboard_share_status(pinboard_shares_id,select_id,error_div) {

    error_obj = document.getElementById(error_div);
    select_obj = document.getElementById(select_id);
    new_status = select_obj.options[select_obj.selectedIndex].value;

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            error_obj.innerHTML = '';
        }
    }

    completeAHAH.ahah('/pinboard/update_pinboard_share_status?pinboard_shares_id=' + pinboard_shares_id + '&status=' + new_status, error_div, null, 'get', null, undefined, do_et_complete, true, error_div);

}

function remove_my_pinboard_share(pinboard_shares_id,pinboards_id,dest_div,error_div,all_shares_div) {

    error_obj = document.getElementById(error_div);
    dest_obj = document.getElementById(dest_div);
    all_shares_obj = document.getElementById(all_shares_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            error_obj.innerHTML = '';
            if (resp_txt == '0') {
                all_shares_obj.innerHTML = '';
            }
        }
    }

    function do_et(valid) {
        if (valid) {
            completeAHAH.ahah('/pinboard/delete_pinboard_share?pinboard_shares_id=' + pinboard_shares_id + '&pinboards_id=' + pinboards_id, error_div, null, 'get', null, undefined, do_et_complete, true, error_div);
        }
    }

    show_confirm('${_("Are you sure?")}','${_("You want to <b>delete</b> this share, are you sure?")}',do_et);

}

new_poll_option_counter = 0;
function add_poll_option(form_name,pages_id,dest_div_container,error_div) {

    error_obj = document.getElementById(error_div);
    dest_div_container_obj = document.getElementById(dest_div_container);
    new_poll_option_counter += 1;
    new_div_name = dest_div_container+'_'+pages_id+'_'+new_poll_option_counter;
    newdiv = document.createElement('div');
    newdiv.setAttribute('id', new_div_name);
    dest_div_container_obj.appendChild(newdiv);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
            dest_div_container_obj.removeChild(newdiv);
            new_pinboards_elem_counter -= 1;
        } else {
            error_obj.innerHTML = '';
            newdiv.innerHTML = resp_txt;
        }
    }

    completeAHAH.likeSubmit('/pages/add_poll_option', 'POST', form_name, error_div, undefined, do_et_complete, true, error_div);

}

function edit_poll_option(poll_options_id,dest_div,error_div) {

    error_obj = document.getElementById(error_div);
    dest_obj = document.getElementById(dest_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),"error:"))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            error_obj.innerHTML = '';
            dest_obj.innerHTML = resp_txt;
        }
    }

    function do_et(new_name) {
        if (new_name) {
            completeAHAH.ahah('/pages/edit_poll_option_name?poll_options_id=' + poll_options_id + '&option_name=' + encodeURIComponent(new_name), error_div, null, 'get', null, undefined, do_et_complete, true, error_div);
        }
    }

    show_input_box('${_("Enter a new name")}','${_("You want to <b>edit</b> this option name")}',dest_obj.innerHTML,do_et);

}

function delete_poll_option(poll_options_id,dest_div,error_div) {

    error_obj = document.getElementById(error_div);
    dest_obj = document.getElementById(dest_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),"error:"))) {
            error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
        } else {
            dest_obj.innerHTML = resp_txt;
        }
    }

    function do_et(valid) {
        if (valid) {
            completeAHAH.ahah('/pages/delete_poll_option_name?poll_options_id=' + poll_options_id, error_div, null, 'get', null, undefined, do_et_complete, true, error_div);
        }
    }

    show_confirm('${_("Are you sure?")}','${_("You want to <b>delete</b> this poll option, are you sure?")}',do_et);

}