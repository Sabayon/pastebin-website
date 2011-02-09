
function package_search(form_name,search_input,dest_div) {
    if (document.getElementById(search_input).value.length > 1) {
        completeAHAH.likeSubmit('/packages/search', 'POST', form_name, dest_div, packages_loading_html);
    }
}

function load_depends(idpackage,arch,product,repo,branch,dest_div) {
    completeAHAH.ahah('/packages/depends?idpackage='+idpackage+'&arch='+arch+'&product='+product+'&branch='+branch+'&repo='+repo, dest_div, null, 'get', null);
}

function load_content(idpackage,arch,product,repo,branch,dest_div) {
        completeAHAH.ahah('/packages/content?idpackage=' + idpackage + '&arch=' + arch + '&product=' + product + '&branch=' + branch + '&repo=' + repo, dest_div, null, 'get', null);
}

function get_packages_stats(dest_div) {
    completeAHAH.ahah('/packages/stats', dest_div, null, 'get', null, packages_loading_html);
}

function get_packages_home(dest_div) {
    completeAHAH.ahah('/packages/home', dest_div, null, 'get', null, packages_loading_html);
}

function get_packages_home_string(dest_div,mystring) {
    completeAHAH.ahah('/packages/home?searchstring='+mystring, dest_div, null, 'get', null, packages_loading_html);
}

function get_package_data(formname, where, image, idpackage, branch, repoid, ugc_count_class) {

    short_el = document.getElementById('shortinfo_'+idpackage+'_'+branch+'_'+repoid);
    extra_el = document.getElementById('extrainfo_'+idpackage+'_'+branch+'_'+repoid);
    imgFile = document[image];
    imgElem = document.getElementById(image);
    if ((imgElem.value == "0") || (imgElem.value != "1") ) {
        imgFile.src = "/images/packages/list-remove.png";
        // save old content into garbage_idpackage
        if (short_el) {
            short_el.value = document.getElementById(where).innerHTML;
        }
        if ((extra_el.value == "") || (!short_el)) {
            completeAHAH.likeSubmit('/packages/extrainfo', 'POST', formname, where, packages_loading_html);
        } else {
            document.getElementById(where).innerHTML = extra_el.value;
        }
        //spin = true;
        imgElem.value = "1";
    } else {
        imgFile.src = "/images/packages/list-add.png";
        extra_el.value = document.getElementById(where).innerHTML;

        // update documents count when showing shortinfo back
        docs_count_elems = document.getElementsByClass(ugc_count_class);
        docs_cur_val = 0;
        for (idx = 0; idx < 1; idx++) {
            cur_val = docs_count_elems[idx].innerHTML;
            docs_cur_val = parseInt(cur_val);
        }
        document.getElementById(where).innerHTML = short_el.value;

        docs_count_elems = document.getElementsByClass(ugc_count_class);
        for (idx = 0; idx < docs_count_elems.length; idx++) {
            docs_count_elems[idx].innerHTML = docs_cur_val;
        }

        imgElem.value = "0";
    }

}

function load_categories(dest_div) {
    completeAHAH.ahah('/packages/categories', dest_div, null, 'get', null, packages_loading_html);
}

function load_releases(dest_div) {
    completeAHAH.ahah('/packages/releases', dest_div, null, 'get', null, packages_loading_html);
}

function load_release(branch,product,repo,arch,dest_div) {
        completeAHAH.ahah('/packages/release?branch=' + branch + '&arch=' + arch + '&product=' + product + '&repo=' + repo, dest_div, null, 'get', null, packages_loading_html);
}

function show_release(form_name,dest_div) {
    completeAHAH.likeSubmit('/packages/show_release', 'POST', form_name, dest_div, packages_loading_html);
}

function show_categories(form_name,dest_div) {
    completeAHAH.likeSubmit('/packages/show_categories', 'POST', form_name, dest_div, packages_loading_html);
}

function load_category(cat, product, repo, arch) {
    listElem = document.getElementById('li_'+cat);
    if (listElem.value == "0") {
        listElem.style.listStyleImage = "url('/images/packages/list-remove-small.png')";
        if (document.getElementById('subtree_'+cat).value == "") {
            spin = false;
            completeAHAH.ahah('/packages/category?cat='+cat+'&product='+product+'&arch='+arch+'&repo='+repo, 'info_'+cat, null, 'get', null);
            spin = true;
        } else {
            document.getElementById('info_'+cat).innerHTML = document.getElementById('subtree_'+cat).value;
        }
        listElem.value = "1";
    } else {
        listElem.style.listStyleImage = "url('/images/packages/list-add-small.png')";
        document.getElementById('subtree_'+cat).value = document.getElementById('info_'+cat).innerHTML;
        document.getElementById('info_'+cat).innerHTML = '';
        listElem.value = "0";
    }
}

function load_advisory(atom,repo,dest_div) {
    completeAHAH.ahah('/packages/getadvisory?atom='+atom+'&repo='+repo, dest_div, null, 'get', null);
}

function load_advisories(dest_div) {
        completeAHAH.ahah('/packages/advisories', dest_div, null, 'get', null, packages_loading_html);
}

function set_stars_rating(item,elem_prefix,vote) {
    item.style.cursor = "pointer";
    var myvote = parseInt(vote);
    for (i=1; i<=myvote; i++) {
        imgdoc = document.getElementById(elem_prefix+i);
        if (imgdoc) {
            imgdoc.src = '/images/packages/star_selected.png';
        }
    }
    for (i=myvote+1; i<=5; i++) {
        imgdoc = document.getElementById(elem_prefix+i);
        if (imgdoc) {
            imgdoc.src = '/images/packages/star_empty.png';
        }
    }
}

function reset_stars_rating(item,elem_prefix,vote) {
    item.style.cursor = "default";
    var myvote = parseInt(vote);
    for (i=1; i<=myvote; i++) {
        imgdoc = document.getElementById(elem_prefix+i);
        if (imgdoc) {
            imgdoc.src = '/images/packages/star.png';
        }
    }
    for (i=myvote+1; i<=5; i++) {
        imgdoc = document.getElementById(elem_prefix+i);
        if (imgdoc) {
            imgdoc.src = '/images/packages/star_empty.png';
        }
    }
}

function submit_ugc_vote(pkgkey,user_id,vote,login_url,dest_div) {
    if (user_id == "0") {
        show_alert('${_("User Generated Content")}', '${_("<p>You need to login to make your vote count.</p>")}')
        return;
    }
    completeAHAH.ahah('/packages/vote?vote=' + vote + '&pkgkey=' + pkgkey, dest_div, null, 'get', null);
}

function ugc_select_doctype(select_elem,pkgkey,atom,mytitle,keywords,desc,repoid,product,arch,dest_div) {
    ugc_doctype = select_elem.value;
    title_cont = document.getElementById(mytitle).value;
    keywords_cont = document.getElementById(keywords).value;
    desc_cont = document.getElementById(desc).value;
    completeAHAH.ahah('/packages/show_ugc_add?ugc_doctype=' + ugc_doctype + '&pkgkey=' + pkgkey + '&atom=' + atom + '&repoid=' + repoid + '&product=' + product + '&arch=' + arch + '&title=' + title_cont + '&keywords=' + keywords_cont + '&description=' + desc_cont, dest_div, null, 'get', null, packages_loading_html);
}

var ugc_new_doc_counter = 0;
function ugc_send_document(form_name,dest_div,div_error,title_id,ugc_count_class,ugc_score_class) {

    title_cont = document.getElementById(title_id).value;
    dest_div_obj = document.getElementById(dest_div);
    err_obj = document.getElementById(div_error);
    form_obj = document.getElementById(form_name);

    function do_et_complete(response) {
        div_doc = document.getElementById('ugc-new-doc-'+ugc_new_doc_counter);
        if (string_startswith(response.toLowerCase(), '${_("Error").lower()}') || string_startswith(response.toLowerCase(),"internal server error")) {
            if (div_doc) {
                dest_div_obj.removeChild(div_doc);
                ugc_new_doc_counter -= 1;
            }
            err_obj.innerHTML = response;
        } else {
            err_obj.innerHTML = '';
            div_doc.innerHTML = response;
            docs_count_elems = document.getElementsByClass(ugc_count_class);
            for (idx = 0; idx < docs_count_elems.length; idx++) {
                cur_val = docs_count_elems[idx].innerHTML;
                cur_val = parseInt(cur_val);
                docs_count_elems[idx].innerHTML = cur_val + 1;
            }
            docs_score_elems = document.getElementsByClass(ugc_score_class);
            max_score = 0;
            for (idx = 0; idx < docs_score_elems.length; idx++) {
                cur_val = docs_score_elems[idx].innerHTML;
                cur_val = parseInt(cur_val);
                if (cur_val > max_score) { max_score = cur_val; }
            }
            for (idx = 0; idx < docs_score_elems.length; idx++) {
                docs_score_elems[idx].innerHTML = max_score;
            }
        }
    }

    function do_et_start() {
        if (title_cont.length < 5) {
            show_error('${_("What about the title?")}','${_("Please insert a proper title")}');
            return false;
        }
        ugc_new_doc_counter += 1;
        newdiv = document.createElement('div');
        newdiv.setAttribute('id', 'ugc-new-doc-'+ugc_new_doc_counter);
        dest_div_obj.appendChild(newdiv);
        completeAHAH.creaDIV('ugc-new-doc-'+ugc_new_doc_counter,packages_loading_html);
        return true;
    }

    return AIM.submit(form_obj, {'onStart' : do_et_start, 'onComplete' : do_et_complete});

}



function delete_ugc_doc(iddoc,err_div,dest_div) {
    err_obj = document.getElementById(err_div);
    dest_obj = document.getElementById(dest_div);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((!valid) || (string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
            err_obj.innerHTML = resp_txt;
        } else {
            dest_obj.innerHTML = '';
            err_obj.innerHTML = resp_txt;
        }
    }

    function do_et(valid) {
        if (valid) {
            completeAHAH.ahah('/packages/ugc_delete?iddoc=' + iddoc, err_div, null, 'get', null, packages_loading_html, on_complete = do_et_complete);
        }
    }

    show_confirm('${_("Are you sure?")}','${_("You want to <b>remove</b> this document, are you super sure?")}',do_et)

}

/*

    UGC

*/

function ugc_search(form_name,search_input,dest_div,offset,do_spin,spin_target,spin_type) {

    if ( spin_type == "1" ) {
        loading_html = packages_loading_html;
    } else {
        loading_html = undefined;
    }

    dest_obj = document.getElementById(dest_div);
    error_obj = document.getElementById(spin_target);

    function do_et_complete(valid, resp_txt, resp_code) {
        if ((valid) && (!string_startswith(resp_txt.toLowerCase(),'${_("Error").lower()}'))) {
                error_obj.innerHTML = '';
                dest_obj.innerHTML = resp_txt;
            } else {
                error_obj.innerHTML = "<span style='color: red; font-weight: bold'>"+resp_txt+"</span>";
            }
        }

    completeAHAH.likeSubmit('/packages/ugc_search?offset='+offset, 'POST', form_name, spin_target, loading_html, do_et_complete, do_spin, spin_target);
}

function get_ugc_home(dest_div) {
    completeAHAH.ahah('/packages/ugc', dest_div, null, 'get', null, packages_loading_html);
}

