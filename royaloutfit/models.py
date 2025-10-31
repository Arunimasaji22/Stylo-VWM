from django.db import models

# Create your models here.


class login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=90)
    type=models.CharField(max_length=90)


class user_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    Gender=models.CharField(max_length=90)
    Place=models.CharField(max_length=100)
    Post=models.CharField(max_length=100)
    Pin=models.IntegerField()
    Phone=models.BigIntegerField()
    Email=models.CharField(max_length=100)
    Photo=models.FileField()


class complaint_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    complaint=models.TextField()
    Date=models.DateField(auto_now_add=True)
    reply=models.CharField(max_length=100)


class designers_table(models.Model):
    LOGIN=models.ForeignKey(login_table, on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    Gender=models.CharField(max_length=90)
    Place=models.CharField(max_length=100)
    Post=models.CharField(max_length=100)
    Pin=models.IntegerField()
    Phone=models.BigIntegerField()
    Email=models.CharField(max_length=100)
    Experience=models.CharField(max_length=100)
    Certificate=models.FileField()
    Photo=models.FileField()

class designs_tables(models.Model):
    dressname=models.CharField(max_length=100)
    platform=models.CharField(max_length=100)
    gendertype=models.CharField(max_length=100)
    dresstype=models.CharField(max_length=100)
    design=models.FileField()
    discription=models.TextField()
    season = models.CharField(max_length=100, null=True, blank=True)
    DESIGNER=models.ForeignKey(designers_table, on_delete=models.CASCADE)

class designs1_tables(models.Model):
    dressname=models.CharField(max_length=100)
    platform=models.CharField(max_length=100)
    design=models.FileField()

class rating_table(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    DESIGN = models.ForeignKey(designs_tables, on_delete=models.CASCADE)
    Reviews=models.TextField()
    rating=models.FloatField()
    Date=models.DateField()

class rating_table1(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    Reviews=models.CharField(max_length=200, null=True, blank=True)
    rating=models.FloatField()
    Date=models.DateField(auto_now_add=True)


class custom_desgin_table(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=100)
    DESIGNER = models.ForeignKey(designers_table, on_delete=models.CASCADE)
    design_details=models.TextField()


class chat(models.Model):
    fromid = models.ForeignKey(login_table, on_delete=models.CASCADE,related_name='fid')
    toid = models.ForeignKey(login_table, on_delete=models.CASCADE,related_name='tid')
    msg=models.TextField()
    date = models.DateField()


class MoreDesignTable(models.Model):
    DESIGN = models.ForeignKey(designs_tables, on_delete=models.CASCADE)
    design_more = models.FileField()


class WardrobeTable(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Dress = models.FileField()
    model_name = models.CharField(max_length=100, null=True, blank=True)
    dress_type = models.CharField(max_length=100, null=True, blank=True)
    gendertype=models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

class TestImageTable(models.Model):
    image = models.FileField(upload_to='test/', null=True, blank=True)
    USERID= models.ForeignKey(user_table, on_delete=models.CASCADE,null=True,blank=True)
    date= models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True) 


