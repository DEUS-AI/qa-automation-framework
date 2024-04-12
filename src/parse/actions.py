from render.action import ActionRenderer
from parse.locators import resolve_locators, load_all_locators_files

def parser(actions):
    '''
    Receives the yaml actions as a list and returns them in the same data type and ready to be rendered with a cypress jinja template.
    '''
    rendered_action_list = ""
    locators = load_all_locators_files()
    res_locators = resolve_locators(locators)
    action_renderer = ActionRenderer()

    for index, action in enumerate(actions):
        action_name = next(iter(action)) if type(action) is not str else action
        action_args = action[next(iter(action))] if type(action) is not str else {}

        rendered_action = "\t\t" + action_renderer.render_action(action_name, action_args, res_locators)

        if index == 0: 
            rendered_action = rendered_action.replace(".then(() => {", "", 1).rsplit("})", 1)[0]
            rendered_action = rendered_action.replace("\t", "", 1) + "\n"
        
        rendered_action_list = rendered_action_list + rendered_action

        if "throw new Error" not in rendered_action_list: continue 
        else: break

    return rendered_action_list

if __name__ == "__main__":
    pass