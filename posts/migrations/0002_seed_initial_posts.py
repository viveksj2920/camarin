from django.db import migrations

def seed_posts(apps, schema_editor):
    Post = apps.get_model('posts', 'Post')
    Post.objects.bulk_create([
        Post(title='Post 1', body='This is the content of post 1.'),
        Post(title='Post 2', body='This is the content of post 2.'),
        Post(title='Post 3', body='This is the content of post 3.'),
        Post(title='Post 4', body='This is the content of post 4.'),
        Post(title='Post 5', body='This is the content of post 5.'),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_posts),
    ]
