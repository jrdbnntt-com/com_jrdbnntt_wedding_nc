import "bootstrap"
import "website/src/css/bootstrap.scss"
import "bootstrap-icons/font/bootstrap-icons.css"
import "./index.scss"
import "./nav.js"
import * as $ from "jquery";
import moment from "moment";


const eventDate = moment(window.EVENT_DATE_ISO);
window.moment = moment;

$(document).ready(() => {
    refresh_date_countdown();
    setTimeout(() => {
        refresh_date_countdown();
    }, 1000 * 60);
})

function refresh_date_countdown() {
    let message;
    let now = moment();
    let timeToEvent = moment.duration(eventDate.diff(now));
    if (now.isBefore(eventDate)) {
        if (timeToEvent.as('days') < 3) {
            message = "Starts at " + eventDate.format("h:mma")
        } else {
            message = now.to(eventDate, true) + " to go!";
        }
    } else if (now.isBefore(eventDate.endOf('day'))) {
        message = "IT IS TIME!!"
    } else {
        message = now.to(eventDate);
    }
    message = message.toUpperCase();
    $('#countdown').text(message);
}