import json
import yaml
import logging
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from jira import JIRA
from jinja2 import Environment, FileSystemLoader
import os 
import requests

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_jira_config_values():
    env = Environment(loader=FileSystemLoader('./../automation/support/'))

    with open("./../automation/support/secrets.yml", 'r') as stream:
        variable_values = yaml.safe_load(stream)
        template = env.get_template('config.yml')
        rendered_yaml = template.render(**variable_values)

        return yaml.safe_load(rendered_yaml)

def load_json(json_file):
    with open(json_file) as f:
        return json.load(f)

def convert_milliseconds_to_time(milliseconds):
    seconds = milliseconds / 1000.0
    time_obj = datetime.fromtimestamp(seconds)
    return time_obj.strftime('%H:%M:%S')

def merge_report_json_files(final_json):
    final_json_enhanced = []

    for ts in final_json:
        try:
            test_set_file = ts["results"][0]["file"].replace(".cy.js", ".yml").replace("cypress/", "automation/")
            test_set_title = ts["results"][0]["suites"][0]["title"]
            test_set_duration = ts["results"][0]["suites"][0]["duration"]
            test_set_stats = ts["stats"]
            test_cases = ts["results"][0]["suites"][0]["tests"]
            test_cases_passed = ts["results"][0]["suites"][0]["passes"]
            test_cases_failed = ts["results"][0]["suites"][0]["failures"]
            test_cases_pending = ts["results"][0]["suites"][0]["pending"]
            test_cases_skipped = ts["results"][0]["suites"][0]["skipped"]

            test_set_data = {
                "file": test_set_file,
                "title": test_set_title,
                "duration": convert_milliseconds_to_time(test_set_duration),
                "suiteState": {
                    "passes": test_set_stats.get("passes", 0),
                    "failures": test_set_stats.get("failures", 0),
                    "pending": test_set_stats.get("pending", 0),
                    "skipped": test_set_stats.get("skipped", 0)
                },
                "tags": [],
                "TestCases": [],
                "passes": test_cases_passed,
                "failures": test_cases_failed,
                "pending": test_cases_pending,
                "skipped": test_cases_skipped
            }

            for tc in test_cases:
                title = tc["title"]
                duration = convert_milliseconds_to_time(tc["duration"])
                state = tc["state"]
                errmsg = tc["err"].get("message")
                errdiff = tc["err"].get("diff") 
                context = tc["context"]
                uuid = tc["uuid"]

                test_case_data = {
                    "title": title,
                    "duration": duration,
                    "state": state,
                    "err": {"message": errmsg, "diff": errdiff},
                    "context": context,
                    "uuid": uuid
                }
                
                test_set_data["TestCases"].append(test_case_data)
            
            final_json_enhanced.append({"TestSet": test_set_data})
        
        except Exception as e:
            logger.error(f"Error processing test set: {e}")

    return final_json_enhanced

def enhance_final_report(report):
    for test_set in report:
        try:
            # Add tags to test sets and test cases
            with open(test_set["TestSet"]["file"], 'r') as stream:
                data = yaml.safe_load(stream)
            
            test_set['TestSet']['tags'] = data['TestSuite']['Tags']

            for test_case in test_set['TestSet']['TestCases']:
                for tc in data["TestCases"]:
                    if tc["Title"] == test_case['title']:
                        if tc.get('Tags') is not None: 
                            test_case['tags'] = tc['Tags']

            [map_tc_uuid_with_tag(test_set, state) for state in ["passes", "failures", "pending", "skipped"]]

        except Exception as e:
            logger.error(f"Error enhancing final report: {e}")
    
    return report

def map_tc_uuid_with_tag(test_set, state = "passes"):

    test_cases = test_set["TestSet"]["TestCases"]
    state_chosen = test_set["TestSet"][state]

    # Replace tc uuid on test set state fields with jira issue (test case) id (tag) 
    for tc_uuid in state_chosen:
        for test_case in test_cases:
            if test_case["uuid"] == tc_uuid:
                for tag in test_case["tags"].split():
                    if tag.startswith(f"{JIRA_PROJECT_NAME}-"):
                        state_chosen[state_chosen.index(tc_uuid)] = tag
                        break  # Stop searching for tags
                break  # Stop searching for test cases
    
    state_chosen[:] = [item for item in state_chosen if item.startswith(f"{JIRA_PROJECT_NAME}-")]

def combine_objects_by_tag(objects):
    combined_objects = defaultdict(dict)
    unmerged_objects = []
    for obj in objects:
        tags = obj["TestSet"]["tags"].split()
        merged = False
        for tag in tags:
            if tag.startswith("FM-"):
                tag_key = tag[:tag.index('-') + 1]  # Get the FM- part as the key
                if tag_key not in combined_objects:
                    combined_objects[tag_key]["TestSet"] = obj["TestSet"].copy()
                    combined_objects[tag_key]["TestSet"]["duration"] = timedelta()  # Initialize duration as timedelta
                    combined_objects[tag_key]["TestSet"]["file"] = [obj["TestSet"]["file"]]  # Initialize as list
                    combined_objects[tag_key]["TestSet"]["title"] = [obj["TestSet"]["title"]]  # Initialize as list
                    combined_objects[tag_key]["tags"] = obj["TestSet"]["tags"].replace(tag, '').strip()
                else:
                    combined_objects[tag_key]["TestSet"]["file"].append(obj["TestSet"]["file"])
                    combined_objects[tag_key]["TestSet"]["title"].append(obj["TestSet"]["title"])
                    combined_objects[tag_key]["TestSet"]["suiteState"]["passes"] += obj["TestSet"]["suiteState"]["passes"]
                    combined_objects[tag_key]["TestSet"]["suiteState"]["failures"] += obj["TestSet"]["suiteState"]["failures"]
                    combined_objects[tag_key]["TestSet"]["suiteState"]["pending"] += obj["TestSet"]["suiteState"]["pending"]
                    combined_objects[tag_key]["TestSet"]["suiteState"]["skipped"] += obj["TestSet"]["suiteState"]["skipped"]
                    combined_objects[tag_key]["TestSet"]["tags"] += " " + obj["TestSet"]["tags"].replace(tag, '').strip()
                    combined_objects[tag_key]["TestSet"]["TestCases"].extend(obj["TestSet"]["TestCases"])
                    combined_objects[tag_key]["TestSet"]["passes"].extend(obj["TestSet"]["passes"])
                    combined_objects[tag_key]["TestSet"]["failures"].extend(obj["TestSet"]["failures"])
                    combined_objects[tag_key]["TestSet"]["pending"].extend(obj["TestSet"]["pending"])
                    combined_objects[tag_key]["TestSet"]["skipped"].extend(obj["TestSet"]["skipped"])
                # Sum the duration
                duration_parts = obj["TestSet"]["duration"].split(':')
                combined_objects[tag_key]["TestSet"]["duration"] += timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]), seconds=int(duration_parts[2]))
                merged = True
                break
        if not merged:
            unmerged_objects.append(obj)
    
    # Convert timedelta to string before returning
    for obj in combined_objects.values():
        obj["TestSet"]["duration"] = str(obj["TestSet"]["duration"])

    return list(combined_objects.values()) + unmerged_objects

def set_ts_info(test_set, jira_fields):
    overall_status = "❌ Failed" if test_set['suiteState']['failures'] != 0 else "✅ Success"

    passed_issues = f"✅\n\n{f'{chr(10)}'.join(test_set['passes'])}" if test_set['passes'] else ""
    failed_issues = f"❌\n\n{f'{chr(10)}'.join(test_set['failures'])}" if test_set['failures'] else ""
    pending_issues = f"🕖\n\n{f'{chr(10)}'.join(test_set['pending'])}" if test_set['pending'] else ""
    skipped_issues = f"➰\n\n{f'{chr(10)}'.join(test_set['skipped'])}" if test_set['skipped'] else ""

    ts_info = {
        f"{jira_fields['overall_info']['fld_id']}": f"""
        Overall Information:
        |Overall Status|Execution Time|UTC Execution Date|
        |{overall_status}| {test_set['duration']}|Day: {datetime.today().strftime('%d-%m-%Y')}\nHour: {datetime.today().strftime('%H:%M:%S')}|
        
        Test Cases Status:
        |✅ Passed|❌ Failed|🕖 Pending|➰Skipped|
        |{test_set['suiteState']['passes']}|{test_set['suiteState']['failures']}|{test_set['suiteState']['pending']}|{test_set['suiteState']['skipped']}|
        
        Total of {test_set['suiteState']['passes'] + 
                  test_set['suiteState']['failures'] + 
                  test_set['suiteState']['pending'] + 
                  test_set['suiteState']['skipped']} test cases were executed.
        From those, {len(test_set['passes']) + 
                       len(test_set['failures']) + 
                       len(test_set['pending']) + 
                       len(test_set['skipped'])} tests contained a tag matching the project issue id pattern.
        They are:
        
        {passed_issues}

        {failed_issues}

        {pending_issues}

        {skipped_issues}
        """
    }
    return ts_info

def set_tc_info(test_case, jira_fields):
    status_map = {
        "passed": ("✅ Success", f"{jira_fields['test_case_status']['options_id']['passed']}"),
        "failed": ("❌ Fail", f"{jira_fields['test_case_status']['options_id']['failed']}"),
        "skipped": ("➰ Skipped", f"{jira_fields['test_case_status']['options_id']['skipped']}"),
        "pending": ("🕖 Pending", f"{jira_fields['test_case_status']['options_id']['pending']}"),
        "unknown": ("🤷 unknown", f"{jira_fields['test_case_status']['options_id']['not_tested']}")
    }

    status = status_map.get(test_case["state"], ("🤷 unknown", f"{jira_fields['test_case_status']['options_id']['not_tested']}"))

    overall_info = f"""
    |Status|Execution Time|
    |{status[0]}|{test_case['duration']}|
    """

    delete_jira_issue_attachments(test_case['tags'])

    if test_case['err'].get('message') is not None:

        if test_case['err'].get('diff') is not None:
            overall_info += f"""
                h4.Error Details:
                {test_case['err'].get('message')}
                {test_case['err'].get('diff')}
            """
            add_failures_evidences_as_attachments(test_case['tags'], test_case['context'])
            
        else:
            overall_info += f"""
                h4.Error Details:
                {test_case['err'].get('message')}
            """
            add_failures_evidences_as_attachments(test_case['tags'], test_case['context'])

    tc_info = {
        f"{jira_fields['overall_info']['fld_id']}": overall_info,
        f"{jira_fields['test_case_status']['fld_id']}": {"id": status[1]}
    }

    return tc_info

def delete_jira_issue_attachments(tc_tags):
    try:
        for tag in tc_tags.split():
            if tag.startswith(f"{JIRA_PROJECT_NAME}-"):
                url = f"{JIRA_SERVER}/rest/api/3/issue/{tag}/attachments" 
                auth  = requests.auth.HTTPBasicAuth(JIRA_USERNAME,JIRA_PASSWORD)
                headers = { 'X-Atlassian-Token': 'nocheck' }
                requests.delete(url, auth=auth, headers=headers)
    except Exception as e:
            logger.error(f"Error deleting attachment: {e}")

def add_failures_evidences_as_attachments(tc_tags, tc_context):
    try:
        context_dict = json.loads(tc_context)

        for img in context_dict['value'][0]:
            if "(failed).png" in img:
                image_path = str(os.getcwd()) + "/cypress/results/screenshots" + str(img)
                break

        for tag in tc_tags.split():
            if tag.startswith(f"{JIRA_PROJECT_NAME}-"):
                url = f"{JIRA_SERVER}/rest/api/3/issue/{tag}/attachments" 
                auth  = requests.auth.HTTPBasicAuth(JIRA_USERNAME,JIRA_PASSWORD)
                headers = { 'X-Atlassian-Token': 'nocheck' }
                files = {'file': open(image_path, 'rb')} 
                requests.post(url, auth=auth, files=files, headers=headers) 

    except Exception as e:
            logger.error(f"Error adding attachment image: {e}")

def update_jira_issue(issue_id, info):
    logger_update = logging.getLogger()
    formatter = logging.Formatter('%(message)s')  # Format to show only the message

    # Set the formatter to the logger
    for handler in logger_update.handlers:
        handler.setFormatter(formatter)

    try:
        jira.issue(issue_id).update(fields=info)
        logger_update.info(f"\tUPDATED ISSUE: {issue_id}")
    except Exception as e:
        logger_update.error(f"\tERROR UPDATING ISSUE {issue_id}: {e}\n")

def main(jira_fields):
    report_files = Path(".").glob("**/*.json")
    reports = []

    for json_file in report_files:
        file = str(json_file)
        if file.startswith("cypress/report/.jsons"):
            loaded_json = load_json(file)
            if loaded_json:
                reports.append(loaded_json)

    final_report = merge_report_json_files(reports)
    enhanced_final_report = enhance_final_report(final_report)
    combined_final_report = combine_objects_by_tag(enhanced_final_report)

    ts_updates = []
    tc_updates = []

    for test_set in combined_final_report:
        ts_info = set_ts_info(test_set["TestSet"], jira_fields)
        for tag in test_set["TestSet"].get("tags", "").split():
            if f"{JIRA_PROJECT_NAME}-" in tag:
                issue_id = tag.split('-')[1]
                ts_updates.append((f"{JIRA_PROJECT_NAME}-{issue_id}", ts_info))

        for test_case in test_set["TestSet"]["TestCases"]:
            tc_info = set_tc_info(test_case, jira_fields)
            if test_case.get("tags") is not None:
                for tag in test_case["tags"].split():
                    if f"{JIRA_PROJECT_NAME}-" in tag:
                        issue_id = tag.split('-')[1]
                        tc_updates.append((f"{JIRA_PROJECT_NAME}-{issue_id}", tc_info))

    with ThreadPoolExecutor(max_workers=5) as executor:
        for issue_id, info in ts_updates + tc_updates:
            executor.submit(update_jira_issue, issue_id, info)

if __name__ == "__main__":
    load_jira_config_values()
    jira_config_values = load_jira_config_values()["jira"]

    JIRA_SERVER = jira_config_values.get("server")
    JIRA_USERNAME = jira_config_values.get("user")
    JIRA_PASSWORD = jira_config_values.get("password")
    JIRA_PROJECT_NAME = jira_config_values.get("project")

    # Initialize Jira client
    jira = JIRA(
        server=JIRA_SERVER,
        basic_auth=(JIRA_USERNAME, JIRA_PASSWORD)
    )

    main(jira_config_values["fields"])
