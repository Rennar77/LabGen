from typing import List, Dict, Any
import re

def parse_protocol(text: str) -> List[Dict[str, Any]]:
    """
    Parses a raw text protocol into a structured list of steps.

    This is a placeholder implementation that splits text by numbered lines or
    newlines and performs simple keyword matching to simulate NLP extraction.
    """
    steps_raw = re.split(r'(?:\r\n|\n|\r)\s*\d+\.\s*', '\n' + text.strip())
    steps_raw = [s.strip() for s in steps_raw if s.strip()]

    if len(steps_raw) <= 1:
        steps_raw = [line.strip() for line in text.splitlines() if line.strip()]

    structured_steps = []
    for i, step_text in enumerate(steps_raw):
        action = "perform"
        equipment = []
        materials = []

        if "pour" in step_text.lower(): action = "pour"
        elif "mix" in step_text.lower(): action = "mix"
        elif "heat" in step_text.lower(): action = "heat"
        elif "measure" in step_text.lower(): action = "measure"
        elif "pipette" in step_text.lower(): action = "pipette"
        elif "centrifuge" in step_text.lower(): action = "centrifuge"
            
        if "beaker" in step_text.lower(): equipment.append("beaker")
        if "flask" in step_text.lower(): equipment.append("flask")
        if "pipette" in step_text.lower(): equipment.append("pipette")
        if "centrifuge" in step_text.lower(): equipment.append("centrifuge")

        if "water" in step_text.lower(): materials.append("water")
        if "acid" in step_text.lower(): materials.append("acid")
        if "solution" in step_text.lower(): materials.append("solution")

        step = {
            "step_number": i + 1,
            "action": action,
            "equipment": equipment or ["generic lab equipment"],
            "materials": materials or ["unspecified materials"],
            "description": step_text
        }
        structured_steps.append(step)

    return structured_steps
