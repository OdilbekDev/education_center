from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from datetime import datetime, date
import requests
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
# Create your views here.


class LessonView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Lesson.objects.all()
    serializer_class = LessonLoader
    
    def post(self, request):
        serializer = serializer(request.data)
        serializer.is_valid()
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Group.objects.all()
    serializer_class = GroupLoader

    def post(self, request):
        name = request.POST['name']
        level = request.POST['level']
        subject_id = request.POST['subject']
        subject = Subject.objects.get(id=subject_id)
        group = Group.objects.create(name=name, level=level, subject=subject)
        ser = self.serializer_class(group)

        return Response(ser.data)

    # def get_object(self, pk):
    #     queryset = self.get_queryset(id=pk)
    #     ser = self.serializer_class(queryset)

    #     return Response(ser.data)

    # def get_queryset(self, request):
    #     group_level = request.GET('group')
    #     group = Group.objects.filter(level=group_level)
    #     ser = self.serializer_class(group, many=True)

    #     return Response(ser.data)

    # def post(self, request):
    #     serializer = self.serializer_class(request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TeacherView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Teacher.objects.all()
    serializer_class = TeacherLoader


    def post(self, request):
        serializer = serializer(request.data)
        serializer.is_valid()
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request):
    #     name = request.POST['name']
    #     level = request.POST['level']
    #     subject_id = request.POST['subject']
    #     subject = Subject.objects.get(id=subject_id)
    #     group = Group.objects.create(name=name, level=level, subject=subject)
    #     ser = self.serializer_class(group)

    #     return Response(ser.data)



@api_view(['GET'])
def Filter_Group(request):
    group_level = request.GET['level']
    group = Group.objects.filter(level__icontains=group_level)
    ser = GroupLoader(group, many=True)

    return Response(ser.data)

@api_view(['GET'])
def Get_Group(request, pk):
    group = Group.objects.get(id=pk)
    ser = GroupLoader(group)
    return Response(ser.data)


@api_view(['GET'])
def Search_Group(request):
    name = request.GET['name']
    group = Group.objects.filter(name__icontains=name)
    ser = GroupLoader(group, many=True)

    return Response(ser.data)

@api_view(['GET'])
def Filter_Teacher(request):
    subject_id = request.GET['subject']
    subject = Subject.objects.get(id=subject_id)
    teacher = Teacher.objects.filter(subject=subject)
    ser = TeacherLoader(teacher, many=True)

    return Response(ser.data)


@api_view(['GET'])
def Filter_Money_Teacher(request):
    start = request.GET['start']
    end = request.GET['end']
    a = Teacher.objects.filter(money__gte=start, money__lte=end)
    ser = TeacherLoader(a, many=True)

    return Response(ser.data)


class PupilView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pupil.objects.all()
    serializer_class = PupilLoader


    def post(self, request):
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self, request, pk):
        a = self.queryset.get(id=pk)
        ser = self.serializer_class(a)
        return Response(ser.data)


class PupilDelView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pupil.objects.all()
    serializer_class = PupilLoader

    def delete(self, request, pk):
        a = self.queryset.get(id=pk)
        a.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def Payment_Pupil(request):
    
    money = request.POST.get('money')
    group_id = request.POST.get('group')
    group = Group.objects.get(id=int(group_id))
    pupil_id = request.POST.get('pupil')
    pupil = Pupil.objects.get(id=int(pupil_id))
    a = Payment_A.objects.create(
        money=money,
        group=group,
        pupil=pupil,
    )

    
    


    # day_payment = group.money / 12
    # days_came = date.today() - pupil.date_joined
    # days_came /= 2
    # pupil.debt = day_payment * days_came.days
    # pupil.save()
    # print(days_came)
    # print(type(pupil.date_joined))
    
    pupil.debt -= int(money)    
    pupil.save()
    id = Parents.objects.get(child=pupil)
    token = '5385500462:AAGoEg5kWLnCgMDS7XrqZB_XkbFZQG5OUHg'
    if pupil.debt > 0 or pupil.debt == 0:
        text = "Assalomu Aleykum" + id.name + "\nTo'lov qilindi!\nGuruh:" + group.name + 'Fan:\n' + group.subject.name + 'Sana:\n' + str(datetime.now()) + "O'quvchi\n" + pupil.name + "Qarzdorlik\n" + str(pupil.debt)
        url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id='
        requests.get(url + str(id.tg_id) + '&text=' + text)
    else:
        text = "Assalomu Aleykum" + id.name + "\nTo'lov qilindi!\nGuruh:" + group.name + '\nFan:' + group.subject.name + '\nSana:' + str(datetime.now()) + "\nO'quvchi:" + pupil.name + "\nBalans:" + str(pupil.debt * -1)
        url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id='
        requests.get(url + str(id.tg_id) + '&text=' + text)
    ser = Paymentone_Loader(a)
    return Response(ser.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def Davomat(request, pk):
    pupil = Pupil.objects.get(id=pk)
    lessons = Lesson.objects.filter(pupil=pupil, status=True)
    ser = LessonLoader(lessons, many=True)

    return Response(ser.data)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def Davomat_Bot(request):
    lesson = Lesson.objects.filter(status=False, time=datetime.today())
    print(datetime.today().weekday())
    for i1 in lesson:
        for i2 in i1.pupil.group.all():
            for i3 in i2.lesson_days.all():
                if i3.dayeng == datetime.today().weekday():
                    pupil = i1.pupil
                    id = Parents.objects.get(child=pupil)
                    token = '5385500462:AAGoEg5kWLnCgMDS7XrqZB_XkbFZQG5OUHg'
                    
                    text = "Assalomu Aleykum " + id.name + "\nFazrandingiz darsga kelmadi!" + "\nIsm Familiya" + pupil.name + "\nFan:" + str(i2.subject) + "\nIltimos bizning reception bilan bog'laning va darsga kelmaslik sababini yozib qoldiring" + "\nTelefon raqam: +998997821703\nTelegram:@django_programmer" 
                    url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id='
                    requests.get(url + str(id.tg_id) + '&text=' + text)
    return Response(status=200)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def Payment_Teacher(request):
    # money = request.POST.get('money')
    group_id = request.POST.get('group')
    group = Group.objects.get(id=group_id)
    teacher_id = request.POST.get('teacher')
    teacher = Teacher.objects.get(id=teacher_id)
    num_pupils = Pupil.objects.filter(group=group)
    money = group.money * len(num_pupils)
    teacher_money = (40 * money) / 100

    a = Payment_B.objects.create(
        money=teacher_money,
        group=group,
        teacher=teacher
    )

    ser = Paymenttwo_Loader(a)
    return Response(ser.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def Filter_Payment_Pupil(request):
    start = request.GET['start']
    end = request.GET['end']
    payment = Payment_A.objects.filter(date__gte=start, date__lte=end)
    ser = Paymentone_Loader(payment, many=True)
    return Response(ser.data)


@api_view(['GET'])
def Filter_Payment_Teacher(request):
    start = request.GET['start']
    end = request.GET['end']
    payment = Payment_B.objects.filter(date__gte=start, date__lte=end)
    ser = Paymenttwo_Loader(payment, many=True)
    return Response(ser.data)

