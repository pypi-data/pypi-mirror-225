"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import logging

from typing import Tuple, Union

import numpy as np
from trajectopy.settings.comparison_settings import ComparisonMethod, ComparisonSettings, RelativeMode
from pointset import PointSet

import trajectopy.util.datahandling as datahandling
from trajectopy.evaluation.matching import match_trajectories
from trajectopy.evaluation.trajectory_deviations import AbsoluteTrajectoryDeviations, RelativeTrajectoryDeviations
from trajectopy.trajectory import Trajectory
from trajectopy.util.rotationset import RotationSet
from trajectopy.util.spatialsorter import Sorting

logger = logging.getLogger("root")


def compare_trajectories(
    traj_test: Trajectory, traj_ref: Trajectory, settings: ComparisonSettings
) -> Union[AbsoluteTrajectoryDeviations, RelativeTrajectoryDeviations]:
    """Compare trajectories

    Compare trajectories using either absolute or relative comparison.
    Before the comparison, the trajectories are matched using one of the
    following methods:
    - nearest neighbor (spatially)
    - nearest neighbor (temporally)
    - interpolation

    Args:
        traj_test (Trajectory): Trajectory that should be compared.
        traj_ref (Trajectory): Reference trajectory.
        settings (ComparisonSettings): Settings for the comparison.

    Returns:
        TrajectoryDeviations: Holding the computed deviations.
    """
    print(settings)
    traj_test, traj_ref = match_trajectories(
        traj_test=traj_test, traj_ref=traj_ref, settings=settings.type.matching_settings
    )

    if len(traj_ref) != len(traj_test):
        raise ValueError("Something went wrong during matching.")

    if settings.type.comparison_method == ComparisonMethod.ABSOLUTE:
        return compare_trajectories_absolute(traj_test=traj_test, traj_ref=traj_ref, settings=settings)

    if settings.type.comparison_method == ComparisonMethod.RELATIVE:
        return compare_trajectories_relative(traj_test=traj_test, traj_ref=traj_ref, settings=settings)

    raise ValueError("Invalid comparison method.")


def compare_trajectories_absolute(
    *, traj_test: Trajectory, traj_ref: Trajectory, settings: ComparisonSettings
) -> AbsoluteTrajectoryDeviations:
    """
    Compares two trajectories in absolute terms, returning the deviations between them.

    Args:
        traj_test (Trajectory): The trajectory to be tested.
        traj_ref (Trajectory): The reference trajectory.
        settings (ComparisonSettings): The settings for the comparison.

    Returns:
        AbsoluteTrajectoryDeviations: An object containing the absolute deviations between the two trajectories.
    """
    logger.info("Performing absolute comparison")
    pos_dev = traj_ref.pos.xyz - traj_test.pos.xyz
    directed_pos_dev = get_directed_deviations(
        xyz_ref=traj_ref.pos.xyz, xyz_test=traj_test.pos.xyz, rot=traj_ref.rot or traj_test.rot
    )

    if traj_ref.rot is not None and traj_test.rot is not None:
        rot_dev = traj_ref.rot - traj_test.rot
    else:
        rot_dev = None

    return AbsoluteTrajectoryDeviations(
        name=f"{traj_test.name} vs. {traj_ref.name}",
        tstamps=traj_test.tstamps,
        arc_lengths=traj_test.arc_lengths,
        pos=traj_test.pos,
        rot=traj_test.rot,
        pos_dev=pos_dev,
        directed_pos_dev=directed_pos_dev,
        rot_dev=rot_dev,
        sort_index=traj_ref.sort_index,
        sorting=traj_ref.sorting,
        rotations_used=(traj_ref.rot or traj_test.rot) is not None,
        comparison_type=settings.type,
    )


def compare_trajectories_relative_distance(
    *,
    traj_test: Trajectory,
    traj_ref: Trajectory,
    settings: ComparisonSettings,
) -> RelativeTrajectoryDeviations:
    """This function compares two trajectories using the relative comparison method.

    This metric evaluates the drift of the trajectory as a function of
    the distance. The trajectory is split into pairs of points
    that are separated by at least a given time distance. The relative
    pose difference are compared between the reference and the test trajectory.

    Args:
        traj_test (Trajectory): Test trajectory.
        traj_ref (Trajectory): Reference trajectory.
        settings (ComparisonSettings): Comparison settings.

    Returns:
        RelativeTrajectoryDeviations: Relative trajectory deviations.
    """
    traj_ref = traj_ref.set_sorting(sorting=Sorting.CHRONO, inplace=False)
    traj_test = traj_test.set_sorting(sorting=Sorting.CHRONO, inplace=False)

    pair_indices = _get_pair_indices_dist(traj_ref, settings)

    return pairwise_comparison(traj_test=traj_test, traj_ref=traj_ref, pair_indices=pair_indices, settings=settings)


def compare_trajectories_relative_time(
    *,
    traj_test: Trajectory,
    traj_ref: Trajectory,
    settings: ComparisonSettings,
) -> RelativeTrajectoryDeviations:
    """This function compares two trajectories using the relative comparison method.

    This metric evaluates the drift of the trajectory as a function of
    the elapsed time. The trajectory is split into pairs of points
    that are separated by at least a given time difference. The relative
    pose difference are compared between the reference and the test trajectory.

    Args:
        traj_test (Trajectory): Test trajectory.
        traj_ref (Trajectory): Reference trajectory.
        settings (ComparisonSettings): Comparison settings.

    Returns:
        RelativeTrajectoryDeviations: Relative trajectory deviations.
    """
    traj_ref = traj_ref.set_sorting(sorting=Sorting.CHRONO, inplace=False)
    traj_test = traj_test.set_sorting(sorting=Sorting.CHRONO, inplace=False)

    pair_indices = _get_pair_indices_time(traj_ref, settings)

    return pairwise_comparison(traj_test=traj_test, traj_ref=traj_ref, pair_indices=pair_indices, settings=settings)


def _get_pair_indices_time(traj_ref: Trajectory, settings: ComparisonSettings) -> np.ndarray:
    if settings.use_all_pose_pairs:
        time_steps = np.array(
            [
                [i, tstamp + settings.relative_pair_time_difference]
                for i, tstamp in enumerate(traj_ref.tstamps)
                if (tstamp + settings.relative_pair_time_difference) < traj_ref.tstamps[-1]
            ],
            dtype=float,
        )
        indices_end = np.searchsorted(traj_ref.tstamps, time_steps[:, 1])
        return np.c_[time_steps[:, 0].astype(int), indices_end]

    time_steps = np.arange(
        traj_ref.tstamps[0],
        traj_ref.tstamps[-1],
        settings.relative_pair_time_difference,
    )

    indices = np.searchsorted(traj_ref.tstamps, time_steps)
    return np.c_[indices[:-1], indices[1:]]


def _get_pair_indices_dist(traj_ref: Trajectory, settings: ComparisonSettings) -> np.ndarray:
    if settings.use_all_pose_pairs:
        dist_steps = np.array(
            [
                [i, arc_length + settings.relative_pair_distance]
                for i, arc_length in enumerate(traj_ref.arc_lengths)
                if (arc_length + settings.relative_pair_distance) < traj_ref.arc_lengths[-1]
            ],
            dtype=float,
        )
        indices_end = np.searchsorted(traj_ref.arc_lengths, dist_steps[:, 1])
        return np.c_[dist_steps[:, 0].astype(int), indices_end]

    dist_steps = np.arange(
        traj_ref.arc_lengths[0],
        traj_ref.arc_lengths[-1],
        settings.relative_pair_distance,
    )

    indices = np.searchsorted(traj_ref.arc_lengths, dist_steps)
    return np.c_[indices[:-1], indices[1:]]


def pairwise_comparison(
    *, traj_test: Trajectory, traj_ref: Trajectory, pair_indices: np.ndarray, settings: ComparisonSettings
) -> RelativeTrajectoryDeviations:
    if len(pair_indices) == 0:
        raise ValueError("No pairs found")

    pos_dev = []
    ref_dev = []
    test_dev = []
    rot_dev = []
    pair_distance = []
    pair_time_difference = []

    for pair in pair_indices:
        ref_translation_diff = traj_ref.pos.xyz[pair[1]] - traj_ref.pos.xyz[pair[0]]
        test_translation_diff = traj_test.pos.xyz[pair[1]] - traj_test.pos.xyz[pair[0]]
        ref_dev.append(ref_translation_diff)
        test_dev.append(test_translation_diff)
        pos_dev.append(np.abs(ref_translation_diff - test_translation_diff))

        if traj_ref.rot is not None and traj_test.rot is not None:
            ref_rotation_diff = traj_ref.rot[pair[1]] - traj_ref.rot[pair[0]]
            test_rotation_diff = traj_test.rot[pair[1]] - traj_test.rot[pair[0]]
            rot_dev.append((ref_rotation_diff - test_rotation_diff).as_quat())

        pair_distance.append(traj_ref.arc_lengths[pair[1]] - traj_ref.arc_lengths[pair[0]])
        pair_time_difference.append(traj_ref.tstamps[pair[1]] - traj_ref.tstamps[pair[0]])

    pos = PointSet(xyz=traj_ref.pos.xyz[pair_indices[:, 0]], epsg=traj_ref.pos.epsg)
    norm_pos_dev = np.abs(np.linalg.norm(np.array(ref_dev), axis=1) - np.linalg.norm(np.array(test_dev), axis=1))
    return RelativeTrajectoryDeviations(
        name=f"{traj_test.name} vs. {traj_ref.name}",
        pair_distances=np.array(pair_distance),
        pair_time_differences=np.array(pair_time_difference),
        pos=pos,
        pos_dev=np.array(pos_dev),
        norm_pos_dev=norm_pos_dev,
        rot_dev=RotationSet.from_quat(np.array(rot_dev)) if rot_dev else None,
        comparison_type=settings.type,
    )


def compare_trajectories_relative(
    *,
    traj_test: Trajectory,
    traj_ref: Trajectory,
    settings: ComparisonSettings,
) -> RelativeTrajectoryDeviations:
    """This function compares two trajectories using the relative comparison method.

    It will perform two comparisons, one based on the distance and one based on the time.

    Args:
        traj_test (Trajectory): Test trajectory.
        traj_ref (Trajectory): Reference trajectory.
        settings (ComparisonSettings): Comparison settings.

    Returns:
        Tuple[RelativeTrajectoryDeviations, RelativeTrajectoryDeviations]:
                                    Distance and time based relative trajectory deviations.
    """
    logger.info("Performing relative comparison")
    if settings.type.relative_mode == RelativeMode.DISTANCE:
        return compare_trajectories_relative_distance(traj_test=traj_test, traj_ref=traj_ref, settings=settings)

    if settings.type.relative_mode == RelativeMode.TIME:
        return compare_trajectories_relative_time(traj_test=traj_test, traj_ref=traj_ref, settings=settings)


def get_directed_deviations(
    *, xyz_ref: np.ndarray, xyz_test: np.ndarray, rot: Union[RotationSet, None] = None
) -> np.ndarray:
    if rot is None:
        return derive_dev_directions_no_rot(xyz_ref=xyz_ref, xyz_test=xyz_test)

    return derive_dev_directions_with_rot(xyz_ref=xyz_ref, xyz_test=xyz_test, rot=rot)


def derive_dev_directions_no_rot(*, xyz_ref: np.ndarray, xyz_test: np.ndarray) -> np.ndarray:
    """
    Function that computes along-track and cross-track deviations
    between two synchronized trajectories.

    By constructing a 3D line between the corresponding point in xyz_ref and
    its successor (predecessor for the last point) one can determine the
    cross- and along-track deviations for each point in xyz_test
    """
    N = len(xyz_test)

    # initialize zero arrays
    d_along = np.zeros((N, 1))
    d_cross_h = np.zeros((N, 1))
    d_cross_v = np.zeros((N, 1))

    for i in range(N):
        cnt = 1
        p_curr = xyz_ref[i, :]
        is_last = i == N - 1

        p_next = xyz_ref[i - cnt, :] if is_last else xyz_ref[i + cnt, :]

        # if both points are (almost) identical, there is no way to reliably
        # destinguish between right and left sided deviations
        while np.allclose(p_curr, p_next) and i + cnt < N - 1:
            cnt += 1
            p_next = xyz_ref[i - cnt, :] if is_last else xyz_ref[i + cnt, :]

        line_pts = [p_next, p_curr] if is_last else [p_curr, p_next]

        d_cross_h[i], d_cross_v[i] = _cross_track_dev(p=xyz_test[i, :], line_pts=line_pts)
        d_along[i] = _along_track_dev(p=xyz_test[i, :], line_pts=line_pts, is_last=is_last)

    return np.c_[d_along, d_cross_h, d_cross_v]


def derive_dev_directions_with_rot(*, xyz_ref: np.ndarray, xyz_test: np.ndarray, rot: RotationSet) -> np.ndarray:
    """
    Function that computes the deviation between ref and single with
    respect to coordinate axes defined by rpy
    """
    devs = np.zeros((len(xyz_test), 3))

    rot_matrices = rot.as_matrix()

    for i in range(len(xyz_ref)):
        # transform to body system
        devs[i, :] = (xyz_test[i, :] - xyz_ref[i, :]) @ rot_matrices[i]

    return devs


def _along_track_dev(*, p: np.ndarray, line_pts: list, is_last: bool) -> float:
    """
    Helper function that computes the along track deviation
    """
    a = line_pts[0]
    b = line_pts[1]
    p_nearest, t = datahandling.nearest_point(p=p, line_pts=line_pts)

    if not is_last:
        return np.sign(t) * np.linalg.norm(p_nearest - a)

    return float(
        -np.linalg.norm(p_nearest - b)
        if np.linalg.norm(b - a) > np.linalg.norm(p_nearest - a)
        else np.linalg.norm(p_nearest - b)
    )


def _cross_track_dev(*, p: np.ndarray, line_pts: list, z_slope_dist: bool = False) -> Tuple[float, float]:
    """
    Helper function that computes the cross track deviation
    """
    a = line_pts[0]
    b = line_pts[1]
    p_nearest, _ = datahandling.nearest_point(p=p, line_pts=line_pts)

    # Determine the sign (left or right of the approximation).
    # It is important that the normal vector is always constructed
    # the same, i.e. is always aligned the same relative to the
    # 3d line. A construction with the help of the nearest point on the
    # line and the point p, is therefore out of the question.
    # The angle between the normal vector and the vector between a and p
    # is calculated indirectly. If the angle is smaller than 90°, the
    # point lies on one side of the straight line, with >90° the point
    # lies on the other side of the straight line. It is not necessary
    # to explicitly calculate the angle. The calculation of the scalar
    # product or the determination of its sign is sufficient.

    n = [b[1] - a[1], -(b[0] - a[0])]
    d = p[:2] - a[:2]
    d_sign = -np.sign(d @ n)
    diff = p_nearest - p
    d_cross_h = d_sign * np.sqrt(diff[0] ** 2 + diff[1] ** 2)
    z_diff = diff[2]
    if z_slope_dist:
        angle_z = np.arctan2(b[1] - a[1], b[0] - a[0])
        gamma = np.pi / 2 + angle_z
        rotm = np.array(
            [
                [np.cos(gamma), -np.sin(gamma), 0],
                [np.sin(gamma), np.cos(gamma), 0],
                [0, 0, 1],
            ]
        )
        diff_rot = rotm @ p - rotm @ p_nearest
        d_cross_v = np.sign(z_diff) * np.sqrt(diff_rot[0] ** 2 + diff_rot[2] ** 2)
    else:
        d_cross_v = z_diff
    return d_cross_h, d_cross_v
