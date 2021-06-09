import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Apprentices
from accounts.services import get_profile_from_user
from api.serializers import LessonSerializer, UserProfileSerializer, HomeworkSerializer, MarksSerializer
from journal.models import Lessons, Homeworks, Marks


class UserAuthView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        print(request)

        content = {}

        try:
            user = authenticate(username=request.data['username'], password=request.data['password'])
        except KeyError:
            content = {
                'status': False,
                'message': 'Не все данные предоставлены!',
            }
            return Response(content)
        else:
            username = request.data['username']

            if user is not None:
                profile = get_profile_from_user(user.id)

                token = Token.objects.get_or_create(user_id=user.id)

                content = {
                    'status': True,
                    'user_id': profile.id,
                    'first_name': profile.first_name,
                    'last_name': profile.second_name,
                    'middle_name': profile.last_name,
                    'phone': profile.phone,
                    'email': profile.email,
                    'study_group': profile.study_group_id,
                    'token': token[0].key
                }
            else:
                content['status'] = False
                if User.objects.filter(username=username).count() > 0:
                    content['error'] = 'Неправильный пароль!'
                else:
                    content['error'] = 'Аккаунт не найден!'

        return Response(content)


class Test(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class WeekLessonsView(APIView):
    def get(self, request):
        student_group_id = get_profile_from_user(request.user.id).study_group_id
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(6)
        this_week_lessons = Lessons.objects.filter(date__range=[start_week, end_week],
                                                   study_group_id=student_group_id)

        json_data = LessonSerializer(this_week_lessons, many=True)

        return Response(json_data.data)


class ProfilesView(APIView):
    def get(self, request, **kwargs):
        profile = Apprentices.objects.get(id=kwargs.get('profile_id'))
        json_data = UserProfileSerializer(profile, many=False)

        return Response(json_data.data)


class HomeworkView(APIView):
    def get(self, request, **kwargs):
        homework = Homeworks.objects.get(id=kwargs.get('homework_id'))
        json_data = HomeworkSerializer(homework, many=False)

        return Response(json_data.data)


class FutureHomeworks(APIView):
    def get(self, request):
        student_group_id = get_profile_from_user(request.user.id).study_group_id

        homework = Homeworks.objects.filter(target_group=student_group_id, deadline_time__gte=datetime.datetime.now())
        if homework:
            json_data = HomeworkSerializer(homework, many=True)
        else:
            return Response(None)

        return Response(json_data.data)


class MarksView(APIView):
    def get(self, request):
        marks = Marks.objects.filter(holder=get_profile_from_user(request.user.id))

        # json_data = []
        # for _ in marks:
        #     json_data.append({
        #         'id': _.id,
        #         'value': _.value,
        #         'weight': _.weight,
        #         'date': _.rating_date,
        #         'subject': _.lesson.subject.title,
        #     })

        json_data = MarksSerializer(marks, many=True)

        return Response(json_data.data)
