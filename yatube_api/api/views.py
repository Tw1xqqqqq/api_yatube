from rest_framework import viewsets, status
from posts.models import Post, Group, Comment
from .serlializers import PostSerializer, GroupSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(
            {"detail": "Это не ваш пост."}, request, *args, **kwargs
        )

    def partial_update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return Response(
                {"detail": "Это не ваш пост."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return Response(
                {"detail": "Это не ваш пост."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        serializer.save(author=self.request.user, post_id=post_id)

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get("post_id"))

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(
            {"detail": "Это не ваш комментарий."}, request, *args, **kwargs
        )

    def partial_update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(
            {"detail": "Это не ваш комментарий."}, request, *args, **kwargs
        )

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(
            {"detail": "Это не ваш комментарий."}, request, *args, **kwargs
        )
