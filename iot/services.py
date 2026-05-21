import logging
from typing import Any, Optional
from .models import SoilMoisture, MotorState

logger = logging.getLogger('iot')

MOISTURE_LOW = 35.0
MOISTURE_HIGH = 45.0


def _find_numeric_value(obj: Any) -> Optional[float]:
    """Recursively search for the first numeric value in a nested JSON-like structure."""
    if obj is None:
        return None

    if isinstance(obj, (int, float)):
        try:
            return float(obj)
        except (TypeError, ValueError):
            return None

    if isinstance(obj, dict):
        for v in obj.values():
            val = _find_numeric_value(v)
            if val is not None:
                return val

    if isinstance(obj, (list, tuple)):
        for item in obj:
            val = _find_numeric_value(item)
            if val is not None:
                return val

    return None


def determine_motor_state(latest_reading: dict, threshold: float) -> dict:
    """
    Determine desired motor state based on the latest reading and a threshold.
    """
    try:
        value = _find_numeric_value(latest_reading)

        if value is None:
            logger.warning("No numeric sensor value found in latest reading")
            return {
                'motor_state': 'unknown',
                'reason': 'no_numeric_value_found',
                'reading_value': None,
            }

        if value < float(threshold):
            return {
                'motor_state': 'on',
                'reason': f'value_below_threshold ({value} < {threshold})',
                'reading_value': value,
            }

        return {
            'motor_state': 'off',
            'reason': f'value_at_or_above_threshold ({value} >= {threshold})',
            'reading_value': value,
        }

    except Exception:
        logger.exception("Error determining motor state")
        return {
            'motor_state': 'unknown',
            'reason': 'error_evaluating_reading',
            'reading_value': None,
        }


def update_motor_state() -> None:
    """
    Updates the persistent MotorState based on the most recent SoilMoisture logic.
    """
    latest = SoilMoisture.objects.order_by("-created_at").first()

    if not latest:
        return

    # Use the robust numeric finder instead of hardcoding key lookup
    moisture = _find_numeric_value(latest.data)
    if moisture is None:
        return

    motor_state, _ = MotorState.objects.get_or_create(id=1)

    if moisture < MOISTURE_LOW:
        motor_state.is_on = True
    elif moisture > MOISTURE_HIGH:
        motor_state.is_on = False

    motor_state.save()
