# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vmngclient',
 'vmngclient.api',
 'vmngclient.api.templates',
 'vmngclient.api.templates.device_template',
 'vmngclient.api.templates.models',
 'vmngclient.api.templates.payloads.aaa',
 'vmngclient.api.templates.payloads.cisco_system',
 'vmngclient.api.templates.payloads.cisco_vpn',
 'vmngclient.api.templates.payloads.cisco_vpn_interface_ethernet',
 'vmngclient.api.templates.payloads.tenant',
 'vmngclient.endpoints',
 'vmngclient.model',
 'vmngclient.tests',
 'vmngclient.tests.templates',
 'vmngclient.tests.templates.models',
 'vmngclient.utils']

package_data = \
{'': ['*'],
 'vmngclient.api.templates.payloads.aaa': ['feature/*'],
 'vmngclient.api.templates.payloads.cisco_system': ['feature/*'],
 'vmngclient.api.templates.payloads.cisco_vpn': ['feature/*'],
 'vmngclient.api.templates.payloads.cisco_vpn_interface_ethernet': ['feature/*'],
 'vmngclient.tests.templates': ['definitions/*', 'schemas/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'attrs>=21.4.0,<22.0.0',
 'cattrs>=22.2.0,<23.0.0',
 'ciscoconfparse>=1.6.40,<2.0.0',
 'clint>=0.5.1,<0.6.0',
 'flake8-quotes>=3.3.1,<4.0.0',
 'packaging>=23.0,<24.0',
 'parameterized>=0.8.1,<0.9.0',
 'pydantic>=1.10.7,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests-toolbelt>=1.0.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tenacity>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'vmngclient',
    'version': '0.13.0',
    'description': 'Universal vManage API',
    'long_description': '# vManage-client\n[![Python-Supported](https://img.shields.io/static/v1?label=Python&logo=Python&color=3776AB&message=3.8%20|%203.9%20|%203.10%20|%203.11)](https://www.python.org/)\n\nvManage client is a package for creating simple and parallel automatic requests via official vManageAPI. It is intended to serve as a multiple session handler (provider, provider as a tenant, tenant). The library is not dependent on environment which is being run in, you just need a connection to any vManage.\n\n## Installation\n```console\npip install vmngclient\n```\n\n## Session usage example\nOur session is an extension to `requests.Session` designed to make it easier to communicate via API calls with vManage. We provide ready to use authenticetion, you have to simply provide the vmanage url, username and password as as if you were doing it through a GUI. \n```python\nfrom vmngclient.session import create_vManageSession\n\nurl = "example.com"\nusername = "admin"\npassword = "password123"\nsession = create_vManageSession(url=url, username=username, password=password)\n\nsession.get("/dataservice/device")\n```\n\n## API usage examples\n\n<details>\n    <summary> <b>Get devices</b> <i>(click to expand)</i></summary>\n\n```python\ndevices = session.api.devices.get()\n```\n\n</details>\n\n<details>\n    <summary> <b>Admin Tech</b> <i>(click to expand)</i></summary>\n\n```Python\nadmin_tech_file = session.api.admin_tech.generate("172.16.255.11")\nsession.api.admin_tech.download(admin_tech_file)\nsession.api.admin_tech.delete(admin_tech_file)\n```\n</details>\n\n<details>\n    <summary> <b>Speed test</b> <i>(click to expand)</i></summary>\n\n```python\ndevices = session.api.devices.get()\nspeedtest = session.api.speedtest.speedtest(devices[0], devices[1])\n```\n\n</details>\n\n<details>\n    <summary> <b>Upgrade device</b> <i>(click to expand)</i></summary>\n\n```python\n# Prepare devices list\nvsmarts = session.api.devices.get().filter(personality=Personality.VSMART)\nimage = "viptela-20.7.2-x86_64.tar.gz"\n\n# Upload image\nsession.api.repository.upload_image(image)\n\n# Install software\n\ninstall_task = session.api.software.install(devices=vsmarts, image=image)\n\n# Check action status\ninstall_task.wait_for_completed()\n```\n\n</details>\n\n<details>\n    <summary> <b>Get alarms</b> <i>(click to expand)</i></summary>\nTo get all alarms:\n\n```python\nalarms = session.api.alarms.get()\n```\n\nTo get all not viewed alarms:\n\n```python\nnot_viewed_alarms = session.api.alarms.get().filter(viewed=False)\n```\n\nTo get all alarms from past `n` hours:\n\n```python\nn = 24\nalarms_from_n_hours = session.api.alarms.get(from_time=n)\n```\n\nTo get all critical alarms from past `n` hours:\n\n```python\nn = 48\ncritical_alarms = session.api.alarms.get(from_time=n).filter(severity=Severity.CRITICAL)\n```\n\n</details>\n\n<details>\n    <summary> <b>Users</b> <i>(click to expand)</i></summary>\n\n```python\n# Get all users\nsession.api.users.get()\n\n# Create user\nnew_user = User(userName="new_user", password="new_user", group=["netadmin"], description="new user")\nsession.api.users.create(new_user)\n\n# Update user data\nnew_user_update = UserUpdateRequest(userName="new_user", group=["netadmin", "netops"], locale="en_US", description="updated-new_user-description", resGroupName="global")\nsession.api.users.update(new_user_update)\n\n# Update user password\nsession.api.users.update_password("new_user", "n3W-P4s$w0rd")\n\n# Reset user\nsession.api.users.reset("new_user")\n\n# Delete user\nsession.api.users.delete("new_user")\n\n# Get current user authentication type and role\nsession.api.users.get_auth_type()\nsession.api.users.get_role()\n```\n\n</details>\n\n<details>\n    <summary> <b>User Groups</b> <i>(click to expand)</i></summary>\n\n```python\n# Get all user groups\nsession.api.user_groups.get()\n\n# Create user group\ngroup = UserGroup("new_user_group", [])\ngroup.enable_read({"Audit Log", "Alarms"})\ngroup.enable_read_and_write({"Device Inventory"})\nsession.api.user_groups.create(group)\n\n# Update user group\ngroup.disable({"Alarms"})\nsession.api.user_groups.update(group)\n\n# Delete user group\nsession.api.user_groups.delete(group.group_name)\n```\n\n</details>\n\n</details>\n\n<details>\n    <summary> <b>Sessions</b> <i>(click to expand)</i></summary>\n\n```python\n# Get all active sessions\nactive_sessions = session.api.sessions.get()\n\n# Invalidate sessions for given user\nnew_user_sessions = active_sessions.filter(raw_username="new_user")\nsession.api.sessions.invalidate(new_user_sessions)\n```\n\n</details>\n\n<details>\n    <summary> <b>Resource Groups</b> <i>(click to expand)</i></summary>\n\n```python\n# get resource groups\nsession.api.resource_groups.get()\n\n# create resource group\nnew_resource_group = ResourceGroup(\n    name="new_resource_group",\n    desc="Custom Resource Group #1",\n    siteIds=[]\n)\nsession.api.resource_groups.create(new_resource_group)\n\n# update resource group\nresource_group = session.api.resource_groups.get().filter(name="new_resource_group").single_or_default()\nupdated_resource_group = ResourceGroupUpdateRequest(\n    id=resource_group.id,\n    name=resource_group.name,\n    desc="Custom Resource Group #1 with updated description and site ids",\n    siteIds=[200]\n)\n\n# switch to resource group view\nsession.api.resource_groups.switch("new_resource_group")\n\n# delete resource group\nsession.api.resource_groups.delete(resource_group.id)\n```\n\n</details>\n\n<details>\n    <summary> <b>Tenant management</b> <i>(click to expand)</i></summary>\n\n```python\napi = session.api.tenant_management\n# create tenants\ntenants = [\n    Tenant(\n        name="tenant1",\n        orgName="CiscoDevNet",\n        subDomain="alpha.bravo.net",\n        desc="This is tenant for unit tests",\n        edgeConnectorEnable=True,\n        edgeConnectorSystemIp="172.16.255.81",\n        edgeConnectorTunnelInterfaceName="GigabitEthernet1",\n        wanEdgeForecast=1,\n    )\n]\ncreate_task = api.create(tenants)\ncreate_task.wait_for_completed()\n# list all tenants\ntenants_data = api.get_all()\n# pick tenant from list by name\ntenant = tenants_data.filter(name="tenant1").single_or_default()\n# get selected tenant id\ntenant_id = tenant.tenant_id\n# get vsession id of selected tenant\nvsessionid = api.vsession_id(tenant_id)\n# delete tenant by ids\ndelete_task = api.delete([tenant_id])\ndelete_task.wait_for_completed()\n# others\napi.get_hosting_capacity_on_vsmarts()\napi.get_statuses()\napi.get_vsmart_mapping()\n```\n</details>\n\n<details>\n    <summary> <b>Tenant migration</b> <i>(click to expand)</i></summary>\nPreparation:\n\n```python\nfrom vmngclient.api.tenant_migration_api import TenantMigrationAPI, st_to_mt\nfrom vmngclient.model.tenant import Tenant\nfrom vmngclient.session import create_vManageSession\n# create sessions to both systems\nst_session = create_vManageSession(**single_tenant_login)\nmt_session = create_vManageSession(**multi_tenant_provider_login)\n# create api and tenant objects\nst_api = TenantMigrationAPI(st_session)\nmt_api = TenantMigrationAPI(mt_session)\ntenant = Tenant.parse_obj({\n    "name": "single-tenant",\n    "desc": "Migrated from Single Tenant",\n    "orgName": "vIPtela Inc Regression",\n    "subDomain": "single-tenant.fruits.com",\n    "wanEdgeForecast": 99\n})\n```\n\nMethod below performs multi-step migration procedure according to [Migrate Single-Tenant Cisco SD-WAN Overlay to Multitenant Cisco SD-WAN Deployment](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/system-interface/vedge-20-x/systems-interfaces-book/sdwan-multitenancy.html#concept_sjj_jmm_z4b)\n\n```python\nfrom pathlib import Path\nst_to_mt(st_api, mt_api, workdir=Path.cwd(), tenant=tenant)\n```\n\nEach step of the procedure can be executed independently using api methods: `export_tenant`, `download`, `import_tenant`, `store_token`, `migrate_network`\n\n```python\ntenant_file = Path("~/tenant.tar.gz")\ntoken_file = Path("~/tenant-token.txt")\n# export\nexport_task = st_api.export_tenant(tenant=tenant)\nexport_result = export_task.wait_for_completed()\n# download\nst_api.download(tenant_file)\n# import\nimport_task = mt_api.import_tenant(tenant_file)\nimport_task.wait_for_completed()\n# get token\nmigration_id = import_task.import_info.migration_token_query_params.migration_id\nmt_api.store_token(migration_id, token_file)\n# migrate network\nmigrate_task = st_api.migrate_network(token_file)\nmigrate_task.wait_for_completed()\n```\n</details>\n\n### Note:\nTo remove `InsecureRequestWarning`, you can include in your scripts (warning is suppressed when `VMNGCLIENT_DEVEL` environment variable is set):\n```Python\nimport urllib3\nurllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)\n```\n\n## Catching Exceptions\n```python\ntry:\n\tsession.api.users.delete_user("XYZ")\nexcept vManageBadRequestError as error:\n\t# Process an error.\n\tlogger.error(error.info.details)\n\n# message = \'Delete users request failed\' \n# details = \'No user with name XYZ was found\' \n# code = \'USER0006\'\n```\n\n## [Supported API endpoints](ENDPOINTS.md)\n\n\n## [Contributing, bug reporting and feature requests](https://github.com/CiscoDevNet/vManage-client/blob/main/CONTRIBUTING.md)\n\n## Seeking support\n\nYou can contact us by submitting [issues](https://github.com/CiscoDevNet/vManage-client/issues), or directly via mail on vmngclient@cisco.com.\n',
    'author': 'kagorski',
    'author_email': 'kagorski@cisco.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CiscoDevNet/vManage-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
