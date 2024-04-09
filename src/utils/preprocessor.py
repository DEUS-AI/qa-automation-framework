import os, sys
import yaml
from pathlib import Path
import utils.logs as logs


def get_all_acceptance_files():
    '''
    Returns a list with the content (as json obj) of all and only acceptance yml files that exists on the project.
    '''

    PATH = "."
    acceptance_files = list(Path(PATH).glob("**/*.yml"))
    tests_list = []

    for files_in_folders in acceptance_files:
        f = str(files_in_folders)
        if f.startswith("automation/acceptance") and f.endswith(".yml") and load_tests(f) is not None:
            tests_list.append(load_tests(f))
    
    return tests_list

def load_tests(file_name: str) -> object:
    '''
    Loads given acceptance yaml filename, validates if mandatory fields are filled and returns the file content as a json object.

    In case one or more test files contains any missing mandatory field, prints a console warning and terminates the proccess.

    @filename - name of the acceptance file to be analyzed
    '''
    with open(file_name, "r") as stream:
        data = yaml.safe_load(stream)

        if data.get("TestSuite") == None: 
            logs.error_test_suite_not_specified(file_name)
            sys.exit()
        elif data["TestSuite"].get("Title") == None: 
            logs.error_test_suite_title_not_specified(file_name)
            sys.exit()
        elif data.get("TestCases") == None or data["TestCases"] == []:
            logs.error_test_cases_not_specified(file_name)
            sys.exit()

        #### TODO need to implement same validation logic for suite hooks
        
        for index, testcase in enumerate(data["TestCases"]):

            if testcase == None:
                logs.error_test_case_not_specified(file_name, index)
                sys.exit()
            elif testcase.get("Title") == None:
                logs.error_test_case_title_not_specified(file_name, index)
                sys.exit()
            elif testcase.get("Actions") == None:
                logs.error_test_case_actions_not_specified(file_name, testcase.get("Title"))
                sys.exit()
    
        else:
            data["filename"] = file_name.replace(".yml", "")
            return data

def create_cy_test(acc_filename: str):
    '''
    Receives the acceptance file name and creates a Cypress file with the same name.

    Returns the cypress file path.

    @acc_filename:    acceptance file content
    '''
    
    p = f"cy_tests/{'/'.join(acc_filename.split('/')[:-1])}".replace("/automation/acceptance", "")
     
    if not os.path.exists(p):
        os.makedirs(p)

    file_path = os.path.join(p, os.path.basename(acc_filename)) + ".cy.js"

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('')
    
    return file_path

def import_all_commands_files():
    '''
    Checks the existence of js files in support/commands and, for each file found, add an import statement in the cypress/support/e2e,js file
    '''
    try:
        if len(list(Path("../support/commands").glob("*.js"))) > 0:
            for f in list(Path("../support/commands").glob("*.js")):
                fname = str(f).split("support/commands/")[1]
                with open("cypress/support/e2e.js", mode="a", encoding="utf-8") as message:
                    message.write(f"\nimport './commands/{fname}'")
                    message.close()
    except:
        print("No command files found.")

if __name__ == "__main__":
    pass