"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from typing import Tuple, Union

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from trajectopy.trajectory import Sorting, Trajectory


def plot_trajectories(trajectories: list[Trajectory], dim: int = 2) -> Tuple[Figure, Figure, Union[Figure, None]]:
    """
    Plots Trajectories
    """
    fig_pos = plot_pos(trajectories=trajectories, dim=dim)
    fig_xyz = plot_xyz(trajectories=trajectories)
    fig_rpy = plot_rpy(trajectories=trajectories)
    return fig_pos, fig_xyz, fig_rpy


def plot_pos(trajectories: list[Trajectory], dim: int = 2) -> Figure:
    """Plots xy(z) coordinates of trajectories as 2d or 3d plot"""
    if dim == 2:
        fig_pos, ax_pos = plt.subplots()
        ax_pos.axis("equal")
    elif dim == 3:
        fig_pos = plt.figure()
        ax_pos = fig_pos.add_subplot(111, projection="3d")
        ax_pos.set_zlabel("z [m]")  # type: ignore
    else:
        raise ValueError(f"Unknown dimension: {dim}")
    ax_pos.set_xlabel("x [m]")
    ax_pos.set_ylabel("y [m]")

    legend_names = []
    for traj in trajectories:
        legend_names.append(traj.name)

        # pos fig
        if dim == 2:
            ax_pos.plot(traj.pos.x, traj.pos.y)
        elif dim == 3:
            ax_pos.plot(traj.pos.x, traj.pos.y, traj.pos.z)

    if dim == 3:
        set_aspect_equal_3d(ax_pos)

    fig_pos.legend(legend_names, ncol=4, loc="upper center")
    return fig_pos


def plot_xyz(trajectories: list[Trajectory]) -> Figure:
    """Plots xyz coordinates of trajectories as subplots"""
    fig_xyz, axs_xyz = plt.subplots(3, 1, sharex=True)

    legend_names = []
    for traj in trajectories:
        legend_names.append(traj.name)
        xyz = traj.pos.xyz

        # xyz fig
        ylabels = ["x [m]", "y [m]", "z [m]"]
        for j, (ax, yl) in enumerate(zip(axs_xyz, ylabels)):
            ax.plot(traj.function_of, xyz[:, j])
            ax.set_ylabel(yl)
            if j == 2:
                if traj.sorting == Sorting.CHRONO:
                    ax.set_xlabel("time [s]")
                else:
                    ax.set_xlabel("trajectory length [m]")

    fig_xyz.legend(legend_names, ncol=4, loc="upper center")
    return fig_xyz


def plot_rpy(trajectories: list[Trajectory]) -> Union[Figure, None]:
    """Plots rpy coordinates of trajectories as subplots"""
    fig_rpy, axs_rpy = plt.subplots(3, 1, sharex=True)

    not_empty = False
    legend_names = []
    for traj in trajectories:
        # rpy fig
        if traj.rot and len(traj.rot) > 0:
            legend_names.append(traj.name)
            rpy = traj.rot.as_euler(seq="xyz")
            ylabels = ["roll [°]", "pitch [°]", "yaw [°]"]
            for j, (ax, yl) in enumerate(zip(axs_rpy, ylabels)):
                rpy_i = np.unwrap(rpy[:, j]) if j < 2 else rpy[:, j]
                ax.plot(traj.function_of, np.rad2deg(rpy_i))
                ax.set_ylabel(yl)
                if j == 2:
                    if traj.sorting == Sorting.CHRONO:
                        ax.set_xlabel("time [s]")
                    else:
                        ax.set_xlabel("trajectory length [m]")
            not_empty = True

    fig_rpy.legend(legend_names, ncol=4, loc="upper center")

    return fig_rpy if not_empty else None


def set_aspect_equal_3d(ax):
    """
    https://stackoverflow.com/a/35126679
    """
    xlim = ax.get_xlim3d()
    ylim = ax.get_ylim3d()
    zlim = ax.get_zlim3d()

    xmean = np.mean(xlim)
    ymean = np.mean(ylim)
    zmean = np.mean(zlim)

    plot_radius = max(
        abs(lim - mean_) for lims, mean_ in ((xlim, xmean), (ylim, ymean), (zlim, zmean)) for lim in lims
    )

    ax.set_xlim3d([xmean - plot_radius, xmean + plot_radius])
    ax.set_ylim3d([ymean - plot_radius, ymean + plot_radius])
    ax.set_zlim3d([zmean - plot_radius, zmean + plot_radius])
