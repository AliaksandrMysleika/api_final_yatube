from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import filters
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import status

from .serializers import (
    GroupSerializer, PostSerializer, CommentSerializer, FollowSerializer
)
from posts.models import Post, Comment, Group


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid() and post.author == request.user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid() and post.author == request.user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if post.author == request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comments = Comment.objects.filter(post=post).all()
        return comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=Post.objects.get(id=self.kwargs['post_id'])
        )

    def retrieve(self, request, post_id, pk):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment = Comment.objects.filter(post=post).get(id=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, pk, post_id):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment = Comment.objects.filter(post=post).get(id=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid() and comment.author == request.user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk, post_id):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment = Comment.objects.filter(post=post).get(id=pk)
        serializer = CommentSerializer(
            comment, data=request.data, partial=True
        )
        if serializer.is_valid() and comment.author == request.user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk, post_id):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment = Comment.objects.filter(post=post).get(id=pk)
        if comment.author == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            if serializer.validated_data['following'] == self.request.user:
                raise serializers.ValidationError(
                    'Нельзя подписываться на себя!'
                )
        serializer.save(user=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
