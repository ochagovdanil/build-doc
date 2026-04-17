from django.urls import path
from .views import (
	UserFileUploadView, UserFileListView, AllFilesListView, 
	UserFileDeleteView, UserFileDeleteAllView, UserFileDownloadView, 
	UserFileDownloadAllView, ToggleFavoriteFileView, MyFavoriteFilesView,
	DownloadFavoriteFilesView, UserFileDetailView, FileCommentListCreateView,
	UserFileRenameView, ExportAllFilesExcelView, ExportMyFilesExcelView,
	ExportFavoriteFilesExcelView,  ProjectListCreateView, ProjectDetailView,
  AddFileToProjectView, RemoveFileFromProjectView, DownloadProjectFilesView,
	ExportProjectFilesExcelView,
)


urlpatterns = [
  path('upload/', UserFileUploadView.as_view(), name='userfile_upload'),
	path('list/', UserFileListView.as_view(), name='userfile_list'),
	path('all/', AllFilesListView.as_view(), name='all_files_list'),
	path('detail/<int:pk>/', UserFileDetailView.as_view(), name='userfile_detail'),
	path('comments/<int:file_id>/', FileCommentListCreateView.as_view(), name='file_comments'),
	path('rename/<int:pk>/', UserFileRenameView.as_view(), name='userfile_rename'),
	path('delete/<int:pk>/', UserFileDeleteView.as_view(), name='userfile_delete'),
  path('delete_all/', UserFileDeleteAllView.as_view(), name='userfile_delete_all'),
	path('download/<int:pk>/', UserFileDownloadView.as_view(), name='userfile_download'),
  path('download_all/', UserFileDownloadAllView.as_view(), name='userfile_download_all'),
	path('favorite/<int:pk>/', ToggleFavoriteFileView.as_view(), name='toggle_favorite_file'),
  path('my-favorites/', MyFavoriteFilesView.as_view(), name='my_favorite_files'),
	path('download_favorites/', DownloadFavoriteFilesView.as_view(), name='download_favorite_files'),
	path('export_excel/', ExportAllFilesExcelView.as_view(), name='export_all_files_excel'),
	path('export_my_excel/', ExportMyFilesExcelView.as_view(), name='export_my_files_excel'),
	path('export_favorites_excel/', ExportFavoriteFilesExcelView.as_view(), name='export_favorite_files_excel'),
	path('projects/', ProjectListCreateView.as_view(), name='project_list_create'),
	path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
	path('projects/<int:project_id>/add_file/', AddFileToProjectView.as_view(), name='add_file_to_project'),
	path('projects/<int:project_id>/remove_file/<int:file_id>/', RemoveFileFromProjectView.as_view(), name='remove_file_from_project'),
	path('projects/<int:project_id>/download_all/', DownloadProjectFilesView.as_view(), name='download_project_files'),
  path('projects/<int:project_id>/export_excel/', ExportProjectFilesExcelView.as_view(), name='export_project_files_excel'),
]
