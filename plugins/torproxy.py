# torproxy.py
# Make dnf operation go trough the tor network.
#
# Copyright (C) 2016 Michael Scherer
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

import dnf
import dnf.plugin
import dnfpluginsextras
import pycurl
import json
import io
import iniparse.compat as ini

from dnfpluginscore import _

MSG = _('It seems that tor is not working, network operations may fail.')


class TorProxy(dnf.Plugin):

    name = "torproxy"

    def __init__(self, base, cli):
        super(TorProxy, self).__init__(base, cli)
        self.base = base
        self.logger = dnfpluginsextras.logger

    def _check_tor_working(self):

        buf = io.BytesIO()

        c = pycurl.Curl()

        c.setopt(pycurl.URL, 'https://check.torproject.org/api/ip')
        c.setopt(pycurl.PROXY, self._host)
        c.setopt(pycurl.PROXYPORT, int(self._port))
        c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
        c.setopt(pycurl.PROXYUSERNAME, 'check')
        c.setopt(pycurl.PROXYPASSWORD, 'check')

        c.setopt(c.WRITEFUNCTION, buf.write)

        try:
            c.perform()
            result = json.loads(buf.getvalue().decode("ascii"))['IsTor']
        # TODO fix me, need to have a better exception filter
        except Exception as e:
            print(e)
            result = False

        return result

    def config(self):
        conf = self.read_config(self.base.conf, "torproxy")
        # TODO try/catch if the config no longer exist (but then, what
        # should the default be ?)
        if not conf.getboolean("main", "enabled"):
            return

        try:
            self._port = conf.get("torproxy", "port")
        except ini.Error:
            self._port = '9050'

        try:
            self._host = conf.get("torproxy", "host")
        except ini.Error:
            self._host = '127.0.0.1'

        if not self._check_tor_working():
            self.logger.error(MSG)

        for name, repo in self.base.repos.items():
            if not repo.proxy:
                repo.proxy = 'socks5h://{}:{}'.format(self._host, self._port)
                # set a password to use IsolateSOCKSAuth, see
                # https://github.com/diocles/apt-transport-tor
                repo.proxy_username = 'dnf_' + name
                repo.proxy_password = 'dnf_' + name
