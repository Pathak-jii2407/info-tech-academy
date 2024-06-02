from django.db import models


class StudentStatus(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)
    name = models.CharField(max_length=40)
    phone_num = models.BigIntegerField()
    status = models.CharField(max_length=100)  
    status_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.status}"

class StudentInfo(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)
    username = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    phone_num = models.BigIntegerField()
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name



class TeacherAccount(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)
    username = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=100,unique=True)
    phone_num = models.BigIntegerField()
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=552, null=True)
    image = models.ImageField(upload_to='images/')  


    def __str__(self):
        return self.name




class Edit(models.Model):
    student_info = models.ForeignKey(to='StudentInfo', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/',null=True)  
    subject = models.CharField(max_length=40,null=True)

    def __str__(self):
        return self.student_info.name
    
    
    
    
    
    
