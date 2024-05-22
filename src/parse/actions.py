from render.action import ActionRenderer
from parse.locators import resolve_locators, load_all_locators_files
from typing import List, Union, Dict

REMOVE_CALLBACK_FROM = ["setLocalStorage", "setSessionStorage"]
THEN_CALLBACK_START = ".then(() => {"
THEN_CALLBACK_END = "})"

def parser(actions: List[Union[str, Dict[str, Dict]]]) -> str:
    """
    Receives the yaml actions as a list and returns them as a string
    ready to be rendered with a Cypress Jinja template.
    """
    rendered_action_list = []
    prev_action_name = ""
    prev_rendered_action = ""
    
    locators = load_all_locators_files()
    res_locators = resolve_locators(locators)
    action_renderer = ActionRenderer()

    for index, action in enumerate(actions):
        if isinstance(action, str):
            action_name = action
            action_args = {}
        else:
            action_name = next(iter(action))
            action_args = action[action_name]

        rendered_action = "\t\t" + action_renderer.render_action(action_name, action_args, res_locators)

        if index == 0 or (prev_action_name in REMOVE_CALLBACK_FROM and THEN_CALLBACK_START not in prev_rendered_action):
            rendered_action = rendered_action.replace(THEN_CALLBACK_START, "", 1).rsplit(THEN_CALLBACK_END, 1)[0]
            rendered_action = rendered_action.replace("\t", "", 1) + "\n"

        rendered_action_list.append(rendered_action)
        prev_action_name = action_name
        prev_rendered_action = rendered_action

        if "throw new Error" in rendered_action_list:
            break

    return ''.join(rendered_action_list)

if __name__ == "__main__":
    pass