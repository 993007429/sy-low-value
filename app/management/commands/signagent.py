from django.core.management import BaseCommand

from infra.authentication import get_tokens_for_agent


class Command(BaseCommand):
    help = "为受信任的三方公司生成token，用于免密登录"

    def add_arguments(self, parser):
        parser.add_argument(
            "agent_id",
            help="三方公司 agent_id",
        )

    def handle(self, agent_id: str, *args, **options):
        token = get_tokens_for_agent(agent_id)
        self.stdout.write(token)
