import logging

from django.forms import formset_factory
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render

from website.forms.reservation import EditGuestForm, EditGuestFormSet
from website.models.guest import Guest
from website.models.reservation import Reservation
from website.views.decorators.reservation import require_activated_reservation, require_rsvp_deadline_not_passed

logger = logging.getLogger(__name__)


@require_activated_reservation
@require_rsvp_deadline_not_passed
def quick_answer(request: HttpRequest, reservation_id: int, answer: str):
    if answer == 'yes':
        rsvp_answer = True
    elif answer == 'no':
        rsvp_answer = False
    else:
        return HttpResponseBadRequest()
    res = Reservation.objects.get(id=reservation_id)
    for guest in Guest.objects.filter(reservation_id=reservation_id).all():
        updated_fields = ['rsvp_answer']
        guest.rsvp_answer = rsvp_answer
        guest.save(update_fields=updated_fields)
    return redirect('reservation')


@require_activated_reservation
@require_rsvp_deadline_not_passed
def index(request: HttpRequest, reservation_id: int):
    res = Reservation.objects.get(id=reservation_id)
    guests = Guest.objects.filter(reservation_id=reservation_id).order_by('created_at').all()
    current_guest_count = len(guests)
    if current_guest_count > res.max_guests:
        logging.warning("Reservation %d has more guests (%d) than they are allowed (%d)" % (
            reservation_id,
            current_guest_count,
            res.max_guests
        ))

    formset_class = formset_factory(EditGuestForm, formset=EditGuestFormSet, extra=(res.max_guests - 1), min_num=1,
                                    max_num=res.max_guests,
                                    can_delete=True, can_delete_extra=True, validate_max=True, validate_min=True,
                                    absolute_max=10)

    allowed_guest_ids = [-1]
    for guest in guests:
        allowed_guest_ids.append(guest.id)

    form_kwargs = {
        'allowed_guest_ids': allowed_guest_ids
    }

    if request.method == 'POST':
        form_kwargs['empty_permitted'] = False
        formset = formset_class(data=request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            final_guest_ids = []
            for form in formset:
                if not form.cleaned_data or form in formset.deleted_forms:
                    continue
                guest_id = form.cleaned_data['guest_id'] if 'guest_id' in form.cleaned_data else None
                guest_data = {
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'rsvp_answer': form.cleaned_data['rsvp_answer'],
                    'food_vegan_option': form.cleaned_data['food_vegan_option'],
                }
                if guest_id and guest_id != -1:
                    guest = Guest.objects.get(id=guest_id)
                    updated_fields = []
                    for attr, value in guest_data.items():
                        updated_fields.append(attr)
                        setattr(guest, attr, value)
                    guest.save(update_fields=updated_fields)
                    final_guest_ids.append(guest_id)
                else:
                    guest = Guest.objects.create(reservation=res, **guest_data)
                    final_guest_ids.append(guest.id)
            for form in formset.deleted_forms:
                guest_id = form.cleaned_data['guest_id'] if 'guest_id' in form.cleaned_data else None
                if guest_id and guest_id != -1:
                    for guest in guests:
                        if guest.id == guest_id:
                            guest.delete()
                            break
            all_guests = Guest.objects.filter(reservation_id=reservation_id).only("id").all()
            for guest in all_guests:
                if guest.id not in final_guest_ids:
                    guest.delete()
            return redirect('reservation')
    else:
        # Populate formset with existing guest data
        initial_form_count = max(min(res.max_guests, current_guest_count), 1)
        initial_data = {
            'form-TOTAL_FORMS': res.max_guests,
            'form-INITIAL_FORMS': initial_form_count
        }
        for i, guest in enumerate(guests):
            if i >= initial_form_count:
                break
            form_prefix = 'form-%d-' % i
            initial_data.update({
                (form_prefix + 'guest_id'): guest.id,
                (form_prefix + 'first_name'): guest.first_name,
                (form_prefix + 'first_name'): guest.first_name,
                (form_prefix + 'last_name'): guest.last_name,
                (form_prefix + 'rsvp_answer'): guest.rsvp_answer,
                (form_prefix + 'food_vegan_option'): guest.food_vegan_option
            })
        formset = formset_class(data=initial_data, form_kwargs=form_kwargs)

    deleted_form_indexes = []
    for i, form in enumerate(formset.forms):
        if form.is_deleted():
            deleted_form_indexes.append(i)

    return render(request, "reservation/rsvp/index.html", {
        'page_title': 'Edit RSVP',
        'formset': formset,
        'deleted_form_indexes': deleted_form_indexes,
        'max_guests': res.max_guests
    })
