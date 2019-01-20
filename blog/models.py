from django.db import models
from mdeditor.fields import MDTextField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import time

# Create your models here.


# 文章分类
class Group(models.Model):
    group = models.CharField("文章分类名",max_length=20)

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = '博客分类'

    def __str__(self):
        return '{}'.format(self.group)


class Tag (models.Model):
    name = models.CharField(verbose_name="标签名",max_length=10)

    class Meta:
        verbose_name = '标签云'
        verbose_name_plural = '标签云'

    def __str__(self):
        return '{}'.format(self.name)


# 日期归档
class Datetime_Manager(models.Manager):
    def get_data_time(self):
        get_data_time_list =[]
        data_time_list = self.values("time")# 取出的为一个queryset字典类{'time': datetime.date(2019, 1, 3)}
        for items in data_time_list:
            data_time = items["time"].strftime("%Y/%m")
            if data_time not in get_data_time_list:
                get_data_time_list.append(data_time)
        return get_data_time_list


#文章显示
class Articles(models.Model):
    title = models.CharField('文章标题',max_length=25)
    abstract = models.CharField('摘要', max_length=200, blank=True, null=True)
    content = MDTextField('文章内容')
    time = models.DateField('编写时间')
    views = models.PositiveIntegerField('浏览量',default=0)
    likes = models.PositiveIntegerField('点赞数',default=0)
    articlecomments = models.PositiveIntegerField('文章评论量',default=0)
    articleimage = ProcessedImageField(verbose_name='文章配图',default="brand_img_pc_jocomomola-de-sybilla.jpg",
                                       blank=True,upload_to="article",processors=[ResizeToFill(224, 168)],format='JPEG',options={'quality': 95})
    auther = models.CharField("作者",max_length=10,default="劉汝翹")
    goupname = models.ForeignKey(Group,on_delete=models.CASCADE,default="",verbose_name="分类")
    tags =models.ManyToManyField(Tag,verbose_name="标签集合",blank=True)
    objects = Datetime_Manager()


    class Meta:
        # abstract = True
        verbose_name="添加文章"
        verbose_name_plural = '添加文章'
        ordering = ['title']

    def __str__(self):
        return '{}'.format(self.title)



# 文章根评论
class Comment(models.Model):
    username = models.CharField('评论者',max_length=50)
    article = models.ForeignKey(Articles,on_delete=models.CASCADE,default="")
    comment = models.CharField('评论内容',max_length=300)
    userinfo = models.CharField('评论者的头像',max_length=100)
    onclick = models.PositiveIntegerField('点赞数',default=0)
    replaynum = models.PositiveIntegerField('回复量',default=0)
    time = models.CharField('评论时间',max_length=50)

    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural = '文章评论'

    def __str__(self):
        return "{}{}".format(self.username,self.comment[0:30])


# 点赞数
class Click(models.Model):
    username = models.CharField(max_length=20,default="")
    target = models.ManyToManyField(Comment,blank=True)




#子评论/二级评论
class SubComment(models.Model):
    subusername = models.CharField("回复者",max_length=20)
    returneduser = models.CharField("被回复者",max_length=20)
    subcomment = models.CharField('评论内容', max_length=300)
    subuserinfo = models.CharField("回复者头像",max_length=100)
    onclick = models.PositiveIntegerField('点赞数', default=0)
    time = models.CharField('回复时间', max_length=50)
    fathercomment = models.ForeignKey(Comment,on_delete=models.CASCADE,default="") # 二级评论归属

    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural = '文章评论'

    def __str__(self):
        return "{}{}".format(self.subusername, self.subcomment[0:30])


class SubClick(models.Model):
    subusername = models.CharField(max_length=20, default="")
    target = models.ManyToManyField(SubComment,blank=True)


#子评论/三级评论
class SecondComment(SubComment):
    second_father_comments = models.ForeignKey(SubComment,on_delete=models.CASCADE,default="",related_name="second_comment")
