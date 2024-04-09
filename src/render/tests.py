from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("templates/jinja"))

def cypress(test_map, template):
    '''
    Creates a cypress file with jinja template rendered mapped values from the acceptance file.

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
    rendered_template = ""

    if template.lower() == "start_suite":
        rendered_template = environment.get_template("cy_start_suite.j2")
    elif template.lower() == "end_suite":
        rendered_template = environment.get_template("cy_end_suite.j2")
    elif template.lower() == "before":
        rendered_template = environment.get_template("cy_before_hook.j2")
    elif template.lower() == "before_each":
        rendered_template = environment.get_template("cy_beforeEach_hook.j2")
    elif template.lower() == "after":
        rendered_template = environment.get_template("cy_after_hook.j2")
    elif template.lower() == "after_each":
        rendered_template = environment.get_template("cy_afterEach_hook.j2")
    elif template.lower() == "test":
        rendered_template = environment.get_template("cy_test.j2")
    else:
        print("Jinja template not supported. Please check valid args or add new templates if needed.")

    st, tt = "", ""
    render_tags = ' {tags:'
    if "suite_tags" in test_map:
        st = test_map['suite_tags']
        test_map["suite_tags"] = f"{render_tags} {str(list(test_map['suite_tags'].split(' ')))}" + '},'

    if "test_tags" in test_map:
        tt = test_map['test_tags']
        test_map["test_tags"] = f"{render_tags} {str(list(test_map['test_tags'].split(' ')))}" + '},'
        
    content = rendered_template.render(test_map)    
    write_template(test_map["cypress_filename"], content, mode = "a")

    test_map["suite_tags"], test_map["test_tags"] = st, tt

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