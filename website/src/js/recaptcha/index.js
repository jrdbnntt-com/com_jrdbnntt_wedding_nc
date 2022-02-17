import * as $ from "jquery";

/**
 * Attaches a recaptcha check to a form submission. Submitting the form triggers a recaptcha check form submission is
 * temporarily stopped. Once the check is completed the recaptcha token is stored in $hiddenTokenInput and then the
 * form is resubmitted without another recaptcha check.
 *
 * @param $form form trigger recaptcha execute on when submitted
 * @param $hiddenTokenInput input to store the recaptcha result token in
 * @param action reCAPTCHA action name override (defaults to window.RECAPTCHA_ACTION)
 */
export function attach($form, $hiddenTokenInput, recaptchaAction) {
    console.debug("attaching reCAPTCHA to form", $form);
    const siteKey = window.RECAPTCHA_SITE_KEY;
    recaptchaAction = recaptchaAction ? recaptchaAction : window.RECAPTCHA_ACTION;
    if (!siteKey) {
        throw new Error('Missing window.RECAPTCHA_SITE_KEY');
    }
    if (!recaptchaAction) {
        throw new Error('Missing window.RECAPTCHA_ACTION');
    }
    if (!window.grecaptcha) {
        throw new Error('Missing window.grecaptcha');
    }
    if (!$form || $form.length === 0) {
        throw new Error("Missing $form");
    }
    if (!$hiddenTokenInput || $hiddenTokenInput.length === 0) {
        throw new Error("Missing $hiddenTokenInput");
    }
    let scoring = false;
    let token = null;
    let listenerContainer = {
        listenerFunction: null
    };
    listenerContainer.listenerFunction = (e) => {
        console.debug("reCAPTCHA submit event", {
            scoring: scoring,
            siteKey: siteKey,
            recaptchaAction: recaptchaAction,
            $form: $form,
            $hiddenTokenInput: $hiddenTokenInput
        });
        e.stopPropagation();
        e.preventDefault();
        if (scoring) {
            return;
        }
        scoring = true;
        window.grecaptcha.ready(() => {
            window.grecaptcha.execute(siteKey, {action: recaptchaAction})
                .then((newToken) => {
                    token = newToken;
                    $hiddenTokenInput.val(newToken);
                    scoring = false;
                    console.debug("reCAPTCHA token", token);
                    $form.off('submit', listenerContainer.listenerFunction);
                    $form.submit();
                })
                .catch((err) => {
                    if (err) {
                        console.error("recaptcha execute failed:", err)
                    }
                    scoring = false;
                });
        });
    };
    $form.on('submit', listenerContainer.listenerFunction);

}