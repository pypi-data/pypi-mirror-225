# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import jinja2
import rs

NGINX_CONF_PATH = '/tmp/nginx.conf'

# -------------------------------------------------------------------------------------------------------------------- #

def get_parameters(j2: jinja2.Environment, **kw) -> dict[str, str]:

    if (nginx_conf_path := rs.getenv('RS_NGINX_CONF_PATH')) is None:
        with open(nginx_conf_path := NGINX_CONF_PATH, 'w') as f:
            print(j2.get_template('nginx.conf.j2').render(**kw), file=f)

    return {
        'nginx_conf_path': nginx_conf_path,
    }

# -------------------------------------------------------------------------------------------------------------------- #
