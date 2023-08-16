# spark_jira_tools

[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)

spark_jira_tools is a Python library that implements jira task

## Installation

The code is packaged for PyPI, so that the installation consists in running:

## Usage

wrapper run jira task

## Sandbox

## Installation

```sh
!yes| pip uninstall spark-jira-tools
```

```sh
pip install spark-jira-tools --user --upgrade
```

## IMPORTS

```sh
from spark_jira_tools import show_dataframe_task
from spark_jira_tools import show_code_template
from spark_jira_tools import generated_task_jira
from spark_jira_tools import Jira

```

## Auth Jira

```sh
jira = Jira(username="jonathan.quiza",
            token="MTc1MzM5NzEyMTA0OqK/nSm+o45gAPayE0q6nkd25xIE",
            proxy=proxy)
```

## Show Dataframe Task

```sh
show_dataframe_task()

```


## Show Code Template
1. Analisis
2. Productivizacion - Scaffolder
3. Ingesta
4. Productivizacion - Scala
5. Ingesta Holding
6. Full Production in Channel	
```sh
code_list = show_code_template(process_name="Analisis")
```



## Generated Task

```sh
table_names = [
    {"table":"t_kctk_collateralization_atrb", "assigned":"", "folio":"", "id_table":""}
]
feature_pad = "PAD3-87929"
code_team_backlog = "5884174"

generated_task_jira(jira=jira, code_list=code_list, table_names=table_names,
                    feature_pad=feature_pad,code_team_backlog=code_team_backlog)
```

## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).

## New features v1.0

## BugFix

- choco install visualcpp-build-tools

## Reference

- Jonathan Quiza [github](https://github.com/jonaqp).
- Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
