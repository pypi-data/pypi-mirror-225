# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from celery import Celery
from celery.signals import celeryd_after_setup
import rs

# -------------------------------------------------------------------------------------------------------------------- #

app = Celery()

app.conf.update(
    beat_schedule_filename = rs.getenv('CELERY_SCHEDULE_FILENAME', '/tmp/celerybeat-schedule'),
    broker_connection_retry = True,
    broker_connection_retry_on_startup = True,
    broker_url = rs.getenv('CELERY_BROKER_URL') or rs.getenv('RS_REDIS_URL', 'redis://redis/'),
    result_backend = rs.getenv('CELERY_RESULT_BACKEND') or rs.getenv('RS_REDIS_URL', 'redis://redis/'),
    # task_acks_late = True,
    task_routes = {},
    timezone = rs.getenv('TZ', 'UTC'),
    worker_prefetch_multiplier = 2,
    worker_pool = 'threads',
)

@celeryd_after_setup.connect
def setup(instance, **_):
    try:
        rs.db.init_db(min_connections=instance.concurrency // 2, max_connections=instance.concurrency)
    except:
        rs.panic('database connection failed', exc_info=True)


# XXX: only initialize radstar when that hasn't already happened.
# XXX: it should really only happen when celery is launched with the celery command.
# XXX: i've already try celeryd_init and other celery signals without luck.
if not rs.list_units():
    rs.init(['tasks'])

# -------------------------------------------------------------------------------------------------------------------- #
