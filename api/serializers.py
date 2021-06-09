from rest_framework import serializers

from accounts.models import Apprentices
from journal.models import Lessons, Homeworks, Marks


class LessonSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField(read_only=True)
    teacher = serializers.StringRelatedField(read_only=True)
    homework = serializers.StringRelatedField(read_only=True)
    study_group = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lessons
        fields = ['id', 'active', 'date', 'order', 'subject', 'teacher', 'auditory', 'study_group', 'homework']


class UserProfileSerializer(serializers.ModelSerializer):
    study_group = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Apprentices
        fields = ['id', 'first_name', 'second_name', 'last_name', 'phone', 'email', 'civ_id', 'study_group']


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homeworks
        fields = ['id', 'text', 'required', 'deadline_time']


class MarksSerializer(serializers.ModelSerializer):
    lesson_subject = serializers.CharField(source='lesson.subject.title', read_only=True)

    class Meta:
        model = Marks
        fields = ['id', 'value', 'weight', 'rating_date', 'lesson_subject']
