HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKCYAN = "\033[96m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
ITAL = "\033[3m"
UNDERLINE = "\033[4m"

def start_processing_test_file(suite_name):
    suite_name = suite_name.replace("automation/acceptance", "..")
    print("\n\033 ======================================================================================================================================= \033[0m")
    print(f"{OKGREEN}Processing file: {suite_name}.yaml\t{'':<5}{ENDC}")
    print("\033 ======================================================================================================================================= \033[0m")
    return None

def end_processing_test_file(file_name, counter):
    print(f"\n{OKCYAN}Total of {'':<2}{counter + 1 if counter != 0 else 1}{'':<2} Test Cases were parsed with success{ENDC}")
    print(f"\n======================================================================================================================================= \n\n")
    return None

def error_test_suite_not_specified(file_name):
    print(f"{FAIL}[ERROR]: \tTestSuite is missing on: {'':<2}{file_name}{ENDC}")
    print(f"\n======================================================================================================================================= \n\n")
    return None

def error_test_suite_title_not_specified(file_name):
    print(f"{FAIL}[ERROR]: \tTestSuite title is missing on: {'':<2}{file_name}{ENDC}")
    print(f"\n======================================================================================================================================= \n\n")
    return None

def error_test_cases_not_specified(file_name):
    print(f"{FAIL}[ERROR]: \tNo TestCases found on: {'':<2}{file_name}{ENDC}")
    print(f"\n======================================================================================================================================= \n\n")
    return None

def error_test_case_not_specified(file_name, test_case_number):
    print(f"{FAIL}[ERROR]: \tNo TestCase found on: \n{'':<5}> File{'':<3}- {file_name} \n{'':<2}> TestCase number\t- {int(test_case_number) + 1}{ENDC}")
    print(f"\n======================================================================================================================================= \n\n")
    return None

def error_test_case_title_not_specified(file_name, test_case_number):
    print(f"{FAIL}[ERROR]: \tTestCase title definition is missing on: \n{'':<5}> File{'':<3}- {file_name} \n{'':<2}> TestCase number{'':<1}- {int(test_case_number) + 1}{ENDC}")
    print(f"\n======================================================================================================================================= \n\n")
    return None

def error_test_case_actions_not_specified(file_name, test_case):
    print(f"{FAIL}[ERROR]: \tTestCase actions definition is missing on: \n{'':<5}> File{'':<3}- {file_name} \n\{'':<2}> TestCase{'':<1}- {test_case}{ENDC}")
    print(f"\n======================================================================================================================================= \n\n")
    return None

def error_action_method_not_defined_or_callable(method):
    print(f"{FAIL}[DEVELOPMENT ERROR]: \tNotCallable or NotFound method: \n\t\t\t> {method}{ENDC}")
    print(f"\n======================================================================================================================================= \n\n")
    return None

def error_action_name_not_defined_in_actions_dict(action):
    print(f"{FAIL}[ERROR]: \t\tAction not suported by the framework: \n\t\t\t> {action}{ENDC}")
    print(f"\n======================================================================================================================================= \n\n")
    return None

def test_data_warning(arg):
    print(f"{WARNING}[WARNING]\t<TestData>\t{'':<5}{ITAL}{arg:<40}{ENDC}{WARNING}{'':<5}is not defined{ENDC}")

def locator_missing_warning(arg):
    print(f"{WARNING}[WARNING]\t<Locator>\t{'':<5}{ITAL}{arg:<30}{ENDC}{WARNING}{'':<5}is not defined{ENDC}")

def action_warning(action):
    print(f"{WARNING}[WARNING]\t<Action>\t{'':<5}{ITAL}{action:<40}{ENDC}{WARNING}{'':<5}is not supported{ENDC}")

if __name__ == "__main__":
    pass