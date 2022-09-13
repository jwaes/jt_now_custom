/** @odoo-module */

import { get_cookie } from 'web.utils.cookies';
import { session } from '@web/session';

$(document ).ready(function() {
    const slct = $('select[name=country_id].s_website_form_input');
    if(slct.length){
        console.log("select is there");
        console.log(slct);

        if (session.geoip){
            console.log("country name is " + session.geoip_country_name);

            $('select[name=country_id].s_website_form_input option').filter(function(){
                console.log($(this).text())
                return $(this).text() == session.geoip_country_name;
            }).prop('selected',true);

        } else {
            console.log("no geoip found");
        }

    } else {
        console.log("select not found");
    }
});
