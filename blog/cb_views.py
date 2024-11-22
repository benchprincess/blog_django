from audioop import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import CommentForm, BlogForm
from blog.models import Blog, Comment


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
    template_name = 'blog/blog_detail.html'

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, *args, **kwargs):
        comment_form = CommentForm(self.request.POST)

        if not comment_form.is_valid():
            self.object =self.get_object()
            context = self.get_context_data(object=self.object)
            context['comment_form'] = comment_form
            return self.render_to_response(context)

        if not self.request.user.is_authenticated:
            raise Http404

        comment = comment_form.save(commit=False)
        comment.blog_id = self.kwargs['pk']
        comment.author = self.request.user
        comment.save()

        return HttpResponseRedirect(reverse_lazy('blog:detail', kwargs={'pk': self.kwargs['pk']}))


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    form_class = BlogForm

    def form_valid(self, form):    # 폼이 유효할 때 호출
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '작성'
        context['btn_name'] = '생성'
        return context


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    form_class = BlogForm

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '수정'
        context['btn_name'] = '수정'
        return context


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Blog, pk=kwargs.get('blog_pk'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(blog=self.object).prefetch_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['blog'] = self.object
        return context

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    from_class = CommentForm

    def get(self, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        blog = self.get_blog()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.blog = blog
        self.object.save()
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'pk': blog.pk}))

    def get_blog(self):
        pk = self.kwargs['blog_pk']
        blog = get_object_or_404(Blog, pk=pk)
        return blog