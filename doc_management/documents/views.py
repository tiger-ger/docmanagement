from django.shortcuts import render, redirect, get_object_or_404
from .forms import DocumentForm, DocumentSearchForm, PostForm, CommentForm
from .models import Document, Post
import chardet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import os
from django.conf import settings
import mimetypes
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


@login_required
def document_list(request):
    query = request.GET.get("q")
    if query:
        documents = Document.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by("-uploaded_at")
    else:
        documents = Document.objects.all().order_by("-uploaded_at")

    return render(request, "documents/document_list.html", {"documents": documents})


@login_required
def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.created_by = request.user
            document.save()

            # アップロードされたファイルを取得
            uploaded_file = request.FILES["file"]

            # ファイルのエンコーディングを確認して変換
            file_content = convert_file_encoding(uploaded_file)

            return redirect("document_list")
    else:
        form = DocumentForm()
    return render(request, "documents/upload_document.html", {"form": form})


# ファイルのエンコーディングをUTF-8に変換する関数
def convert_file_encoding(file):
    # ファイルの内容をバイナリモードで読み込む
    raw_data = file.read()

    # chardetライブラリでエンコーディングを推測
    result = chardet.detect(raw_data)
    file_encoding = result["encoding"]

    # 推測されたエンコーディングでデコードし、再エンコード
    if file_encoding:
        # UTF-8にエンコードしてから戻す
        file_content = (
            raw_data.decode(file_encoding, errors="replace")
            .encode("utf-8")
            .decode("utf-8")
        )
    else:
        # エンコーディングがわからなければ、デフォルトでUTF-8として扱う
        file_content = raw_data.decode("utf-8", errors="replace")

    return file_content


def my_view(request):
    return render(request, "documents/test.html")


@require_POST
def delete_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    document.delete()
    return redirect("document_list")


@login_required
def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect("document_list")
    else:
        form = DocumentForm(instance=document)
    return render(
        request, "documents/edit_document.html", {"form": form, "document": document}
    )


@login_required
def view_text_file(request, filename):
    # ファイルパスを取得
    file_path = os.path.join(settings.MEDIA_ROOT, "documents", filename)

    # ファイルが存在するか確認
    if not os.path.exists(file_path):
        return HttpResponse("ファイルが見つかりません", status=404)

    # ファイルを読み込んで内容を取得
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    # 内容をHttpResponseとして返す
    return HttpResponse(file_content, content_type="text/plain; charset=utf-8")


@login_required
def serve_document(request, path):
    # 先頭のスラッシュを削除
    if path.startswith("/"):
        path = path[1:]

    file_path = os.path.join(
        settings.MEDIA_ROOT, "documents", path
    )  # 'documents'ディレクトリを追加
    print(f"File path: {file_path}")  # デバッグ用にファイルパスを出力
    if not os.path.exists(file_path):
        return HttpResponse("File not found.", status=404)

    with open(file_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        file_encoding = result["encoding"]
        if file_encoding:
            file_content = raw_data.decode(file_encoding, errors="replace").encode(
                "utf-8"
            )
        else:
            file_content = raw_data.decode("utf-8", errors="replace").encode("utf-8")

    response = HttpResponse(file_content, content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = "inline; filename=%s" % smart_str(
        os.path.basename(file_path)
    )
    return response


@login_required
def view_document(request, path):
    # 先頭のスラッシュを削除
    if path.startswith("/"):
        path = path[1:]

    file_path = os.path.join(settings.MEDIA_ROOT, "documents", path)
    print(f"File path: {file_path}")  # デバッグ用にファイルパスを出力
    if not os.path.exists(file_path):
        return HttpResponse("File not found.", status=404)

    with open(file_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        file_encoding = result["encoding"]
        if file_encoding:
            file_content = raw_data.decode(file_encoding, errors="replace")
        else:
            file_content = raw_data.decode("utf-8", errors="replace")

    return render(
        request,
        "documents/view_document.html",
        {"file_content": file_content, "file_name": os.path.basename(file_path)},
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("document_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "registration/profile.html")


def main_menu(request):
    return render(request, "documents/main_menu.html")


def board_list(request):
    posts = Post.objects.all().order_by("-created_at")  # 新しい順に並べる
    return render(request, "board/board_list.html", {"posts": posts})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 投稿者をセット
            post.save()
            return redirect("board_list")  # 投稿後に掲示板へリダイレクト
    else:
        form = PostForm()
    return render(request, "board/post_create.html", {"form": form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by("created_at")  # 関連名で取得
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", post_id=post.id)

    return render(
        request,
        "board/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
        },
    )
