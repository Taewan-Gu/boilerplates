from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import ArticleSerializer, CommentSerializer
from .models import Article, Comment

# Create your views here.


@api_view(["GET", "POST"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def article_CR(request):
    if request.method == "GET":
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data)
    else:
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def article_RUD(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == "GET":
        serializer = ArticleSerializer(article)
        data = {
            "article": serializer.data,
            "comments": CommentSerializer(article.comments.all(), many=True).data,
        }

        return Response(data)

    if not request.user.articles.filter(pk=article.pk).exists():
        return Response({"detail": "권한이 없습니다."})

    if request.method == "PUT":
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        article.delete()
        return Response({"id": pk})


@api_view(["GET", "POST"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_CR(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == "GET":
        comments = Comment.objects.filter(article=article)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    else:
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_D(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if not request.user.comments.filter(pk=comment_pk).exists():
        return Response({"detail": "권한이 없습니다."})

    comment.delete()
    return Response({"id": comment_pk})


@api_view(["GET"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_article_reverse(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    return Response(ArticleSerializer(comment.article).data)
