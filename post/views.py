from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions import IsOwnerReadOnly

from . import error_messages
from .models import Comment, Post
from .serializers import CommentSerializer, PostDetailSerializer, PostSerializer


class PostCreateView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        ser_data = self.serializer_class(data=data)

        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(user=user)

    def update(self, request, *args, **kwargs):
        try:
            pk = kwargs.get("pk")
            post = Post.objects.get(pk=pk)

            if not request.user.is_superuser and post.user != request.user:
                raise PermissionError

            serializer = self.get_serializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
            return Response(
                {"error": error_messages.POST_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        except PermissionError:
            return Response(
                {"error": error_messages.INACCESSIBILITY_UPDATE_ERROR},
                status=status.HTTP_403_FORBIDDEN,
            )

        except Exception as e:
            return Response(
                {"error": error_messages.SERVER_ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     try:
    #         if user.is_superuser:
    #             return Post.objects.all()
    #         else:
    #             return Post.objects.filter(user=user)

    # except Exception as e:
    #     print(error_messages.SERVER_ERROR)
    #     return Post.objects.none()


class PostDestroyView(generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        try:
            pk = kwargs.get("pk")
            post = Post.objects.get(pk=pk)

            if not request.user.is_superuser and post.user != request.user:
                raise PermissionError

            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return Response(
                {"error": error_messages.POST_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        except PermissionError:
            return Response(
                {"error": error_messages.INACCESSIBILITY_DELETE_ERROR},
                status=status.HTTP_403_FORBIDDEN,
            )

        except Exception as e:
            return Response(
                {"error": error_messages.SERVER_ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get("pk")
        post = get_object_or_404(Post, pk=pk)
        return post


class ExploreView(APIView):

    serializer_class = PostSerializer

    def get(self, request):
        return Response(
            {"message": "this is Explore of posts"}, status=status.HTTP_200_OK
        )


class CommentCreateView(APIView):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_post(self, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post not found")

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        post = self.get_post(post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data)
        return Response(serializer.errors)


class CommentReplyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        parent_comment_id = self.kwargs.get("comment_id")
        parent_comment = Comment.objects.get(id=parent_comment_id)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                post=parent_comment.post,
                reply=parent_comment,
                is_reply=True,
            )
            return Response(serializer.data)
        return Response(serializer.errors)
