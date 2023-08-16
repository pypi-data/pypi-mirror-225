# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from rs import db

# -------------------------------------------------------------------------------------------------------------------- #


def init_tables(old_schema):

    current_schema = 1

    if old_schema < 1:
        db.query('''
            CREATE OR REPLACE FUNCTION rs.webd_modify_trigger() RETURNS TRIGGER AS $$
                BEGIN
                    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
                        PERFORM pg_notify('rs.webd', concat_ws('|', TG_TABLE_SCHEMA, TG_TABLE_NAME, TG_OP, NEW.id));
                        RETURN NEW;
                    ELSIF TG_OP = 'DELETE' THEN
                        PERFORM pg_notify('rs.webd', concat_ws('|', TG_TABLE_SCHEMA, TG_TABLE_NAME, TG_OP, OLD.id));
                        RETURN OLD;
                    END IF;
                END;
            $$ LANGUAGE plpgsql;
        ''')

    return current_schema

# -------------------------------------------------------------------------------------------------------------------- #
