from django.utils import timezone
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from polls.models import Poll, Question, Answer, UserAnswer, UserPoll
from polls.serializers import PollSerializer, QuestionSerializer, AnswerSerializer, UserAnswerSerializer, \
    UserPollSerializer, ActivePollSerializer, UserAnswerInfoSerializer


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @action(detail=False, methods=['GET'], permission_classes=[permissions.AllowAny])
    def active(self, request):
        now = timezone.now()
        active_polls = self.get_queryset().filter(start_date__lte=now, end_date__gt=now)
        serializer = ActivePollSerializer(active_polls, many=True)
        return Response(serializer.data)


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class UserPollViewSet(ModelViewSet):
    queryset = UserPoll.objects.all()
    serializer_class = UserPollSerializer

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def user_create(self, request, *args, **kwargs):
        data = request.data.copy()

        if request.user.is_authenticated:
            data.update({'user': request.user.pk})
            data.pop('session_key', None)
        else:
            if not request.session.session_key:
                request.session.create()
            data.update({'session_key': request.session.session_key})
            data.pop('user', None)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserAnswerViewSet(ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['GET'], permission_classes=[permissions.AllowAny])
    def answers(self, request):
        if request.user.is_authenticated:
            user_polls = UserPoll.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key
            user_polls = UserPoll.objects.filter(session_key=session_key)

        answers = UserAnswer.objects.filter(user_poll__in=user_polls)
        serializer = UserAnswerInfoSerializer(answers, many=True)
        return Response(serializer.data)
