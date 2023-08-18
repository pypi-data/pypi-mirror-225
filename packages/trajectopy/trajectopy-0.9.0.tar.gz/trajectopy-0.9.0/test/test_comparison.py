import unittest

import numpy as np
from test.util import random_number
from test.testdata import generated_trajectory as generated_trajectory
from trajectopy.alignment.parameters import AlignmentParameters, Parameter
from trajectopy.alignment.result import AlignmentResult
from trajectopy.evaluation.comparison import compare_trajectories
from trajectopy.settings.comparison_settings import (
    ComparisonMethod,
    ComparisonSettings,
    ComparisonType,
    MatchingMethod,
    MatchingSettings,
    RelativeMode,
)
from trajectopy.util.definitions import Unit


class TestComparison(unittest.TestCase):
    def test_body_frame_deviations(self) -> None:
        trajectory = generated_trajectory.copy()

        parameters = AlignmentParameters(
            lever_x=Parameter(value=random_number(min=-1, max=1), unit=Unit.METER),
            lever_y=Parameter(value=random_number(min=-1, max=1), unit=Unit.METER),
            lever_z=Parameter(value=random_number(min=-1, max=1), unit=Unit.METER),
        )
        transformed = generated_trajectory.apply_alignment(
            AlignmentResult(position_parameters=parameters), inplace=False
        )

        settings = ComparisonSettings(
            type=ComparisonType(
                comparison_method=ComparisonMethod.ABSOLUTE,
                matching_settings=MatchingSettings(method=MatchingMethod.NEAREST_TEMPORAL),
            )
        )

        deviations = compare_trajectories(traj_ref=trajectory, traj_test=transformed, settings=settings)

        np.testing.assert_almost_equal(deviations.bias_along, parameters.lever_x.value)
        np.testing.assert_almost_equal(deviations.bias_cross_h, parameters.lever_y.value)
        np.testing.assert_almost_equal(deviations.bias_cross_v, parameters.lever_z.value)

    def test_xyz_deviations(self) -> None:
        trajectory = generated_trajectory.copy()

        parameters = AlignmentParameters(
            sim_trans_x=Parameter(value=random_number(min=-1, max=1), unit=Unit.METER),
            sim_trans_y=Parameter(value=random_number(min=-1, max=1), unit=Unit.METER),
            sim_trans_z=Parameter(value=random_number(min=-1, max=1), unit=Unit.METER),
        )
        transformed = generated_trajectory.apply_alignment(
            AlignmentResult(position_parameters=parameters), inplace=False
        )

        settings = ComparisonSettings(
            type=ComparisonType(
                comparison_method=ComparisonMethod.ABSOLUTE,
                matching_settings=MatchingSettings(method=MatchingMethod.NEAREST_TEMPORAL),
            )
        )

        deviations = compare_trajectories(traj_ref=trajectory, traj_test=transformed, settings=settings)

        np.testing.assert_almost_equal(-deviations.bias_x, parameters.sim_trans_x.value)
        np.testing.assert_almost_equal(-deviations.bias_y, parameters.sim_trans_y.value)
        np.testing.assert_almost_equal(-deviations.bias_z, parameters.sim_trans_z.value)

    def test_relative_deviations(self) -> None:
        trajectory = generated_trajectory.copy()
        transformed = generated_trajectory.copy()

        x_random = np.random.randn(len(transformed)) * 0.1
        y_random = np.random.randn(len(transformed)) * 0.1
        z_random = np.random.randn(len(transformed)) * 0.1
        transformed.pos.xyz += np.c_[x_random, y_random, z_random]

        x_diff = np.abs(np.diff(x_random))
        y_diff = np.abs(np.diff(y_random))
        z_diff = np.abs(np.diff(z_random))

        settings = ComparisonSettings(
            type=ComparisonType(
                comparison_method=ComparisonMethod.RELATIVE,
                matching_settings=MatchingSettings(method=MatchingMethod.NEAREST_TEMPORAL),
                relative_mode=RelativeMode.TIME,
            ),
            use_all_pose_pairs=True,
            relative_pair_time_difference=1.0,
        )

        deviations_time = compare_trajectories(traj_ref=trajectory, traj_test=transformed, settings=settings)

        np.testing.assert_almost_equal(deviations_time.x_drift_per_second, x_diff[:-1])
        np.testing.assert_almost_equal(deviations_time.y_drift_per_second, y_diff[:-1])
        np.testing.assert_almost_equal(deviations_time.z_drift_per_second, z_diff[:-1])

        np.testing.assert_almost_equal(
            deviations_time.x_drift_per_meter, (x_diff / np.diff(trajectory.arc_lengths))[:-1]
        )
        np.testing.assert_almost_equal(
            deviations_time.y_drift_per_meter, (y_diff / np.diff(trajectory.arc_lengths))[:-1]
        )
        np.testing.assert_almost_equal(
            deviations_time.z_drift_per_meter, (z_diff / np.diff(trajectory.arc_lengths))[:-1]
        )

        settings.type.relative_mode = RelativeMode.DISTANCE
        settings.relative_pair_distance = 1.0

        deviations_dist = compare_trajectories(traj_ref=trajectory, traj_test=transformed, settings=settings)
        np.testing.assert_almost_equal(deviations_dist.x_drift_per_second, x_diff)
        np.testing.assert_almost_equal(deviations_dist.y_drift_per_second, y_diff)
        np.testing.assert_almost_equal(deviations_dist.z_drift_per_second, z_diff)

        np.testing.assert_almost_equal(deviations_dist.x_drift_per_meter, (x_diff / np.diff(trajectory.arc_lengths)))
        np.testing.assert_almost_equal(deviations_dist.y_drift_per_meter, (y_diff / np.diff(trajectory.arc_lengths)))
        np.testing.assert_almost_equal(deviations_dist.z_drift_per_meter, (z_diff / np.diff(trajectory.arc_lengths)))
