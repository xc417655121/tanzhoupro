from django.shortcuts import render
from django.views import View
from course.models import CourseClass,CourseSort,Course,Teacher
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

class CourseList(View):
    def get(self, request):
        # 取出全部的数据
        course_class = CourseClass.objects.all()
        course_sort = CourseSort.objects.all()
        all_course = Course.objects.all()

        # 取出热门课程
        hot_course = all_course.order_by("-click_num")[:3]

        # 取出第一分类的id
        class_id = request.GET.get('class_id', "")
        if class_id:
            course_class = course_class.filter(id=int(class_id))
            course_sort = course_sort.filter(classes_id=int(class_id))
            all_course = all_course.filter(sort__classes_id=int(class_id))

        # 取出第二分类的id
        sort_id = request.GET.get('sort_id', "")
        if sort_id:

            all_course = all_course.filter(sort_id=int(sort_id))



        # 需要对是不是公开课的的价格做筛选
        price = request.GET.get('price', "")
        if price:
            if price == '0':
                all_course = all_course.filter(price=0)
            else:
                all_course = all_course.filter(price__gt=0)


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 比如对课程进行分页.
        # all_course需要分页的对象    数字 表示每页显示的数值
        p = Paginator(all_course, 4, request=request)

        all_course = p.page(page)



        return render(request, 'course_list.html', {"course_class": course_class,
                                                   "course_sort": course_sort,
                                                   "all_course": all_course,
                                                   "sort_id": sort_id,
                                                   "class_id": class_id,
                                                   "hot_course": hot_course,
                                                   "price": price
                                                   })




class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 每次点击进页面之后增加点击数
        course.click_num += 1
        course.save()

        teacher = Teacher.objects.get(teacher_course_id=course_id)
        if teacher:
            return render(request, 'course_detail.html', {"course": course,
                                                         "teacher": teacher})
        else:
            return render(request, 'course_detail.html', {"course": course})