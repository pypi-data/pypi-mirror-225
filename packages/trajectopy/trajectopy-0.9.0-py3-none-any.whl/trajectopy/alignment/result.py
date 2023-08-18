"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass, field

from trajectopy.alignment.parameters import AlignmentParameters, SensorRotationParameters
from trajectopy.settings.alignment_settings import AlignmentEstimationSettings


@dataclass
class AlignmentResult:
    name: str = "Alignment Result"
    position_parameters: AlignmentParameters = field(default_factory=AlignmentParameters)
    rotation_parameters: SensorRotationParameters = field(default_factory=SensorRotationParameters)
    estimation_of: AlignmentEstimationSettings = field(default_factory=AlignmentEstimationSettings)
