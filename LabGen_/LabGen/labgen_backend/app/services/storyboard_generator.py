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
        
        # Extract details from the parsed step
        action = step_data.get('action', 'perform an action').lower()
        details = step_data.get('details', 'as specified').lower()
        full_step_text = step_data.get('step', 'Proceed with the next action.')

        # Create a detailed visual description for an image/video generator
        visual_description = (
            f"A scientist in a clean, modern laboratory, wearing a lab coat and safety glasses. "
            f"The scientist is carefully {action} {details}. "
            f"The scene focuses on the equipment being used, showing the action with precision. "
            f"Background shows relevant lab environment (e.g., chemical fume hood, cell culture cabinet, physics workbench)."
        )
        
        # Create a clear narration script for a TTS engine
        narration_script = f"Step {scene_number}: {full_step_text}"

        storyboard.append({
            "scene_number": scene_number,
            "visual_description": visual_description,
            "narration_script": narration_script,
        })
    
    return storyboard

