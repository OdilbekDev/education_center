from rest_framework import serializers
from .models import *

class GroupLoader(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class SubjectLoader(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TeacherLoader(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
class LessonLoader(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class PupilLoader(serializers.ModelSerializer):
    class Meta:
        model = Pupil
        fields = '__all__'

class DirectorLoader(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class Paymentone_Loader(serializers.ModelSerializer):
    class Meta:
        model = Payment_A
        fields = '__all__'

class Paymenttwo_Loader(serializers.ModelSerializer):
    class Meta:
        model = Payment_B
        fields = '__all__'

