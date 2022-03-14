import "website/src/views/_templates/main/index"
import "./index.scss"
import * as $ from "jquery";

$(document).ready(() => {
    init();
});

let context = {
    $btnAddForm: null,
    $form: null
}

function init() {
    context.$form = $('form');
    context.$btnAddForm = $('button.btn-form-add');
    refreshAddFormBtn();
    context.$btnAddForm.on('click', (e) => {
        let $formContainer = getNextAvailableForm();
        if ($formContainer) {
            let $deleteInput = $formContainer.find('input.deletion');
            let $guestIdInput = $formContainer.find('input.guest-id');
            $deleteInput.val('');
            $guestIdInput.val('-1');
            $formContainer.find('.is-invalid').removeClass('is-invalid');
            $formContainer.toggle(true);
            $('html, body').animate({
                scrollTop: $formContainer.offset().top
            });
        }
        refreshAddFormBtn();
    });
    $('button.btn-form-delete').on('click', (e) => {
        let $deleteBtn = $(e.target);
        let $formContainer = $deleteBtn.closest('.form-container');
        let $deleteInput = $formContainer.find('input.deletion');
        let $guestIdInput = $formContainer.find('input.guest-id');
        $deleteInput.val('on');
        if ($guestIdInput.val() === '-1') {
            $guestIdInput.val('');
        }
        $formContainer.toggle(false);
        refreshAddFormBtn();
    });
    getAvailableForms().find('input.deletion').val('on');
}

function getAvailableForms() {
    return context.$form.find('.form-container:not(:visible)');
}

function getNextAvailableForm() {
    let availableForms = getAvailableForms();
    if (availableForms.length > 0) {
        return $(availableForms[0]);
    }
    return null;
}

function refreshAddFormBtn() {
    context.$btnAddForm.closest('.page-section').toggle(!!getNextAvailableForm());
}