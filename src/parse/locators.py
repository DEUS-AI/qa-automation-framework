import yaml
from pathlib import Path
 
def load_all_locators_files():
    '''
    Returns a dictionary with the content of all and only locators.yml files that exists on the project.
    '''
    PATH = "."
    locators_files = list(Path(PATH).glob("**/*locators.yml"))
    locators_list = []

    for file in locators_files:
        f = str(file)
        if f.startswith("automation/support/locators") and f.endswith("locators.yml"):
            with open(f, "r") as stream:
                locators_list.append(yaml.safe_load(stream))

    return {k: v for d in locators_list for k, v in d.items()}

def resolve_locators(locators):
    '''
    Receives a dictionary of locators and returns the same dictionary but with locators type propely matched to cypress values.
    '''
    for loc in locators:

        type = locators.get(loc)["type"]

        if type == "css":
            locators.get(loc)["type"] = "get"
        elif type == "text":
            locators.get(loc)["type"] = "contains"
        elif type == "xpath":
            continue
        else:
            locators.get(loc)["type"] = "get"

    return locators

if __name__ == "__main__":
    pass