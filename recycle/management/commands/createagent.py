from django.core.management import BaseCommand

from recycle.models.agent import Agent, get_token_for_agent


class Command(BaseCommand):
    help = "create agent"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--username",
            help="代理用户名",
        )
        parser.add_argument(
            "-n",
            "--name",
            help="代理名称",
        )

    def handle(self, username: str, name: str, *args, **options):
        if not (username and name):
            self.stdout.write("请提供用户名和名称")
            return
        create_agent(username, name)
        self.stdout.write("OK!")


def create_agent(username: str, name: str):
    secret = get_token_for_agent(username)
    agent = Agent.objects.create(
        agent_id=username,
        name=name,
        secret=secret,
    )
    return agent
