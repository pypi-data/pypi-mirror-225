from ul_api_utils.access import PermissionRegistry

permissions = PermissionRegistry('example-debug-log', 111, 222)

SOME_PERMISSION = permissions.add('SOME', 1, 'Param pam Pam', 'test')
