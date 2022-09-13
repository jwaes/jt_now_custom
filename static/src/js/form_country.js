/** @odoo-module */

import { session } from '@web/session';

$(document ).ready(function() {
    const slct = $('select[name=country_id].s_website_form_input');
    if(slct.length){
        if (session.geoip_country_name){
            $('select[name=country_id].s_website_form_input option').filter(function(){
                return $(this).text() == session.geoip_country_name;
            }).prop('selected',true);
        }
    } 
});
