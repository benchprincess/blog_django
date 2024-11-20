from django.db.models import Q
from django.shortcuts import redirect, reverse
from blog.forms import BlogForm
from blog.models import Blog
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')


    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )

    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    visits = int(request.COOKIES.get('visits', 0)) + 1
    request.session['count'] = request.session.get('count', 0) + 1

    context = {
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
    }
    return render(request, 'blog_list.html', context)

def blog_detail(request, pk):
    # blog = Blog.objects.get(pk=pk)
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog':blog}
    return render(request, 'blog/blog_detail.html', context)

@login_required()
def blog_create(request):

    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False) # 블로그 모델만 생성
        blog.author = request.user # author는 현재 로그인 된 유저
        blog.save()
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))
    context = {'form': form}
    return render(request, 'blog_create.html', context)

@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)

    form = BlogForm(request.POST or None, instance=blog) # instance로 기초데이터 세팅
    if form.is_valid():
        blog = form.save()
        return redirect(reverse('fb:detail', kwargs={'pk': blog.pk}))

    context = {
               'form' : form,
               }

    return render(request, 'blog_update.html', context)

@login_required()
@require_http_methods(['POST'])
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog_delete()

    return redirect(reverse('fb:list'))