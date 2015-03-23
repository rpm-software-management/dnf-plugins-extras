# orphans.py
# DNF plugin for listing installed packages not required by any other
# installed package.
#
# Copyright (C) 2015 Emil Renner Berthing
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
from collections import deque

import dnf
import dnf.sack
import dnf.cli
from dnfpluginsextras import _


class Orphans(dnf.Plugin):
    name = 'orphans'

    def __init__(self, base, cli):
        super(Orphans, self).__init__(base, cli)
        if cli:
            cli.register_command(OrphansCommand)


class OrphansCommand(dnf.cli.Command):
    aliases = ('orphans',)
    summary = _('List installed packages not required by any other package')

    def findorphans(self, onlytrueorphans=False):
        sack = dnf.sack.rpmdb_sack(self.base)
        allpackages = set(sack.query())
        tmp = set()

        # build dependency graph and find true orphans
        # (packages not required by any other package)
        depends = dict()
        orphans = allpackages.copy()
        for pkg in allpackages:
            deps = set()
            for req in pkg.requires:
                sreq = str(req)
                if sreq.startswith('rpmlib(') or sreq == 'solvable:prereqmarker':
                    continue
                tmp.clear()
                tmp.update(sack.query().filter(provides=req))
                if pkg not in tmp:
                    deps.update(tmp)
            depends[pkg] = deps
            orphans.difference_update(deps)

        # convert the set of orphans to a list
        orphans = list(orphans)

        # remove true orphans and all their recursive
        # dependencies from allpackages
        queue = deque()
        for pkg in orphans:
            allpackages.remove(pkg)
            queue.append(pkg)

        while len(queue) > 0:
            deps = depends[queue.popleft()]
            deps.intersection_update(allpackages)
            for dpkg in deps:
                allpackages.remove(dpkg)
                queue.append(dpkg)

        # if the true orphans and all their recursive
        # dependencies account for all installed
        # packages: great! we're done.
        if len(allpackages) == 0 or onlytrueorphans:
            return orphans

        # otherwise the remaining packages must consist
        # of one or more dependency cycles and their
        # dependencies

        # let's begin by cutting the graph down to just
        # the remaining packages
        for pkg, deps in depends.items():
            if pkg in allpackages:
                deps.intersection_update(allpackages)
            else:
                del depends[pkg]

        # for each remaining package find its set of
        # recursive dependencies (including itself).
        # packages in dependency cycles must have the
        # same such set of recursive dependencies,
        # so let's group packages by this set.
        rdepmap = dict()
        for pkg in allpackages:
            tmp.clear()
            tmp.add(pkg)

            queue.append(pkg)
            while len(queue) > 0:
                for dpkg in depends[queue.popleft()]:
                    if dpkg not in tmp:
                        tmp.add(dpkg)
                        queue.append(dpkg)

            rdeps = frozenset(tmp)
            if rdeps in rdepmap:
                rdepmap[rdeps].append(pkg)
            else:
                rdepmap[rdeps] = [pkg]

        # add the packages of the "topmost" dependency
        # cycles to the orphans list until all packages
        # are accounted for
        for rdeps in sorted(rdepmap.iterkeys(), key=len, reverse=True):
            if rdepmap[rdeps][0] not in allpackages:
                continue

            orphans.extend(rdepmap[rdeps])
            allpackages.difference_update(rdeps)
            if len(allpackages) == 0:
                break

        return orphans

    def run(self, args):
        for pkg in sorted(map(str, self.findorphans())):
            print(pkg)
