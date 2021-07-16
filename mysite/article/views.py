from article.permissions import IsAdminUserOrReadOnly
from article.models import Article
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from article.models import Category
from article.serializers import CategorySerializer, CategoryDetailSerializer,ArticleSerializer
from article.models import Tag
from article.serializers import TagSerializer,ArticleDetailSerializer
from article.models import Avatar
# 这个 AvatarSerializer 最后来写
from article.serializers import AvatarSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author__username', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]