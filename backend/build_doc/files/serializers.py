from rest_framework import serializers
from .models import UserFile, FavoriteFile, FileComment, Project, ProjectFile


class UserFileSerializer(serializers.ModelSerializer):
    owner_email = serializers.SerializerMethodField()
    owner_username = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    last_edited_email = serializers.SerializerMethodField()
    last_edited_username = serializers.SerializerMethodField()


    class Meta:
        model = UserFile
        fields = [
            'id', 'title', 'file', 'stage', 'uploaded_at', 'version',
            'owner_email', 'owner_username',
            'last_edited_email', 'last_edited_username', 'last_edited_at',
            'is_favorite'
        ]
        read_only_fields = [
            'id', 'uploaded_at', 'version',
            'owner_email', 'owner_username',
            'last_edited_email', 'last_edited_username', 'last_edited_at',
            'is_favorite'
        ]


    def get_owner_email(self, obj):
        return obj.owner.email if obj.owner else None
    
    def get_owner_username(self, obj):
        return obj.owner.username if obj.owner else None
    
    def get_last_edited_email(self, obj):
        return obj.last_edited_by.email if obj.last_edited_by else None

    def get_last_edited_username(self, obj):
        return obj.last_edited_by.username if obj.last_edited_by else None

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        
        if user.is_authenticated:
            return obj.favorited_by.filter(user=user).exists()
        
        return False


class FileCommentSerializer(serializers.ModelSerializer):
    author_email = serializers.SerializerMethodField()

    class Meta:
        model = FileComment
        fields = ['id', 'author_email', 'text', 'created_at']

    def get_author_email(self, obj):
        return obj.author.email if obj.author else None


class FavoriteFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteFile
        fields = ['id', 'file', 'added_at']


class ProjectFileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    file_id = serializers.PrimaryKeyRelatedField(
        queryset=UserFile.objects.all(), source='file', write_only=True
    )

    class Meta:
        model = ProjectFile
        fields = ['id', 'file', 'file_id', 'added_at']

    def get_file(self, obj):
        request = self.context.get('request')
        return UserFileSerializer(obj.file, context={'request': request}).data

class ProjectSerializer(serializers.ModelSerializer):
    project_files = serializers.SerializerMethodField()
    files_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'created_at', 'project_files', 'files_count']

    def get_project_files(self, obj):
        request = self.context.get('request')
        return ProjectFileSerializer(obj.project_files.all(), many=True, context={'request': request}).data

    def get_files_count(self, obj):
        return obj.project_files.count()
