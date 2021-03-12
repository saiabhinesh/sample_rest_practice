from django.db import models

# Create your models here.

class Location(models.Model):
    area_name = models.CharField(max_length=255)

    def __str__(self):
        return self.area_name

class School(models.Model):
    Sname = models.CharField(max_length=255)
    Slocation  = models.ForeignKey(Location,models.SET_NULL,blank=True,null=True,)

    def __str__(self):
        return self.Sname

class Teacher(models.Model):
    tname = models.CharField(max_length=255)
    tsubject = models.CharField(max_length=255)
    teacher_school = models.ManyToManyField(School)

    def __str__(self):
        return self.tname

class Student(models.Model):
    name = models.CharField(max_length=255)
    student_school = models.ForeignKey(School,on_delete=models.CASCADE)
    student_teacher =  models.ManyToManyField(Teacher)
    student_address = models.ForeignKey(Location,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        db_table='StudentModel'

from django.db.models.signals import post_save,post_delete,pre_delete

def create_School(sender,instance,created,**kwargs):
    if created:
        schname=instance.area_name+"Govt High School"
        School.objects.create(Sname=schname,Slocation=instance)
        print('saving name',instance.area_name,'instance',instance)

post_save.connect(create_School,sender=Location)

# def update_School(sender,instance,instance1,created,**kwargs):
#     if created == False:
#         instance.school.save()
#         instance1.school.save()
#         print('profile updated')
#
# post_save.connect(update_location,sender=Location)

def delete_School(sender,instance,**kwargs):
    School.objects.filter(Slocation=instance.id).delete()
pre_delete.connect(delete_School,sender=Location)
#pre delete must be used as instance.id must be exist to delete child model

def update_School(sender,instance,created,**kwargs):
    if created == False:
        instance.school.save()
        instance1.school.save()
        print('profile updated')

post_save.connect(update_location,sender=Location)