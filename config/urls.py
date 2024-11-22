from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include
from django.views import View
from django.views.generic import TemplateView, RedirectView

from blog import views
from blog import cb_views
from member import views as member_views
from config import settings
from django.conf.urls.static import static


class AboutView(TemplateView):
    template_name = 'about.html'

class TestView(View):
    def get(self, request):
        return render(request, 'test_get.html')

    def post(self, request):
        return render(request, 'test_post.html')

urlpatterns = [
    # FBV blog
    path('admin/', admin.site.urls),
    # path('blog/', views.blog_list, name='blog_list'),
    path('', include('blog.urls')),
    path('fb/', include('blog.fbv_urls')),

    # auth
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),

    # CBV blog
    path('cb/', cb_views.BlogListView.as_view(), name='cb_blog_list'),
    path('/cb/<int:id>/', cb_views.BlogDetailView.as_view(), name='cb_blog_detail'),
    path('/cb/create/', cb_views.BlogCreateView.as_view(), name='cb_blog_create.html'),
    path('cb/<int:pk>/update/', cb_views.BlogUpdateView.as_view(), name='cb_blog_update.html'),
    path('<int:pk>/delete/', cb_views.BlogDeleteView.as_view(), name='blog_delete'),
    # summernote 추가
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)