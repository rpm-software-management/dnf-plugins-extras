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

    def buildgraph(self):
        """
        Load the list of installed packages and their dependencies using
        hawkey, and build the dependency graph and the graph of reverse
        dependencies.
        """
        sack = dnf.sack.rpmdb_sack(self.base)
        pkgmap = dict()
        packages = []
        depends = []
        rdepends = []
        deps = set()
        providers = set()

        for i, pkg in enumerate(sack.query()):
            pkgmap[pkg] = i
            packages.append(pkg)
            rdepends.append([])

        for i, pkg in enumerate(packages):
            for req in pkg.requires:
                sreq = str(req)
                if sreq.startswith('rpmlib(') or sreq == 'solvable:prereqmarker':
                    continue
                for dpkg in sack.query().filter(provides=req):
                    providers.add(pkgmap[dpkg])
                if i not in providers:
                    deps.update(providers)
                providers.clear()

            deplist = list(deps)
            deps.clear()
            depends.append(deplist)
            for j in deplist:
                rdepends[j].append(i)

        return (packages, depends, rdepends)

    def kosaraju(self, graph, rgraph):
        """
        Run Kosaraju's algorithm to find strongly connected components
        in the graph, and return the list of nodes in the components
        without any incoming edges.
        """
        N = len(graph)
        rstack = []
        stack = []
        tag = [False] * N

        # do depth-first searches in the graph
        # and push nodes to rstack "on the way up"
        # until all nodes have been pushed.
        # tag nodes so we don't visit them more than once
        for u in range(N):
            if tag[u]:
                continue

            stack.append(u)
            tag[u] = True
            while stack:
                u = stack[-1]
                if u >= 0:
                    stack[-1] = -1 - u
                    for v in graph[u]:
                        if not tag[v]:
                            stack.append(v)
                            tag[v] = True
                else:
                    stack.pop()
                    rstack.append(-1 - u)

        # now searches beginning at nodes popped from
        # rstack in the graph with all edges reversed
        # will give us the strongly connected components.
        # the incoming edges to each component is the
        # union of incoming edges to each node in the
        # component minus the incoming edges from
        # component nodes themselves.
        # now all nodes are tagged, so this time let's
        # remove the tags as we visit each node.
        orphans = []
        scc = []
        sccredges = set()
        while rstack:
            v = rstack.pop()
            if not tag[v]:
                continue

            stack.append(v)
            tag[v] = False
            while stack:
                v = stack.pop()
                redges = rgraph[v]
                scc.append(v)
                sccredges.update(redges)
                for u in redges:
                    if tag[u]:
                        stack.append(u)
                        tag[u] = False

            sccredges.difference_update(scc)
            if not sccredges:
                orphans.extend(scc)
            del scc[:]
            sccredges.clear()

        return orphans

    def findorphans(self):
        (packages, depends, rdepends) = self.buildgraph()
        return [packages[i] for i in self.kosaraju(depends, rdepends)]

    def run(self, args):
        for pkg in sorted(map(str, self.findorphans())):
            print(pkg)
