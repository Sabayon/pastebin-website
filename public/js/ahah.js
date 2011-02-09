// ==========================================================================
// @function		Complete AHAH function
// @author		Daniele Florio / Fabio Erculiani
// @site		www.gizax.it
// @version		1.2.0

// @thanksTo		Andrea Paiola,Walter Wlodarski,Scott Chapman,Fabio Erculiani

// (c) 2006 Daniele Florio <daniele@gizax.it>
// (c) 2010 Fabio Erculiani <lxnay@sabayonlinux.org>

// ==========================================================================

var completeAHAH = {

        loading : '<img border="0" src="/js/loading.png" alt="" />',

        ahah : function (url, target, delay, method, parameters, loading_html, on_complete, spin, spin_div) {

            if ( spin == undefined ) { spin = true; };
            spin_target = target;
            if ( spin_div != undefined ) { spin_target = spin_div; };

            if ( ( method == undefined ) || ( method == "GET" ) || ( method == "get" ) ){

                        if (spin) {
                            if (loading_html == undefined) {
                                loading_html = this.loading;
                            }
                            this.creaDIV(spin_target, loading_html);
                        }

                        if (window.XMLHttpRequest) {
                                req = new XMLHttpRequest();
                        } 
                        else if (window.ActiveXObject) {
                                req = new ActiveXObject("Microsoft.XMLHTTP");
                        }
                        if (req) {
                                req.onreadystatechange = function() {
                                        completeAHAH.ahahDone(url, target, delay, method, parameters, on_complete);
                                };
                                req.open(method, url, true);
                                req.send("");
                        }
                }
                if ( (method == "POST") || (method == "post") ){

                        if (spin) {
                            if (loading_html == undefined) {
                                loading_html = this.loading;
                            }
                            this.creaDIV(spin_target, loading_html);
                        }


                        if (window.XMLHttpRequest) {
                                req = new XMLHttpRequest();
                        } 
                        else if (window.ActiveXObject) {
                                req = new ActiveXObject("Microsoft.XMLHTTP");
                        }
                        if (req) {
                                req.onreadystatechange = function() {
                                        completeAHAH.ahahDone(url, target, delay, method, parameters, on_complete);
                                };
                                req.open(method, url, true);
                                req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                                req.send(parameters);
                            }
                }
        },

        creaDIV : function (target, html){

            if (html == undefined) {
                html = this.loading;
            }

            if (document.body.innerHTML){
                            document.getElementById(target).innerHTML = html;
            }
            else if (document.getElementById){
                            var element = document.getElementById(target);
                            var range = document.createRange();

                            range.selectNodeContents(element);
                            range.deleteContents();
                            element.appendChild(range.createContextualFragment(html));

            }
        },

        ahahDone : function (url, target, delay, method, parameters, on_complete) {
                if (req.readyState == 4) { 
                        element = document.getElementById(target);
                        if (req.status == 200) {
                                this.creaDIV(target, req.responseText);
                                if (on_complete != undefined) { on_complete(true, req.responseText, req.statusText); }
                        }
                        else {
                                this.creaDIV(target, "Server Error: " + req.statusText);
                                if (on_complete != undefined) { on_complete(false, req.responseText, req.statusText); }
                        }
                }
        },

        /*

        @@ parameters : 
        fileName	= name of your cgi or other
        method		= GET or POST, default is GET
        formName	= name of your form
        dynamicTarget	= name of your dynamic Target DIV or other

        @@ usage : 
        <form id="formName" action="javascript:completeAHAH.likeSubmit('fileName', 'method', 'formName', 'dynamicTarget');">

        */

        likeSubmit : function ( file, method, formName, target, loading_html, on_complete, spin, spin_div) {

                var the_form = document.getElementById(formName);
                var num = the_form.elements.length;
                var url = "";
                var radio_buttons = new Array();
                var nome_buttons = new Array();
                var check_buttons = new Array();
                var nome_buttons = new Array();

                // submit radio values
                var j = 0;
                var a = 0;
                for(var i=0; i < the_form.length; i++){
                        var temp = the_form.elements[i].type;
                        if ( (temp == "radio") && ( the_form.elements[i].checked) ) { 
                                nome_buttons[a] = the_form.elements[i].name;
                                radio_buttons[j] = the_form.elements[i].value; 
                                j++; 
                                a++;
                        }
                }
                for(var k = 0; k < radio_buttons.length; k++) {
                        url += nome_buttons[k] + "=" + radio_buttons[k] + "&";
                }

                // submit checkbox values
                var j = 0;
                var a = 0;
                for(var i=0; i < the_form.length; i++){
                        var temp = the_form.elements[i].type;
                        if ( (temp == "checkbox") && ( the_form.elements[i].checked) ) { 
                                nome_buttons[a] = the_form.elements[i].name;
                                check_buttons[j] = the_form.elements[i].value; 
                                j++; 
                                a++;
                        }
                }
                for(var k = 0; k < check_buttons.length; k++) {
                        url += nome_buttons[k] + "=" + check_buttons[k] + "&";
                }

                // submit all kind of input
                for (var i = 0; i < num; i++){	
                        var chiave = the_form.elements[i].name;
                        var valore = the_form.elements[i].value;
                        var tipo = the_form.elements[i].type;

                        if ( (tipo == "submit") || (tipo == "radio") || (tipo == "checkbox") ){}
                        else {
                            url += chiave + "=" + encodeURIComponent(valore) + "&";
                        }
                }

                var parameters = url;
                url = file + "?" + url;

                if (method == undefined) { 
                        method = "GET";
                }
                if (method == "GET") { 
                        this.ahah(url, target, '', method, '', loading_html, on_complete, spin, spin_div);
                }
                else {
                        this.ahah(file, target, '', method, parameters, loading_html, on_complete, spin, spin_div);
                }
        }

};
