from datetime import timedelta

from django.utils import timezone
from ninja import Router
from ninja.errors import HttpError

from app.models import User
from app.models.openapi import Agent, Ticket, generate_ticket
from app.schemas.openapi import TicketLoginIn, TicketOut
from app.schemas.token import Token
from infra.authentication import agent_auth, get_tokens_for_user

router = Router(tags=["三方免密登录"])


@router.get("/ticket", auth=agent_auth, response=TicketOut)
def get_ticket(request):
    """获取免密登录 ticket"""
    agent: Agent = request.auth
    ticket = generate_ticket()
    expired_at = timezone.now() + timedelta(minutes=3)

    Ticket.objects.create(ticket=ticket, agent=agent, expired_at=expired_at)
    return TicketOut(ticket=ticket)


@router.post("/ticket-login", auth=None)
def ticket_login(request, data: TicketLoginIn):
    """一次性ticket登录，登录后废弃"""
    try:
        ticket = Ticket.objects.filter(used=False, expired_at__gt=timezone.now()).get(ticket=data.ticket)
        authorizer = ticket.agent.authorizer
    except Ticket.DoesNotExist:
        raise HttpError(401, "invalid ticket")
    except User.DoesNotExist:
        raise HttpError(404, "未绑定授权账户")

    token = get_tokens_for_user(authorizer)
    ticket.used = True
    ticket.save()
    return Token(username=authorizer.username, nickname=authorizer.nickname, phone=authorizer.phone, token=token)


@router.post("/agent-login", auth=agent_auth)
def agent_login(request):
    """受信任的三方代理绑定的帐号登录"""
    authorizer = request.auth.authorizer
    token = get_tokens_for_user(authorizer)
    return Token(username=authorizer.username, nickname=authorizer.nickname, phone=authorizer.phone, token=token)
