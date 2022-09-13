/** @odoo-module */

import { get_cookie } from 'web.utils.cookies';
import { session } from '@web/session';

$(document ).ready(function() {
    const slct = $('select.s_website_form_input');
    if(slct.length){
        console.log("select is there");
        const htmlEl = document.documentElemen;
        const country = session.geoip_country_code;
        console.log("session is " + session);
        console.log(session);
        if (country) {
            console.log("country is " + country);
        }
    } else {
        console.log("select not found");
    }
});
