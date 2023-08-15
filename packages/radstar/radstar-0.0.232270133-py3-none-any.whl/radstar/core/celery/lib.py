# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

def task(queue=None, retry=False, schedule=None, **kw):

    def inner(x):
        from .celery_app import app

        if retry is True:
            if 'autoretry_for' not in kw:
                kw['autoretry_for'] = (Exception,)
            if 'retry_backoff' not in kw:
                kw['retry_backoff'] = True

        x = app.task(**kw)(x)

        if queue is not None:
            app.conf.task_routes[x.name] = {'queue': queue}

        if schedule is not None:
            app.conf.beat_schedule[x.name] = {'task': x.name, 'schedule': schedule}

        return x

    return inner

# -------------------------------------------------------------------------------------------------------------------- #

def have_tasks_defined():
    from .celery_app import app
    return any(not x.startswith('celery.') for x in app.tasks)

# -------------------------------------------------------------------------------------------------------------------- #
