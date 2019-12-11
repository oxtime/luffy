from rest_framework.serializers import ModelSerializer
from . import models


class TeachModelSerializers(ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['name',
                  'role_name',
                  'title',
                  'signature',
                  'image',
                  'brief', ]


class FreeCourseListSerializers(ModelSerializer):
    teacher = TeachModelSerializers()

    class Meta:
        model = models.Course
        fields = ['name',
                  'course_img',
                  'id',
                  'brief',
                  'level',
                  'pub_date',
                  'period',
                  'students',
                  'sections',
                  'pub_sections',
                  'price',
                  'teacher',
                  'section_list',
                  ]


class CategoriesSerializers(ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ('id', 'name')

class CourseSectionModelSerializer(ModelSerializer):
    class Meta:
        model = models.CourseSection
        fields = '__all__'



class ChapterListSerializers(ModelSerializer):
    coursesections = CourseSectionModelSerializer(many=True)
    class Meta:
        model = models.CourseChapter
        fields =(
            'id',
            'name',
            'chapter',
            'summary',
            'coursesections',
        )