"""driveClosedLoop must use the motor functions L1_motor (Pi) defines."""
import os
import sys
import types
from unittest import mock

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_drive_closed_loop_sends_to_both_motors():
    gpiozero = types.ModuleType("gpiozero")
    gpiozero.PWMOutputDevice = mock.MagicMock()
    with mock.patch.dict(sys.modules, {"gpiozero": gpiozero}):
        sys.modules.pop("L1_motor", None)
        sys.modules.pop("L2_speed_control", None)
        import L1_motor
        import L2_speed_control as sc

        with mock.patch.object(L1_motor, "sendLeft") as left, \
                mock.patch.object(L1_motor, "sendRight") as right:
            sc.driveClosedLoop(np.array([2.0, -2.0]), np.array([0.0, 0.0]), np.zeros(2))

    assert left.call_count == 1 and right.call_count == 1
    assert left.call_args[0][0] > 0 > right.call_args[0][0]
