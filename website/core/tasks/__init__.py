import logging
import time
from threading import Thread

from django.conf import settings

from website.core.mail import send_rsvp_updated_email
from website.models.guest import Guest
from website.models.reservation import Reservation
from website.models.task import schedule_task, Task, get_processable_tasks
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
TASK_NAME_SEND_RSVP_UPDATED_EMAIL = 'send_rsvp_updated_email'
_SECONDS_IN_NANOSECOND = 1000000000.0


def schedule_send_rsvp_updated_email(reservation_id: int):
    schedule_task(
        TASK_NAME_SEND_RSVP_UPDATED_EMAIL,
        datetime.now() + timedelta(seconds=30),
        task_kwargs={
            'reservation_id': reservation_id
        }
    )


def _task_send_rsvp_updated_email(reservation_id: int):
    reservation = Reservation.objects.filter(id=reservation_id).get()
    guests = Guest.objects.filter(reservation_id=reservation_id).get()

    attending_wedding = False
    attending_rehearsal = False
    guest_rsvp_statuses = []
    rsvp_complete = True
    for guest in guests:
        if guest.rsvp_answer:
            attending_wedding = True
        if guest.rehearsal_rsvp_answer:
            attending_rehearsal = True
        rsvp_complete = rsvp_complete and guest.rsvp_answer is not None and (
                not reservation.invited_to_rehearsal or guest.rehearsal_rsvp_answer is not None)
        status = guest.first_name
        if guest.rsvp_answer is None:
            status += " has not yet RSVP'd to the wedding reception"
        else:
            status += " has RSVP'd " + guest.rsvp_answer_display()
        if reservation.invited_to_rehearsal:
            if guest.rsvp_answer is None:
                status += " and has not yet RSVP'd to the wedding rehearsal"
            else:
                status += " and has RSVP'd " + guest.rehearsal_rsvp_answer_display()
        status += '.'
        guest_rsvp_statuses.append(status)

    if len(guests) > 0:
        to_name = guests[0].first_name
    else:
        to_name = reservation.name

    send_rsvp_updated_email(
        to_email=reservation.user.email,
        to_name=to_name,
        invited_to_rehearsal=reservation.invited_to_rehearsal,
        attending_wedding=attending_wedding,
        attending_rehearsal=attending_rehearsal,
        guest_rsvp_statuses=guest_rsvp_statuses,
        rsvp_complete=rsvp_complete
    )


TASK_EXECUTOR_LOOKUP: {
    TASK_NAME_SEND_RSVP_UPDATED_EMAIL: _task_send_rsvp_updated_email
}


def process_task(task: Task):
    if task.name not in TASK_EXECUTOR_LOOKUP:
        raise ValueError("Task name '%s' not found in task executor lookup'" % task.name)
    task.execute_task(TASK_EXECUTOR_LOOKUP[task.name])


def process_all_processable_tasks() -> int:
    process_count = 0
    tasks = get_processable_tasks()
    for task in tasks:
        process_count += 1
        process_task(task)
    return process_count


def _process_tasks_continuously():
    min_wait_time_ns = int(settings.MIN_TIME_BETWEEN_TASK_POLLING_IN_SECONDS * _SECONDS_IN_NANOSECOND)
    while True:
        start_time = time.time_ns()
        tasks_processed = process_all_processable_tasks()
        process_time = time.time_ns() - start_time
        if process_time < min_wait_time_ns:
            wait_time_ns = min_wait_time_ns - process_time
            time.sleep(wait_time_ns / _SECONDS_IN_NANOSECOND)
        logger.debug("Processed %d tasks in %.3f seconds" % (tasks_processed, process_time / _SECONDS_IN_NANOSECOND))


def start_processing_tasks_in_background():
    th = Thread(target=_process_tasks_continuously, daemon=True)
    th.start()
