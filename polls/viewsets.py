from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from polls.models import Poll, Question, Answer, UserAnswer, UserPoll
from polls.serializers import PollSerializer, QuestionSerializer, AnswerSerializer, UserAnswerSerializer, \
    UserPollSerializer, ActivePollSerializer, UserPollEntrySerializer


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @action(detail=False, methods=['GET'], permission_classes=[permissions.AllowAny])
    def active(self, request):
        now = timezone.now()
        active_polls = self.get_queryset().filter(start_date__lte=now, end_date__gt=now)
        serializer = ActivePollSerializer(active_polls, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class UserPollViewSet(ModelViewSet):
    queryset = UserPoll.objects.all()
    serializer_class = UserPollSerializer

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def create_entry(self, request, *args, **kwargs):
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

    @action(detail=False, methods=['GET'], permission_classes=[permissions.AllowAny])
    def entries(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_polls = UserPoll.objects.filter(user=request.user)
        else:
            if not request.session.session_key:
                return Response([])
            user_polls = UserPoll.objects.filter(session_key=request.session.session_key)

        serializer = self.get_serializer(user_polls, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], permission_classes=[permissions.AllowAny])
    def entry(self, request, *args, **kwargs):
        entry_id = kwargs.get('pk')
        if request.user.is_authenticated:
            user_poll = UserPoll.objects.filter(user=request.user, pk=entry_id).first()
        else:
            if not request.session.session_key:
                return Response([])
            user_poll = UserPoll.objects.filter(session_key=request.session.session_key, pk=entry_id).first()

        if user_poll is not None:
            serializer = UserPollEntrySerializer(user_poll)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserAnswerViewSet(ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_answers = UserAnswer.objects.filter(user_poll__user=request.user)
        else:
            if not request.session.session_key:
                return Response(status.HTTP_403_FORBIDDEN)
            user_answers = UserAnswer.objects.filter(user_poll__session_key=request.session.session_key)

        serializer = self.get_serializer(user_answers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        entry_id = kwargs.get('pk')

        if request.user.is_authenticated:
            user_answer = UserAnswer.objects.filter(user_poll__user=request.user, pk=entry_id).first()
        else:
            if not request.session.session_key:
                return Response(status.HTTP_403_FORBIDDEN)
            user_answer = UserAnswer.objects \
                .filter(user_poll__session_key=request.session.session_key, pk=entry_id).first()

        if user_answer is not None:
            serializer = self.get_serializer(user_answer)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        entry_id = kwargs.get('pk')

        if request.user.is_authenticated:
            user_answer = UserAnswer.objects.filter(user_poll__user=request.user, pk=entry_id).first()
        else:
            if not request.session.session_key:
                return Response(status.HTTP_403_FORBIDDEN)
            user_answer = UserAnswer.objects \
                .filter(user_poll__session_key=request.session.session_key, pk=entry_id).first()

        if user_answer is not None:
            user_answer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
