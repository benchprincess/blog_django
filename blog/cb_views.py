from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.views import Blog
from blog.models import Blog


class BlogListView(ListView):
    queryset = Blog.objects.all()
    template_name = 'blog_detail.html'
    paginate_by = 10
    ordering = ('-created_at', )

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    # pk_url_kwarg = 'id'
    # """
    # 이 속성은 URL에서 데이터를 찾을때 사용할 키 이름을 바꿔주는 것
    # 보통 Django는 pk를 기준으로 데이터를 찾는데, 만약 URL 에서 id라는 이름을 쓰고 싶으면 이걸로 바꿔야함
    # URL이 blog/5/ 라면 pk를 쓰고, URL이 blog/<int:id>/라면 id를 씀
    # """


    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id__lte=50)
    # """
    # get_queryset 메서드는 어떤 데이터를 보여줄지 결정하는 것으로 데이터전체에서 필터링하는 느낌
    # 블로그 글이 100개 있는데, id=50이하인 글만 보여주고 싶을 때 사용
    # queryset = super().get_queryset()        # 전체 데이터 가져오기
    # return queryset.filter(id__lte=50)       # 그 중에서 id가 50 이하인 것만 골라내기
    # 결과는 50번째 글까지만 보여줌
    # """
    #
    # def get_object(self, queryset=None):
    #     object = super().get_object()
    #     object = self.model.objects.get(pk=self.kwargs.get('pk'))
    #
    #     return object
    #
    # """
    # get_object 메서드는 URL에서 특정 글(데이터) 하나를 가져오는 방법을 바꾸는것
    # 지금은 별로 바뀌는게 없지만, 나중에 더 복잡한 조건(ex.이 글을 작성한 사람만 볼 수 있다) 같은 걸 추가가능
    # object = super().get_object()        # 기본 방식으로 글 하나 가져오기
    # object = self.model.objects.get(pk=self.kwargs.get('pk'))           # 다시 글 찾기
    # self.model.objects.get()은 pk = 5인 데이터를 데이터베이스에서 직접 가져오는 방법
    # self.kwargs.get('pk') 는 URL에서 pk값을 가져옴
    # 결과는 그냥 글 하나 가져오는 기본 방식이랑 거의 똑같지만, 나중에 수정할 준비를 해둔 것
    # """
    #
    # def get_context_data(selfself, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['text'] = 'CBV'
    #     return context
    #
    # """
    # 테믈릿에 추가로 데이터를 전달하는 것으로 템플릿에서 사용할 수 있는 변수를 더 만드는 것
    # 템플릿에 CBV라는 텍스트를 표시하고 싶을때 쓸 수 있음
    # 결과는 템플릿에서 {{ test }} 를 쓰면 CBV라는 값이 나옴
    # context = super().get_context_data(**kwargs)        # 기본 데이터 가져오기
    # context['test'] = 'CBV'                              # 추가로 test라는 이름으로 'CBV' 넣기
    # """

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog_create.html'
    fields = ('title', 'content')

    def form_valid(self, form):    # 폼이 유효할 때 호출
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail', kwargs={'pk':self.object.pk})


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    fields = ('category', 'title', 'content')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('blog:list')