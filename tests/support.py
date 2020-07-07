# Copyright (C) 2014-2019  Red Hat, Inc.
# Copyright (C) 2015 Igor Gnatenko
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
import dnf.cli.option_parser
import logging
import sys

from unittest import mock

def command_configure(cmd, args):
    parser = dnf.cli.option_parser.OptionParser()
    args = [cmd._basecmd] + args
    parser.parse_main_args(args)
    parser.parse_command_args(cmd, args)
    return cmd.configure()

def command_run(cmd, args):
    command_configure(cmd, args)
    return cmd.run()


class FakeConf(dnf.conf.Conf):
    def __init__(self, **kwargs):
        super(FakeConf, self).__init__()
        self.substitutions['releasever'] = 'Fedora69'
        for optname, val in [
                ('assumeyes', None),
                ('best', False),
                ('cachedir', dnf.const.TMPDIR),
                ('clean_requirements_on_remove', False),
                ('color', 'never'),
                ('color_update_installed', 'normal'),
                ('color_update_remote', 'normal'),
                ('color_list_available_downgrade', 'dim'),
                ('color_list_available_install', 'normal'),
                ('color_list_available_reinstall', 'bold'),
                ('color_list_available_upgrade', 'bold'),
                ('color_list_installed_extra', 'bold'),
                ('color_list_installed_newer', 'bold'),
                ('color_list_installed_older', 'bold'),
                ('color_list_installed_reinstall', 'normal'),
                ('color_update_local', 'bold'),
                ('debug_solver', False),
                ('debuglevel', 2),
                ('defaultyes', False),
                ('disable_excludes', []),
                ('diskspacecheck', True),
                ('exclude', []),
                ('includepkgs', []),
                ('install_weak_deps', True),
                ('history_record', False),
                ('installonly_limit', 0),
                ('installonlypkgs', ['kernel']),
                ('installroot', '/'),
                ('ip_resolve', None),
                ('multilib_policy', 'best'),
                ('obsoletes', True),
                ('persistdir', '/should-not-exist-bad-test/persist'),
                ('protected_packages', ["dnf"]),
                ('plugins', False),
                ('showdupesfromrepos', False),
                ('tsflags', []),
                ('strict', True),
                ] + list(kwargs.items()):
            self._set_value(optname, val, dnf.conf.PRIO_DEFAULT)

    @property
    def releasever(self):
        return self.substitutions['releasever']

class BaseStub(object):
    def __init__(self):
        self.sack = dnf.sack.Sack()
        self.repos = dnf.repodict.RepoDict()
        self.conf = FakeConf()

    def add_remote_rpms(self, path_list):
        self.sack.create_cmdline_repo()
        pkgs = []
        for path in path_list:
            pkgs.append(self.sack.add_cmdline_package(path))
        return pkgs

class BaseCliStub(object):
    """A class mocking `dnf.cli.cli.BaseCli`."""

    def __init__(self, available_pkgs=(), available_groups=()):
        """Initialize the base."""
        self._available_pkgs = set(available_pkgs)
        self._available_groups = set(available_groups)
        self.installed_groups = set()
        self.installed_pkgs = set()
        self.repos = dnf.repodict.RepoDict()
        self.conf = FakeConf()

    def read_all_repos(self):
        """Read repositories information."""
        self.repos.add(dnf.repo.Repo(name='main'))

    def read_comps(self):
        """Read groups information."""
        if not self._available_groups:
            raise dnf.exceptions.CompsError('no group available')

    def install_specs(self, install, exclude=None, reponame=None, strict=True, forms=None):
        for spec in install:
            if spec.startswith("@"):
                self.installed_groups.add(spec[1:])
            else:
                self.installed_pkgs.add(spec)

class CliStub(object):
    """A class mocking `dnf.cli.Cli`."""

    nogpgcheck = True

    def __init__(self, base):
        """Initialize the CLI."""
        self.base = base
        self.cli_commands = {}
        self.demands = DemandsStub()
        self.logger = logging.getLogger()
        self.register_command(dnf.cli.commands.HelpCommand)

    def redirect_logger(self, stdout=None, stderr=None):
        return

    def redirect_repo_progress(self, fo=sys.stderr):
        return

    def register_command(self, command):
        """Register given *command*."""
        self.cli_commands.update({alias: command for alias in command.aliases})


class DemandsStub(object):
    pass
