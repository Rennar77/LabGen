import json
def generate_storyboard_from_steps(structured_steps: list) -> list:
    """
    Generates a storyboard with visual descriptions and narration scripts
    from a list of structured protocol steps.
    """
    storyboard = []
    if not structured_steps:
        return storyboard

    for i, step_data in enumerate(structured_steps):
        scene_number = i + 1

        action = step_data.get("action", "perform").lower()
        description = step_data.get("description", "")
        equipment = step_data.get("equipment", [])
        materials = step_data.get("materials", [])

        # Build a rich, context-aware visual description
        equipment_text = ", ".join(equipment) if equipment else "generic lab equipment"
        materials_text = ", ".join(materials) if materials else "unspecified materials"

        visual_description = (
            f"A scientist in a modern laboratory using {equipment_text} "
            f"with {materials_text} while performing the action: {action}. "
            f"The scene should clearly depict: {description}. "
            f"Background shows an appropriate lab environment such as a fume hood or workbench."
        )

        narration_script = f"Step {scene_number}: {description}"

        storyboard.append({
            "scene_number": scene_number,
            "visual_description": visual_description,
            "narration_script": narration_script
        })

    return storyboard
