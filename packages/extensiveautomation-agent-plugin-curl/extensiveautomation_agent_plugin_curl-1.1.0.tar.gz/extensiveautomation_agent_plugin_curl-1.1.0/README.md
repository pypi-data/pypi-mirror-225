# CURL plugin for ExtensiveAutomation Agent

Installing from pypi
--------------------

1. Run the following command

    ```bash
    pip install extensiveautomation_agent_plugin_curl
    ```

2. (Optional) only on Linux, you must also install the `curl` command

    ```bash
    yum install curl
    ```
    
3. Now you can deploy this plugin with the option `--web`


    ```bash
    extensiveautomation_agent  --remote=[your_ea_ip] --name=curl01 --web
    ```
