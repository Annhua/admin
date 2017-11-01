from qi.server import V1

from app01 import models


class DepartmentConding(V1.ModelNb):
    list_display=['title']


V1.site.register(models.Department,DepartmentConding)



class UserInfoConding(V1.ModelNb):
    list_display=['name','phone','depart',]


V1.site.register(models.UserInfo,UserInfoConding)


class CourseConding(V1.ModelNb):
    list_display=['name',]


V1.site.register(models.Course,CourseConding)



class SchoolConding(V1.ModelNb):
    list_display=['title',]


V1.site.register(models.School,SchoolConding)



class ClassListConding(V1.ModelNb):
    list_display=['school','course','semester','price','start_date','graduate_date','memo','tutor','teachers']


V1.site.register(models.ClassList,ClassListConding)



class CustomerConding(V1.ModelNb):
    list_display=['qq','name','gender','education','graduation_school','major','experience',
                  'work_status','company','salary','source','referral_from','course','status','consultant',
                  'date','last_consult_date']


V1.site.register(models.Customer,CustomerConding)




class ConsultRecordConding(V1.ModelNb):
    list_display=['customer','consultant','date','note',]


V1.site.register(models.ConsultRecord,ConsultRecordConding)



class PaymentRecordConding(V1.ModelNb):
    list_display=['customer','class_list','pay_type','paid_fee','turnover','quote','note','date','consultant']


V1.site.register(models.PaymentRecord,PaymentRecordConding)



class StudentConding(V1.ModelNb):
    list_display=['username','password','emergency_contract','class_list','location',]


V1.site.register(models.Student,StudentConding)


class CourseRecordConding(V1.ModelNb):
    list_display=['course','day_num','teacher','date','course_title',]


V1.site.register(models.CourseRecord,CourseRecordConding)


class StudyRecordConding(V1.ModelNb):
    list_display=['course_record','student','record','score','homework_note',]


V1.site.register(models.StudyRecord,StudyRecordConding)