import "./index.scss";
import "bootstrap";
import "website/src/css/bootstrap/bootstrap.scss";
import "bootstrap-icons/font/bootstrap-icons.css";
import * as $ from "jquery";
import moment from "moment";


const eventDate = moment(window.EVENT_DATE_ISO);
window.moment = moment;

$(document).ready(() => {
    refreshDateCountdown();
    setTimeout(() => {
        refreshDateCountdown();
    }, 1000 * 60);
    initForms();

    setVw();
    window.addEventListener('resize', setVw);
})

function refreshDateCountdown() {
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

function initForms() {
    let $forms = $('form');
    if ($forms.length === 0) {
        return;
    }
    let $fieldErrorMessages = $forms.find('.invalid-feedback');
    $fieldErrorMessages.each((i, e) => {
        let $feedback = $(e);
        let $fieldInputs = $feedback.parent().find('input,textarea,select');
        $fieldInputs.addClass('is-invalid');
        let onChangeContainer = {}
        onChangeContainer.clearErrorMessage = () => {
            $fieldInputs.removeClass('is-invalid');
            $fieldInputs.off('change', onChangeContainer.clearErrorMessage);
        };
        $fieldInputs.on('change', onChangeContainer.clearErrorMessage);
    });
}

function setVw() {
    let vw = document.documentElement.clientWidth / 100;
    document.documentElement.style.setProperty('--vw', `${vw}px`);
}
