from django.urls import path

from Posts.views import show_all_posts, add_post, post_detail, edit_post, delete, user_posts_and_comment, comment_edit, \
    delete_comment

app_name = 'posts'
urlpatterns = [
    path('', show_all_posts, name='posts_list'),
    path('add-post/', add_post, name='add_post'),
    path('post-detail/<int:post_id>/', post_detail, name='post_detail'),
    path('edit/<int:post_id>/', edit_post, name='edit'),
    path('delete-post/<int:post_id>/', delete, name='delete-post'),
    path('history-posts/', user_posts_and_comment, name='user_posts'),
    path('edit-comment/<int:comment_id>/', comment_edit, name='comment_edit'),
    path('delet-comment/<int:post_id>/<int:comment_id>/', delete_comment, name='delete_comment'),



]
