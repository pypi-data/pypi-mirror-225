def show_result_task(jira_task_list, table_names):
    from prettytable import PrettyTable
    from spark_jira_tools.utils.color import get_color_b

    _table_names = list(jira_task_list[0].keys())
    for table in _table_names:
        assigned = [_["assigned"] for _ in table_names if _.get("table") == table][0]

        x = PrettyTable()
        x.field_names = ["Code", "Summary"]
        for col in jira_task_list[0][table]:
            _task = col.get("tasks")
            _summary = col.get("summary")
            x.add_row([f"{_task}", f"{_summary}"])
        print(x.get_string(title=f"{get_color_b(table)} - {get_color_b(assigned)}"))


def show_dataframe_task():
    from itables import init_notebook_mode, show
    from spark_jira_tools.utils import BASE_DIR
    import os
    import sys
    import pandas as pd
    import itables.options as opt

    opt.lengthMenu = [50]

    init_notebook_mode(all_interactive=True)
    is_windows = sys.platform.startswith('win')
    jira_tasks = os.path.join(BASE_DIR, "utils", "resource", "jira_task.csv")
    if is_windows:
        jira_tasks = jira_tasks.replace("\\", "/")
    df = pd.read_csv(jira_tasks)
    show(df)


def show_code_template(process_name=None):
    from spark_jira_tools.utils import BASE_DIR
    import os
    import sys
    import pandas as pd
    import numpy as np

    is_windows = sys.platform.startswith('win')
    jira_tasks = os.path.join(BASE_DIR, "utils", "resource", "jira_task.csv")
    if is_windows:
        jira_tasks = jira_tasks.replace("\\", "/")

    process_name = str(process_name).upper()
    df = pd.read_csv(jira_tasks)
    df = df.replace(np.nan, '', regex=True)
    df["PROCESO"] = df["PROCESO"].str.upper()

    data = df[df["PROCESO"] == process_name]
    data_unique = list(data["CODIGO_PLANTILLA"].unique())
    return data_unique


def generated_task_jira(jira=None,
                        code_list=None,
                        table_names=None,
                        feature_pad=None,
                        code_team_backlog=None):
    from itables import init_notebook_mode
    from spark_jira_tools.utils import BASE_DIR
    import os
    import sys
    import pandas as pd
    import numpy as np
    init_notebook_mode(all_interactive=False)

    is_windows = sys.platform.startswith('win')
    jira_tasks = os.path.join(BASE_DIR, "utils", "resource", "jira_task.csv")
    if is_windows:
        jira_tasks = jira_tasks.replace("\\", "/")

    jira_task_list = list()
    jira_task_dict = dict()

    for table in table_names:
        table_name = table.get("table")
        assigned = table.get("assigned", None)
        id_table = table.get("id_table", None)
        folio = table.get("folio", None)

        df = pd.read_csv(jira_tasks)
        df = df.replace(np.nan, '', regex=True)
        data = df[df["CODIGO_PLANTILLA"].isin(code_list)]
        data = data.replace("{fuente}", f"{table_name}", regex=True)

        for index, row in data.iterrows():
            code_template = row["CODIGO_PLANTILLA"]
            code_template = f"P-{code_template}"
            id_table_template = id_table or "ID-0000"
            folio_template = folio or "F-CA000000"
            summary_template = row["PLANTILLA"]
            description = None
            acceptance_criteria_template = row["CRITERIO_ACEPTACION"]
            labels = [folio_template, id_table_template, code_template]
            code_jira = jira.generated_issue(summary=summary_template,
                                             description=description,
                                             assignee=assigned,
                                             labels=labels,
                                             feature_pad=feature_pad,
                                             acceptance_criteria=acceptance_criteria_template,
                                             code_team_backlog=code_team_backlog)

            if table_name not in jira_task_dict.keys():
                jira_task_dict[table_name] = list()

            jira_task_details = dict()
            jira_task_details["assignee"] = assigned
            jira_task_details["tasks"] = code_jira.get("key")
            jira_task_details["summary"] = summary_template
            jira_task_dict[table_name].append(jira_task_details)
    jira_task_list.append(jira_task_dict)
    show_result_task(jira_task_list, table_names)
