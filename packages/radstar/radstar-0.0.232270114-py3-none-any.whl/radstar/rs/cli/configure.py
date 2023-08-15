# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from itertools import chain
import os
import shutil

import jinja2
import rs
import yaml

from . import cli

# -------------------------------------------------------------------------------------------------------------------- #

DEBIAN_CODENAMES = {
    '11': 'bullseye',
    '12': 'bookworm',
    '13': 'trixie',
    '14': 'forky',
}

# -------------------------------------------------------------------------------------------------------------------- #

@cli.command()
def configure():
    ''' Reconfigure project. '''

    with open('/rs/project/project.yml') as f:
        project_data = yaml.safe_load(f)

    rs.init(import_default_modules=False)

    # jinja environment
    env = jinja2.Environment(undefined=jinja2.StrictUndefined)

    # versions
    project_data['v'] = project_data['versions']
    project_data['v']['codename'] = DEBIAN_CODENAMES[project_data['v']['debian']]

    # apt packages
    for x in ['', 'build_', 'dev_']:
        project_data[f'apt_{x}pkgs'] = [render(env, p, **project_data) for p in chain_attrs(f'apt.{x}packages')]

    # apt repos
    for x in ['repos', 'build_repos', 'dev_repos']:
        repos = chain_attrs(f'apt.{x}')
        for r in repos:
            r['entry'] = render(env, r['entry'], **project_data)
        project_data[f'apt_{x}'] = repos

    # docker
    for x in ['build', 'build_setup', 'dev_setup', 'setup']:
        project_data[f'docker_{x}'] = '\n\n'.join(
            render(env, cmds, **project_data) for app in rs.list_units() if (cmds := app.get_attr(f'docker.{x}'))
        )

    copy_with_templates(env, 'templates/root', '/rs/project', project_data)
    copy_with_templates(env, 'templates/devcontainer', '/rs/project/.devcontainer', project_data)
    copy_with_templates(env, 'templates/vscode', '/rs/project/.vscode', project_data)

# -------------------------------------------------------------------------------------------------------------------- #

def chain_attrs(key: str) -> list:
    return list(chain.from_iterable(x for app in rs.list_units() if (x := app.get_attr(key))))

# -------------------------------------------------------------------------------------------------------------------- #

def copy_with_templates(env: jinja2.Environment, src: str, dst: str, project_data: dict):

    for src_root, dirs, files in os.walk(src):

        dst_root = os.path.join(dst, src_root[len(src)+1:])
        if not os.path.isdir(dst_root):
            os.mkdir(dst_root)

        for x in dirs:
            if x[0] == '.':
                continue
            x = os.path.join(dst_root, x)

            if not os.path.isdir(x):
                os.mkdir(x)

        for x in files:
            if x[0] == '.':
                continue

            src_file = os.path.join(src_root, x)
            if x.startswith('dot-'):
                x = x.replace('dot-', '.', 1)
            dst_file = os.path.join(dst_root, x)

            if x.endswith('.j2'):
                with open(src_file) as f:
                    data = env.from_string(f.read()).render(**project_data)
                with open(dst_file[:-3], 'w') as f:
                    print(data, file=f)
            else:
                shutil.copy(src_file, dst_file)

# -------------------------------------------------------------------------------------------------------------------- #

def render(env_: jinja2.Environment, src_: str, **kw):
    return env_.from_string(src_).render(**kw)

# -------------------------------------------------------------------------------------------------------------------- #
