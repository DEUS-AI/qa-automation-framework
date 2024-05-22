from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("templates/jinja"))

# def cypress(test_map, template):
#     '''
#     Creates a cypress file with jinja template rendered mapped values from the acceptance file.

#     @test_map - mapped values from acceptance file

#     @template - which template to use. Possible args are:

#         - start_suite:  use "cypress_start_suite_block" template
#         - end_suite:    use "cypress_end_suite_block" template
#         - before:       use "cypress_before_block" template
#         - before_each:  use "cypress_beforeEach_block" template
#         - after:        use "cypress_after_block" template
#         - after_each:   use "cypress_afterEach_block" template
#         - test:         use "cypress_test_block" template
#     '''
#     rendered_template = ""

#     if template.lower() == "start_suite":
#         rendered_template = environment.get_template("cy_start_suite.j2")
#     elif template.lower() == "end_suite":
#         rendered_template = environment.get_template("cy_end_suite.j2")
#     elif template.lower() == "before":
#         rendered_template = environment.get_template("cy_before_hook.j2")
#     elif template.lower() == "before_each":
#         rendered_template = environment.get_template("cy_beforeEach_hook.j2")
#     elif template.lower() == "after":
#         rendered_template = environment.get_template("cy_after_hook.j2")
#     elif template.lower() == "after_each":
#         rendered_template = environment.get_template("cy_afterEach_hook.j2")
#     elif template.lower() == "test":
#         rendered_template = environment.get_template("cy_test.j2")
#     else:
#         print("Jinja template not supported. Please check valid args or add new templates if needed.")

#     st, tt = "", ""
#     render_tags = ' {tags:'
#     if "suite_tags" in test_map:
#         st = test_map['suite_tags']
#         test_map["suite_tags"] = f"{render_tags} {str(list(test_map['suite_tags'].split(' ')))}" + '},'

#     if "suite_retries" in test_map:
#         if "suite_tags" in test_map:
#             test_map["suite_retries"] = f"{test_map['suite_tags'].split('}')[0]}, retries: {test_map['suite_retries']}" + '},'
#         else:
#             test_map["suite_retries"] = '{' + f"retries: {test_map['suite_retries']}" + '},'

#     if "test_tags" in test_map:
#         tt = test_map['test_tags']
#         test_map["test_tags"] = f"{render_tags} {str(list(test_map['test_tags'].split(' ')))}" + '},'
    
#     if "test_retries" in test_map:
#         if "test_tags" in test_map:
#             test_map["test_tags"] = f"{test_map['test_tags'].split('}')[0]}, retries: {test_map['test_retries']}" + '},'
#         else:
#             test_map["test_tags"] = ' {' + f"retries: {test_map['test_retries']}" + '},'

#     content = rendered_template.render(test_map)    
#     write_template(test_map["cypress_filename"], content, mode = "a")

#     test_map["suite_tags"], test_map["test_tags"] = st, tt

#     return None


# def cypress(test_map, template):
#     '''
#     Creates a Cypress file with a Jinja template rendered with mapped values from the acceptance file.

#     @test_map - mapped values from acceptance file

#     @template - which template to use. Possible args are:

#         - start_suite:  use "cypress_start_suite_block" template
#         - end_suite:    use "cypress_end_suite_block" template
#         - before:       use "cypress_before_block" template
#         - before_each:  use "cypress_beforeEach_block" template
#         - after:        use "cypress_after_block" template
#         - after_each:   use "cypress_afterEach_block" template
#         - test:         use "cypress_test_block" template
#     '''
#     template_mapping = {
#         "start_suite": "cy_start_suite.j2",
#         "end_suite": "cy_end_suite.j2",
#         "before": "cy_before_hook.j2",
#         "before_each": "cy_beforeEach_hook.j2",
#         "after": "cy_after_hook.j2",
#         "after_each": "cy_afterEach_hook.j2",
#         "test": "cy_test.j2"
#     }

#     template_file = template_mapping.get(template.lower())
#     if not template_file:
#         print("Jinja template not supported. Please check valid args or add new templates if needed.")
#         return

#     rendered_template = environment.get_template(template_file)

#     def format_tags_and_retries(tags_key, retries_key):
#         tags = test_map.get(tags_key)
#         retries = test_map.get(retries_key)
        
#         if tags:
#             tags_list = list(tags.split())
#             if retries:
#                 return f" {{tags: {tags_list}, retries: {retries}}},"
#             return f" {{tags: {tags_list}}},"
#         elif retries:
#             return f" {{retries: {retries}}},"
        
#         return ""

#     # Preserve original values
#     original_suite_tags = test_map.get("suite_tags", "")
#     original_test_tags = test_map.get("test_tags", "")
    
#     # Update the test_map with formatted tags and retries
#     test_map["suite_tags"] = format_tags_and_retries("suite_tags", "suite_retries")
#     test_map["test_tags"] = format_tags_and_retries("test_tags", "test_retries")

#     # Render the template with the updated test_map
#     content = rendered_template.render(test_map)
    
#     # Write the rendered content to the specified file
#     write_template(test_map["cypress_filename"], content, mode="a")

#     # Restore the original values to prevent side effects
#     test_map["suite_tags"] = original_suite_tags
#     test_map["test_tags"] = original_test_tags

#     return None

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