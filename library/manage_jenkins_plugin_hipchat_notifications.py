#!/usr/bin/python


from ansible.module_utils.basic import *  # NOQA
import json
from os.path import basename


def main():

    colors = ['YELLOW', 'GREEN', 'RED', 'PURPLE', 'GRAY', 'RANDOM']
    notification_types = ['STARTED', 'ABORTED', 'SUCCESS', 'FAILURE',
                          'NOT_BUILT', 'BACK_TO_NORMAL', 'UNSTABLE']

    module = AnsibleModule(
        argument_spec=dict(
            notify_enabled=dict(
                type='bool',
                required=False,
                default=True),
            text_format=dict(
                type='bool',
                required=False,
                default=True),
            notification_type=dict(
                type='str',
                required=True,
                choices=notification_types),
            color=dict(
                type='str',
                required=True,
                choices=colors),
            message_template=dict(
                type='str',
                required=True),
            state=dict(
                type='str',
                required=False,
                choices=['present', 'absent'],
                default='present'),
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

    script = "%s/manage_jenkins_plugin_hipchat_notifications.groovy" % (
        module.params['groovy_scripts_path'])

    rc, stdout, stderr = module.run_command(
        "java -jar %s -remoting -s '%s' -i '%s' groovy %s '%s'" %
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
