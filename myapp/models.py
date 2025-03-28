﻿from django.db import models
from datetime import datetime

# Create your models here.

class Users(models.Model):
	 #id = models.AutoField(primary_key=True)
	 name = models.CharField(max_length=32)
	 password = models.CharField(max_length=32)
	 Email = models.CharField(max_length=40)
	 phone = models.CharField(max_length=16)
	 addtime = models.DateTimeField(default=datetime.now)

class Animate_data(models.Model):
	#id = models.AutoField(primary_key=True)
	aname = models.CharField(max_length=32)
	ascore = models.CharField(max_length=32)
	arank = models.CharField(max_length=32)
	aimg = models.CharField(max_length=60)

#class Meta:
#    db_table = "myapp_users"  # 指定表名


class Article(models.Model):    #定义文章模型类
    title = models.CharField(max_length=100,verbose_name='文章标题')   #verbose_name是
    content = models.TextField(verbose_name='文章内容')
    publish_time = models.DateTimeField(default=datetime.now,verbose_name='发布时间')
    author = models.CharField(max_length=32,verbose_name='作者')
 
    class Meta:
        db_table = 'article_tb'     #定义表名
        verbose_name = '文章'       #后台显示
        verbose_name_plural = verbose_name    #后台显示的复数
 
 
 
 
class Comment(models.Model):    #定义评论模型
    article = models.ForeignKey(to=Article,on_delete=models.DO_NOTHING,verbose_name='评论文章')
    comment_content = models.TextField(verbose_name='评论内容')
    comment_author = models.CharField(max_length=32,verbose_name='评论者')
    comment_time = models.DateTimeField(default=datetime.now,verbose_name='评论时间')
    pre_comment = models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True,verbose_name='父评论id')  #父级评论，如果没有父级则为空NULL, "self"表示外键关联自己
 
    class Meta:
        db_table = 'comment_tb'
        verbose_name = '评论'
        verbose_name_plural = verbose_name