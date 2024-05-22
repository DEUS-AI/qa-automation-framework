from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("templates/jinja"))

def cypress(test_map, template):
    '''
    Creates a Cypress file with a Jinja template rendered with mapped values from the acceptance file.

    @test_map - mapped values from acceptance file

    @template - which template to use. Possible args are:

        - start_suite:  use "cypress_start_suite_block" template
        - end_suite:    use "cypress_end_suite_block" template
        - before:       use "cypress_before_block" template
        - before_each:  use "cypress_beforeEach_block" template
        - after:        use "cypress_after_block" template
        - after_each:   use "cypress_afterEach_block" template
        - test:         use "cypress_test_block" template
    '''
    template_mapping = {
        "start_suite": "cy_start_suite.j2",
        "end_suite": "cy_end_suite.j2",
        "before": "cy_before_hook.j2",
        "before_each": "cy_beforeEach_hook.j2",
        "after": "cy_after_hook.j2",
        "after_each": "cy_afterEach_hook.j2",
        "test": "cy_test.j2"
    }

    template_file = template_mapping.get(template.lower())
    if not template_file:
        print("Jinja template not supported. Please check valid args or add new templates if needed.")
        return

    rendered_template = environment.get_template(template_file)

    # Preserve original values
    original_suite_tags = test_map.get("suite_tags", "")
    original_test_tags = test_map.get("test_tags", "")

    # Convert tags to list format
    if "suite_tags" in test_map:
        test_map["suite_tags"] = list(test_map['suite_tags'].split())
    else: 
        test_map["suite_tags"] = []

    if "test_tags" in test_map:
        test_map["test_tags"] = list(test_map['test_tags'].split())
    else:
        test_map["test_tags"] = []

    # Render the template with the updated test_map
    content = rendered_template.render(test_map)

    # Write the rendered content to the specified file
    write_template(test_map["cypress_filename"], content, mode="a")

    # Restore the original values to prevent side effects
    test_map["suite_tags"] = original_suite_tags
    test_map["test_tags"] = original_test_tags

    return None

def write_template(filename, content, mode = "w"):
    '''
    @filename   - cypress filename where rendered jinja template will be written/appended
    @content    - object with all required fields to render jinja template. In this case, it is the test_map object
    @mode       - {optional} mode to write on @filename. Default is "w" (write) but also accepts "a" (append)
    '''
    with open(filename, mode=mode, encoding="utf-8") as message:
        message.write(str(content))
        message.close()
    return ""

if __name__ == "__main__":
    pass