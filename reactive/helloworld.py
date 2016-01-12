
import shutil
import subprocess

from charmhelpers.fetch.yum import (
    yum_install,
    yum_update,
)

from charmhelpers.core.hookenv import (
    status_set,
    open_port,
)


from charms.reactive import (
    hook,
    set_state,
    remove_state,
    when,
)


@hook('install')
def time_to_make_the_donuts():
    set_state('install-deps')


@when('install-deps')
def install_deps():
    status_set('maintenance', 'installing deps')
    yum_update()
    yum_install(['httpd'])
    set_state('httpd.installed')
    remove_state('install-deps')


@when('httpd.installed')
@when_not('demo ready')
def setup_demo():
    status_set('maintenance', 'starting apache')
    subprocess.check_call('/usr/sbin/apachectl start')
    open_port(80)
    set_state('demo ready')
    status_set('active', 'ready')

