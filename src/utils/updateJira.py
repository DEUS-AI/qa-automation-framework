import json
import yaml
import logging
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from jira import JIRA
from jinja2 import Environment, FileSystemLoader


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
                "TestCases": []
            }

            for tc in test_cases:
                title = tc["title"]
                duration = convert_milliseconds_to_time(tc["duration"])
                state = tc["state"]
                errmsg = tc["err"].get("message")
                errdiff = tc["err"].get("diff") 

                test_case_data = {
                    "title": title,
                    "duration": duration,
                    "state": state,
                    "err": {"message": errmsg, "diff": errdiff}
                }
                
                test_set_data["TestCases"].append(test_case_data)
            
            final_json_enhanced.append({"TestSet": test_set_data})
        except Exception as e:
            logger.error(f"Error processing test set: {e}")

    return final_json_enhanced

def enhance_final_report(report):
    for test_set in report:
        try:
            with open(test_set["TestSet"]["file"], 'r') as stream:
                data = yaml.safe_load(stream)
            
            test_set['TestSet']['tags'] = data['TestSuite']['Tags']

            for test_case in test_set['TestSet']['TestCases']:
                for tc in data["TestCases"]:
                    if tc["Title"] == test_case['title']:
                        if tc.get('Tags') is not None: 
                            test_case['tags'] = tc['Tags'] 
        
        except Exception as e:
            logger.error(f"Error enhancing final report: {e}")
    
    return report

def set_ts_info(test_set, jira_fields):
    overall_status = "❌ Failed" if test_set['suiteState']['failures'] != 0 else "✅ Success"

    ts_info = {
        f"{jira_fields['overall_info']['fld_id']}": f"""
        Overall Information:
        |Overall Status|Execution Time|UTC Execution Date|
        |{overall_status}| {test_set['duration']}|Day: {datetime.today().strftime('%d-%m-%Y')}\nHour: {datetime.today().strftime('%H:%M:%S')}|
        
        Test Cases Status:
        |✅ Passed|❌ Failed|🕖 Pending|➰Skipped|
        |{test_set['suiteState']['passes']}|{test_set['suiteState']['failures']}|{test_set['suiteState']['pending']}|{test_set['suiteState']['skipped']}|
        """
    }
    return ts_info

def set_tc_info(test_case, jira_fields):
    status_map = {
        "passed": ("✅ Success", f"{jira_fields['test_case_status']['options_id']['passed']}"),
        "failed": ("❌ Fail", f"{jira_fields['test_case_status']['options_id']['failed']}"),
        "skipped": ("➰Skipped", f"{jira_fields['test_case_status']['options_id']['skipped']}"),
        "pending": ("🕖 Pending", f"{jira_fields['test_case_status']['options_id']['pending']}"),
        "unknown": ("🤷 unknown", f"{jira_fields['test_case_status']['options_id']['not_tested']}")
    }

    status = status_map.get(test_case["state"], ("🤷 unknown", "10313"))

    testcase_final_msg = f"""
    |Status|Execution Time|
    |{status[0]}|{test_case['duration']}|
    """

    error_msg = test_case['err'].get('message', '-')
    diff_msg = test_case['err'].get('diff', '')

    if error_msg != "-":
        testcase_final_msg += f"\nh4.Error Details:\n{error_msg}\n{diff_msg}"

    tc_info = {
        f"{jira_fields['overall_info']['fld_id']}": testcase_final_msg,
        f"{jira_fields['test_case_status']['fld_id']}": {"id": status[1]}
    }

    return tc_info

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

    ts_updates = []
    tc_updates = []

    for test_set in enhanced_final_report:
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
