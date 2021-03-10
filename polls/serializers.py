from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from polls.models import Poll, Question, Answer, UserAnswer, UserPoll
from utils.constants import POLL_MINIMUM_DURATION_MINUTES, POLL_MINIMUM_DURATION_ERROR, START_DATE_CANNOT_BE_CHANGED, \
    START_DATE_EARLIER_THAN_NOW, CANNOT_CREATE_ANSWER
from utils.serializers import ChoicesField


class PollSerializer(serializers.ModelSerializer):
    def validate_start_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(START_DATE_EARLIER_THAN_NOW)

        if self.instance and value != self.instance.start_date:
            raise serializers.ValidationError(START_DATE_CANNOT_BE_CHANGED)

        return value

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date is not None and end_date is not None:
            if end_date - start_date < timezone.timedelta(minutes=POLL_MINIMUM_DURATION_MINUTES):
                raise serializers.ValidationError(POLL_MINIMUM_DURATION_ERROR)
        return data

    class Meta:
        model = Poll
        fields = '__all__'
        extra_kwargs = {'questions': {'required': False}}


class ActivePollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        exclude = ('users',)
        read_only_fields = ('id', 'name', 'description', 'start_date', 'end_date', 'questions')


class UserSerializer(serializers.ModelSerializer):
    polls = PollSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    polls = PollSerializer(read_only=True, many=True)
    type = ChoicesField(choices=Question.TYPE_CHOICES)

    class Meta:
        model = Question
        fields = ('id', 'answers', 'type', 'polls')


class AnswerSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Answer
        fields = '__all__'


class UserPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoll
        fields = '__all__'


class UserAnswerSerializer(serializers.ModelSerializer):
    def validate_question(self, value):
        if self.instance and value != self.instance.question:
            raise serializers.ValidationError('question cannot be changed')
        return value

    def validate_user_poll(self, value):
        if self.instance and value != self.instance.user_poll:
            raise serializers.ValidationError('user_poll cannot be changed')
        return value

    def validate(self, data):
        data = super().validate(data)
        question = data.get('question')
        user_poll = data.get('user_poll')
        answer = data.get('answer')
        request = self.context.get("request")

        if question and user_poll:
            if question not in user_poll.poll.questions.all():
                raise serializers.ValidationError('wrong question')

        if question and answer:
            if question.type != Question.TYPE_TEXT and \
                    answer not in question.answers.all().values_list('text', flat=True):
                raise serializers.ValidationError('wrong answer')

        if request.method == 'POST' and question and user_poll and question.type != Question.TYPE_MULTIPLE:
            if UserAnswer.objects.filter(question=question, user_poll=user_poll).exists():
                raise serializers.ValidationError('you cannot create multiple answers for this question')

        if user_poll:
            if request.user != user_poll.user and request.session.session_key != user_poll.session_key:
                raise serializers.ValidationError('you cannot answer for another user')

        return data

    class Meta:
        model = UserAnswer
        fields = '__all__'


class UserAnswerPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        exclude = ('questions', 'users')


class UserAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        depth = 1


class UserAnswerUserPollSerializer(serializers.ModelSerializer):
    poll = UserAnswerPollSerializer()

    class Meta:
        model = UserPoll
        exclude = ('session_key', 'user')


class UserAnswerInfoSerializer(serializers.ModelSerializer):
    user_poll = UserAnswerUserPollSerializer()
    question = UserAnswerQuestionSerializer()

    class Meta:
        model = UserAnswer
        fields = '__all__'