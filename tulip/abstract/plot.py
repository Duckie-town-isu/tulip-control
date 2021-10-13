# Copyright (c) 2011-2014 by California Institute of Technology
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the California Institute of Technology nor
#    the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CALTECH
# OR THE CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
"""Functions for plotting Partitions."""
import logging
logger = logging.getLogger(__name__)

import networkx as nx
import numpy as np
import scipy.sparse as sp

from polytope.plot import (
    plot_partition,
    plot_transition_arrow)
# inline imports:
#
# import matplotlib as mpl
# from tulip.graphics import newax

def plot_abstraction_scc(ab, ax=None):
    """Plot Regions colored by strongly-connected component.

    Handy to develop new examples or debug existing ones.
    """
    try:
        import matplotlib as mpl
    except:
        logger.error(
            'failed to load `matplotlib`')
        return
    ppp = ab.ppp
    ts = ab.ts
    ppp2ts = ab.ppp2ts
    # each connected component of
    # filtered graph is a symbol
    components = nx.strongly_connected_components(ts)
    if ax is None:
        ax = mpl.pyplot.subplot()
    l, u = ab.ppp.domain.bounding_box
    ax.set_xlim(l[0, 0], u[0, 0])
    ax.set_ylim(l[1, 0], u[1, 0])
    for component in components:
        # map to random colors
        red = np.random.rand()
        green = np.random.rand()
        blue = np.random.rand()
        color = (red, green, blue)
        for state in component:
            i = ppp2ts.index(state)
            ppp[i].plot(ax=ax, color=color)
    return ax


def plot_ts_on_partition(
        ppp, ts, ppp2ts,
        edge_label, only_adjacent, ax):
    """Plot partition and arrows from labeled digraph.

    Edges can be filtered by
    selecting an `edge_label`.
    So it can plot transitions of
    a single mode for a switched system.

    @param edge_label: desired label
    @type edge_label: `dict`
    """
    l,u = ppp.domain.bounding_box
    arr_size = (u[0, 0] - l[0, 0]) / 50.0
    ts2ppp = {v: k for k, v in enumerate(ppp2ts)}
    for from_state, to_state, label in (
            ts.transitions.find(
                with_attr_dict=edge_label)):
        i = ts2ppp[from_state]
        j = ts2ppp[to_state]
        if only_adjacent:
            if ppp.adj[i, j] == 0:
                continue
        plot_transition_arrow(
            ppp.regions[i],
            ppp.regions[j],
            ax,
            arr_size)


def project_strategy_on_partition(ppp, mealy):
    """Project transitions of `ppp` on `mealy`.

    Returns an `FTS` with the `PPP` (spatial)
    transitions used by the Mealy strategy.

    @type ppp: `PropPreservingPartition`
    @type mealy: `transys.MealyMachine`
    """
    n = len(ppp)
    proj_adj = sp.lil_matrix((n, n))
    for (from_state, to_state, label) in mealy.transitions.find():
        from_label = mealy.states[from_state]
        to_label = mealy.states[to_state]
        if 'loc' not in from_label or 'loc' not in to_label:
            continue
        from_loc = from_label['loc']
        to_loc = to_label['loc']
        proj_adj[from_loc, to_loc] = 1
    return proj_adj


def plot_strategy(ab, mealy):
    """Plot strategic transitions on PPP.

    Assumes that `mealy` is feasible for `ab`.

    @type ab: `AbstractPwa` or `AbstractSwitched`
    @type mealy: `transys.MealyMachine`
    """
    proj_mealy = project_strategy_on_partition(ab.ppp, mealy)
    ax = plot_partition(
        ab.ppp,
        proj_mealy,
        color_seed=0)
    return ax


def plot_trajectory(
        ppp, x0, u_seq, ssys,
        ax=None,
        color_seed=None):
    """Plot partition and trajectory, starting from `x0`.

    Plots a `PropPreservingPartition` and
    the trajectory that is generated by the
    input sequence `u_seq`, starting from point `x0`.


    Relevant
    ========
    `plot_partition`, plot

    @type ppp: `PropPreservingPartition`
    @param x0: initial state
    @param u_seq: matrix where each row contains an input
    @param ssys: system dynamics
    @param color_seed: see `plot_partition`
    @return: axis object
    """
    try:
        from tulip.graphics import newax
    except:
        logger.error(
            'failed to import '
            '`tulip.graphics.newax`')
        return
    if ax is None:
        ax, fig = newax()
    plot_partition(
        plot_numbers=False,
        ax=ax,
        show=False)
    A = ssys.A
    B = ssys.B
    if ssys.K is not None:
        K = ssys.K
    else:
        K = np.zeros(x0.shape)
    x = x0.flatten()
    x_arr = x0
    for i in range(u_seq.shape[0]):
        x = (
            np.dot(A, x).flatten() +
            np.dot(B, u_seq[i, :]).flatten() +
            K.flatten())
        x_arr = np.vstack([x_arr, x.flatten()])
    ax.plot(x_arr[:, 0], x_arr[:, 1], 'o-')
    return ax
