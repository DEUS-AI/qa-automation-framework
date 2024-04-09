import parse.actions
import render.tests
import utils.preprocessor as preprocessor
import utils.logs as logs

acceptance_files = preprocessor.get_all_acceptance_files()

# import_all_commands_files()

### render cypress tests
for acceptance_file in acceptance_files:

    logs.start_processing_test_file(acceptance_file["filename"])

    cy_filename = preprocessor.create_cy_test(acceptance_file["filename"])

    test_map = {}
    test_map["cypress_filename"] = cy_filename
    test_map["suite_title"] = acceptance_file["TestSuite"]["Title"]

    if "Tags" in acceptance_file["TestSuite"].keys(): 
        test_map["suite_tags"] = acceptance_file["TestSuite"]["Tags"]
    
    render.tests.cypress(test_map, "start_suite")

    if "Hooks" in acceptance_file.keys():
        if "Before" in acceptance_file["Hooks"]:
            test_map["before_steps"] = parse.actions.parser(acceptance_file["Hooks"]["Before"].get("Actions"))
            render.tests.cypress(test_map, "before")
        
        if "BeforeEach" in acceptance_file["Hooks"]:
            test_map["beforeEach_steps"] = parse.actions.parser(acceptance_file["Hooks"]["BeforeEach"].get("Actions"))
            render.tests.cypress(test_map, "before_each")

        if "After" in acceptance_file["Hooks"]:
            test_map["after_steps"] = parse.actions.parser(acceptance_file["Hooks"]["After"].get("Actions"))
            render.tests.cypress(test_map, "after")

        if "AfterEach" in acceptance_file["Hooks"]:
            test_map["afterEach_steps"] = parse.actions.parser(acceptance_file["Hooks"]["AfterEach"].get("Actions"))
            render.tests.cypress(test_map, "after_each")

    for i, test in enumerate(acceptance_file["TestCases"]):
        test_map["test_title"] = test["Title"]

        if "test_tags" in test_map: del test_map["test_tags"]
        if "Tags" in test.keys():
            test_map["test_tags"] = test["Tags"]
        
        test_map["test_steps"] = parse.actions.parser(test["Actions"])

        render.tests.cypress(test_map, "test")  

    render.tests.cypress(test_map, "end_suite")

    logs.end_processing_test_file(acceptance_file["filename"], i)


if __name__ == "__main__":
    pass