from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()
class Blog(models.Model):

    CATEGORY_CHOICES = (
        ('free','자유'),
        ('travel','여행'),
        ('cat','고양이'),
        ('dog','강아지'),
    )
    category = models.CharField('카테고리', max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제가 불가능함 (유절르 삭제하려고 할떄 블로그가 있으면 삭제가 안됨)
    # models.SET_NULL => null값을 넣음 -> 유저 삭제 시 블로그의 author가 null이 됨, 이때 null = True의 옵션도 함꼐 설정 필요
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}]{self.title[:10]}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

# 제목
# 본문
# 작성자
# 작성일자
# 수정일자
# 카테고리


