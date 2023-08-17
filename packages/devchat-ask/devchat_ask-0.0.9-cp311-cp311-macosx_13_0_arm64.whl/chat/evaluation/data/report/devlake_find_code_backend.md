# Evaluation Report

- Name: report_20230713_233606
- Date: 2023-07-14 00:24:36
- Description: Using test set <DevLake>
- Subjects: ['StuffDc_with_OpenAIEmbeddings_ForDevlake', 'FindCode_with_OpenAIEmbeddings_ForDevlake']
- Evaluators: ['Correctness', 'Rating']


## Correctness

| Test Question |  StuffDc_with_OpenAIEmbeddings_ForDevlake | FindCode_with_OpenAIEmbeddings_ForDevlake |
| ------------- |  --  | --  |
| devlake-01: How is the lead time for changes calculated? |  False | False |
| devlake-02: Why can the lead time for changes metric be null sometimes? |  False | False |
| devlake-03: Can you provide a high-level description of DevLake's architecture? |  False | False |
| devlake-04: What data does the Azure DevOps plugin collect? |  False | False |
| devlake-05: What are the features of DevLake? |  False | False |
| devlake-06: What are the use cases of DevLake? |  False | False |
| devlake-07: How can I contribute to DevLake? |  False | False |
| devlake-08: Does DevLake's GitHub plugin support incremental sync? |  False | False |
| devlake-09: How can I create DevLake plugins in Python? |  False | False |
| devlake-10: How do I resolve the 'panic: invalid encKey' error? |  True | True |
| devlake-11: How does DevLake generate a pipeline based on a blueprint's setting? |  False | False |
| devlake-12: How does DevLake delete a project? |  False | False |
| devlake-13: How does DevLake generate the template user_account_mapping.csv file? |  False | True |
| devlake-14: How is the findAllAccounts function implemented? |  False | False |
| devlake-15: How is the h.store.findAllAccounts function implemented? |  False | False |
| devlake-16: How is the fromDomainLayer method of the account type implemented? |  False | False |
| devlake-17: Is the information collected from all branches from git? |  False | False |
| devlake-18: Does DevLake support PostgreSQL? |  False | False |
| devlake-19: Why is it that not all organisations in my Github are being shown? |  False | False |
| devlake-20: Is it possible to consume events/data from a stream instead of pulling an API? |  False | False |
| devlake-21: Is Devlake moving to Python based plugin rather than GoLang? |  False | False |
| devlake-22: I do not see anything on DORA dashboard, can anyone help with this? |  False | False |
| devlake-23: Does Apache Devlake supports deployment metrics from CloudBuild, Cloud Deploy and Anthos Config Management? |  False | False |
| devlake-24: I have set up DevLake only to collect the DORA metrics using helm but it is opening the DevLake UI without any authentication, i.e. no username and password. As I am entering the IP it is taking me to Devlake dashboard without asking any username and password. Is it the correct behaviour? |  False | False |
| devlake-25: Do you have plans to add user management in DevLake UI?  |  False | False |
| devlake-26: We have dozens of GitHub organizations and hundreds of repositories to track. At that scale it is difficult to manage using the Project interface and UI. Has anyone tried to use DevLake to work with anything close to that kind of scale? |  False | False |
| devlake-27: I want to define some commits as deployment jobs, such as commit messages starting with “merge..” or some specific account like admin. How can I do this? |  False | False |
| devlake-28: Does Lead Time for Changes support trunk-based development? |  False | False |
| devlake-29: How can I deploy DevLake with 5k+ repositories without constantly hitting the rate limit problem? |  False | False |
| devlake-30: When creating teams, if I have a hierarchy of parents and sub-teams, do I need to put the sub-team members in both parents and sub-teams, or just sub-teams? |  False | False |
| devlake-31: Is SSO supported for the DevLake UI and the dashboards? |  False | False |
| devlake-32: I entered a GitHub token but it showed INVALID TOKEN. What could be the causes? |  False | False |
| devlake-33: Can I filter out GitHub issues created by bots? |  False | False |
| devlake-34: How do I login to Grafana to access the dashboards |  False | False |
| devlake-35: Is it possible to modify a blueprint with an additional integration after its been created? |  False | False |
| devlake-36: When should I use advanced mode for a blueprint? |  False | False |
| devlake-37: How do I configure SonarQube? |  False | False |


## Rating

| Test Question |  StuffDc_with_OpenAIEmbeddings_ForDevlake | FindCode_with_OpenAIEmbeddings_ForDevlake |
| ------------- |  --  | --  |
| devlake-01: How is the lead time for changes calculated? |  7 | 7 |
| devlake-02: Why can the lead time for changes metric be null sometimes? |  4 | 4 |
| devlake-03: Can you provide a high-level description of DevLake's architecture? |  2 | 4 |
| devlake-04: What data does the Azure DevOps plugin collect? |  7 | 6 |
| devlake-05: What are the features of DevLake? |  4 | 6 |
| devlake-06: What are the use cases of DevLake? |  2 | 2 |
| devlake-07: How can I contribute to DevLake? |  7 | 7 |
| devlake-08: Does DevLake's GitHub plugin support incremental sync? |  2 | 2 |
| devlake-09: How can I create DevLake plugins in Python? |  7 | 6 |
| devlake-10: How do I resolve the 'panic: invalid encKey' error? |  8 | 8 |
| devlake-11: How does DevLake generate a pipeline based on a blueprint's setting? |  6 | 6 |
| devlake-12: How does DevLake delete a project? |  4 | 2 |
| devlake-13: How does DevLake generate the template user_account_mapping.csv file? |  0 | 9 |
| devlake-14: How is the findAllAccounts function implemented? |  10 | 9 |
| devlake-15: How is the h.store.findAllAccounts function implemented? |  0 | 0 |
| devlake-16: How is the fromDomainLayer method of the account type implemented? |  10 | 10 |
| devlake-17: Is the information collected from all branches from git? |  2 | 2 |
| devlake-18: Does DevLake support PostgreSQL? |  4 | 6 |
| devlake-19: Why is it that not all organisations in my Github are being shown? |  4 | 2 |
| devlake-20: Is it possible to consume events/data from a stream instead of pulling an API? |  2 | 2 |
| devlake-21: Is Devlake moving to Python based plugin rather than GoLang? |  4 | 6 |
| devlake-22: I do not see anything on DORA dashboard, can anyone help with this? |  4 | 2 |
| devlake-23: Does Apache Devlake supports deployment metrics from CloudBuild, Cloud Deploy and Anthos Config Management? |  2 | 2 |
| devlake-24: I have set up DevLake only to collect the DORA metrics using helm but it is opening the DevLake UI without any authentication, i.e. no username and password. As I am entering the IP it is taking me to Devlake dashboard without asking any username and password. Is it the correct behaviour? |  2 | 2 |
| devlake-25: Do you have plans to add user management in DevLake UI?  |  2 | 2 |
| devlake-26: We have dozens of GitHub organizations and hundreds of repositories to track. At that scale it is difficult to manage using the Project interface and UI. Has anyone tried to use DevLake to work with anything close to that kind of scale? |  2 | 2 |
| devlake-27: I want to define some commits as deployment jobs, such as commit messages starting with “merge..” or some specific account like admin. How can I do this? |  4 | 7 |
| devlake-28: Does Lead Time for Changes support trunk-based development? |  2 | 2 |
| devlake-29: How can I deploy DevLake with 5k+ repositories without constantly hitting the rate limit problem? |  4 | 4 |
| devlake-30: When creating teams, if I have a hierarchy of parents and sub-teams, do I need to put the sub-team members in both parents and sub-teams, or just sub-teams? |  0 | 2 |
| devlake-31: Is SSO supported for the DevLake UI and the dashboards? |  2 | 2 |
| devlake-32: I entered a GitHub token but it showed INVALID TOKEN. What could be the causes? |  2 | 2 |
| devlake-33: Can I filter out GitHub issues created by bots? |  2 | 2 |
| devlake-34: How do I login to Grafana to access the dashboards |  2 | 2 |
| devlake-35: Is it possible to modify a blueprint with an additional integration after its been created? |  9 | 9 |
| devlake-36: When should I use advanced mode for a blueprint? |  2 | 4 |
| devlake-37: How do I configure SonarQube? |  2 | 2 |

