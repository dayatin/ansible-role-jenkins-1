#!/usr/bin/python


from ansible.module_utils.basic import *  # NOQA
import json
from os.path import basename


def main():

    module = AnsibleModule(
        argument_spec=dict(
            credentials_type=dict(
                type='str',
                required=True,
                choice=['ssh_with_passphrase', 'password', 'text']),
            credentials_domain=dict(
                type='str',
                required=False,
                default='global'),
            scope=dict(
                type='str',
                required=True),
            id=dict(
                type='str',
                required=True),
            username=dict(
                type='str',
                required=False),
            password=dict(
                type='str',
                required=False),
            private_key_source_type=dict(
                type='str',
                required=False,
                choice=['direct_entry', 'file_on_master', 'user']),
            private_key_source_data=dict(
                type='str',
                required=False),
            private_key_passphrase=dict(
                type='str',
                required=False),
            description=dict(
                type='str',
                required=True),
            state=dict(
                type='str',
                required=False,
                default='present',
                choices=['present', 'absent']),
            text=dict(
                type='str',
                required=False),
            deployment_ssh_key=dict(
                type='str',
                required=False,
                default='/var/lib/jenkins/.ssh/id_rsa'),
            cli_path=dict(
                type='str',
                required=False,
                default='/var/lib/jenkins/jenkins-cli.jar'),
            groovy_scripts_path=dict(
                type='str',
                required=False,
                default='/var/lib/jenkins/groovy_scripts'),
            url=dict(
                type='str',
                required=False,
                default='http://localhost:8080')
        )
    )

    script = "%s/manage_jenkins_credentials.groovy" % (
        module.params['groovy_scripts_path'])

    rc, stdout, stderr = module.run_command(
        "java -jar %s -s '%s' -i '%s' groovy %s '%s'" %
        (module.params['cli_path'], module.params['url'],
         module.params['deployment_ssh_key'], script,
         json.dumps(module.params)))

    if (rc != 0):
        module.fail_json(msg=stderr)

    json_stdout = json.loads(stdout)
    module.exit_json(changed=bool(json_stdout['changed']),
                     output=json_stdout['output'])


if __name__ == '__main__':
    main()
