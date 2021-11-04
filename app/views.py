"""
views:Djangoの司令塔の役割を果たす
ルーティング(アプリケーション内urls.py)から受け取った情報をもとに，
forms.pyに処理を渡す，models.pyにデータベース操作を依頼する，
templatesにhtmlの生成を依頼する　などを行う
"""

from django.shortcuts import render,redirect
from django.views.generic import View
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
#↑login必須
#redirect:特定ビューへのアクセスを別ビューにリダイレクト
#例．ユーザがAページに訪れたら，そのままBページへ転送する

class IndexView(View):
    def get(self,request,*args,**kwargs):#def get viewがコールされると最初呼び出される
        post_data=Post.objects.order_by('-id')#order_by()並び替え'-id'で降順に並び替え
        return render(request,'app/index.html',{
            'post_data':post_data
        })

class PostDetailView(View):
    def get(self,request,*args,**kwargs):
        post_data=Post.objects.get(id=self.kwargs['pk'])#self.kwargsでid指定
        return render(request,'app/post_detail.html',{
            'post_data':post_data
        })

class CreatePostView(View):
    def get(self,request,*args,**kwargs):
        form=PostForm(request.POST or None)
        return render(request,'app/post_form.html', {
            'form':form
        })
    
    def post(self,request,*args,**kwargs):
        form=PostForm(request.POST or None)

        if form.is_valid():
            post_data=Post()
            post_data.author=request.user
            post_data.title=form.cleaned_data['title']
            post_data.content=form.cleaned_data['content']
            if request.FILES:####画像アップロード機能
                post_data.image=request.FILES.get('image')####
            post_data.save()
            return redirect('post_detail',post_data.id)

        return render(request,'app/post_form.html',{
            'form': form
        })



class PostEditView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        post_data=Post.objects.get(id=self.kwargs['pk'])
        form=PostForm(
            request.POST or None,
            initial={
                'title':post_data.title,
                'content':post_data.content,
                'image':post_data.image,####
            }
        )

        return render(request,'app/post_form.html',{
            'form': form
        })

    def post(self,request,*args,**kwargs):
        form=PostForm(request.POST or None)

        if form.is_valid():
            post_data=Post.objects.get(id=self.kwargs['pk'])
            post_data.title=form.cleaned_data['title']
            post_data.content=form.cleaned_data['content']
            if request.FILES:####
                post_data.image=request.FILES.get('image')####
            post_data.save()
            return redirect('post_detail',self.kwargs['pk'])

        return render(request,'app/post_form.html',{
            'form': form
        })

class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        post_data=Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html',{
            'post_data':post_data
        })
    
    def post(self,request,*args,**kwargs):
        post_data=Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')