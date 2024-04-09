import templates.actions.cyActions as templateActions
import utils.logs as logs
from jinja2 import Environment, FileSystemLoader
from render.action_methods import ActionMethods

class ActionRenderer:
    def __init__(self):
        self.environment = Environment(loader=FileSystemLoader("templates/actions"))
        self.template_actions = templateActions.template_actions()
        self.action_methods = ActionMethods()

    def render_action(self, action_name, args, locators):
        self.action_template = self.validate_args(action_name, args, locators)

        if isinstance(self.action_template, str):
            return self.action_template

        render_method = getattr(self.action_methods, action_name, None)
        if render_method:
            if args:
                return render_method(self.action_template, args)
            else:
                return render_method(self.action_template)
        else:
            return None

    def validate_args(self, action_name, args, locators):
        if action_name in self.template_actions:
            action_template = self.environment.from_string(self.template_actions[action_name])

            if args.get("element") is not None:
                if args["element"] in locators:
                    args["element"] = locators[args["element"]]
                else:
                    logs.locator_missing_warning(args["element"])
                    return f"throw new Error('Locator {args['element']} not defined')"
            return action_template

        else:
            logs.action_warning(action_name)
            return f"throw new Error('Action {action_name} not supported')"

if __name__ == "__main__":
    pass