# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import os
import subprocess

import click

from . import cli, shexec
from .. import db, list_units
from .. import init as rs_init

DUMP_DIR = '/rs/project/local'
DUMP_FILE = DUMP_DIR + '/db-dump.sql'

# -------------------------------------------------------------------------------------------------------------------- #

@cli.group('db')
def db_cli():
    ''' Database management. '''

# -------------------------------------------------------------------------------------------------------------------- #

@db_cli.command()
def init():
    ''' Initialize database tables. '''

    db.init_db()

    rs_init()

    for x in list_units():
        x.init_tables()

# -------------------------------------------------------------------------------------------------------------------- #

@db_cli.command()
def shell():
    ''' Launch psql connected to radstar db. '''
    os.environ['PGOPTIONS'] = '--search_path=public,rs'
    shexec('psql {dsn}', dsn=db.get_conninfo())

# -------------------------------------------------------------------------------------------------------------------- #

@db_cli.command()
def dump():
    ''' Backup database. '''
    if not os.path.isdir(DUMP_DIR):
        os.mkdir(DUMP_DIR)
    shexec('pg_dump -c -f {file} {dsn}', file=DUMP_FILE, dsn=db.get_conninfo())


@db_cli.command()
def restore():
    ''' Restore database. '''
    if not os.path.isdir(DUMP_DIR):
        os.mkdir(DUMP_DIR)
    shexec('psql -f {file} {dsn}', file=DUMP_FILE, dsn=db.get_conninfo())

# -------------------------------------------------------------------------------------------------------------------- #

@db_cli.command()
@click.option('--dst-dsn', prompt='Destination DSN', required=True)
def migrate(dst_dsn):
    ''' Migrate data to another database. '''

    p1 = subprocess.Popen(['pg_dump', '-c', db.get_conninfo()], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['psql', dst_dsn], stdin=p1.stdout)

    p1.stdout.close()

    rc2 = p2.wait()
    rc1 = p1.wait()

    if rc1 != rc2 != 0:
        print('ERROR: Migration failed')

# -------------------------------------------------------------------------------------------------------------------- #

@db_cli.command()
@click.confirmation_option(prompt='This will erase all data from the database. Continue?')
def wipe():
    ''' Wipe existing data in database. '''

    db.init_db()

    with db.transaction():
        db.query('''\
            DROP SCHEMA IF EXISTS public CASCADE;
            DROP SCHEMA IF EXISTS rs CASCADE;
            CREATE SCHEMA public;
        ''')

# -------------------------------------------------------------------------------------------------------------------- #
