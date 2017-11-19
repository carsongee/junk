#!/usr/bin/env python
from os import environ as env, path, listdir
from subprocess import call

import click

SCRIPTS_DIRNAME = env.get('SCRIPTS_DIR', 'shell')
SCRIPTS_PATH = path.join(
    path.dirname(path.abspath(__file__)),
    SCRIPTS_DIRNAME
)


class ScriptsFinder(click.MultiCommand):
    commands = {}

    def find_commands(self):
        for file_path in listdir(SCRIPTS_PATH):
            command_base = path.splitext(path.basename(file_path))[0]
            self.commands[command_base] = file_path        

    def list_commands(self, ctx):
        self.find_commands()
        commands = list(self.commands)
        commands.sort()
        return commands

    def get_command(self, ctx, name):
        self.find_commands()
        matches = [x for x in self.commands.keys()
                   if x.startswith(name)]
        if not matches or len(matches) != 1:
            return None
        command = matches[0]

        @click.pass_context
        def callback(*args, **kwargs):
            call(
                path.join(SCRIPTS_PATH, self.commands[command]),
                shell=True,
                cwd=SCRIPTS_PATH,
            )

        return click.Command(command, callback=callback)


@click.command(cls=ScriptsFinder)
@click.pass_context
def cli(*args, **kwargs):
    pass


if __name__ == '__main__':
    cli()
