# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Widget'
        db.create_table(u'website_widget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('widget_format', self.gf('django.db.models.fields.related.ForeignKey')(related_name='widget', to=orm['website.WidgetFormat'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='widget', null=True, to=orm['my_user.CustomUser'])),
        ))
        db.send_create_signal(u'website', ['Widget'])

        # Adding M2M table for field clips on 'Widget'
        m2m_table_name = db.shorten_name(u'website_widget_clips')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('widget', models.ForeignKey(orm[u'website.widget'], null=False)),
            ('video', models.ForeignKey(orm[u'audience.video'], null=False))
        ))
        db.create_unique(m2m_table_name, ['widget_id', 'video_id'])

        # Adding M2M table for field sections on 'Widget'
        m2m_table_name = db.shorten_name(u'website_widget_sections')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('widget', models.ForeignKey(orm[u'website.widget'], null=False)),
            ('section', models.ForeignKey(orm[u'website.section'], null=False))
        ))
        db.create_unique(m2m_table_name, ['widget_id', 'section_id'])


    def backwards(self, orm):
        # Deleting model 'Widget'
        db.delete_table(u'website_widget')

        # Removing M2M table for field clips on 'Widget'
        db.delete_table(db.shorten_name(u'website_widget_clips'))

        # Removing M2M table for field sections on 'Widget'
        db.delete_table(db.shorten_name(u'website_widget_sections'))


    models = {
        u'audience.collection': {
            'Meta': {'object_name': 'Collection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['audience.Topic']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collection'", 'to': u"orm['my_user.CustomUser']"})
        },
        u'audience.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'audience.topic': {
            'Meta': {'object_name': 'Topic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'audience.video': {
            'Meta': {'object_name': 'Video'},
            'blacklisted_country': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['audience.Country']", 'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['audience.Collection']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_url': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'my_user.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'website.category': {
            'Meta': {'object_name': 'Category'},
            'category_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'created_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'website.section': {
            'Meta': {'object_name': 'Section'},
            'allowed_clips': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['audience.Video']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': u"orm['website.Website']"})
        },
        u'website.website': {
            'Meta': {'object_name': 'Website'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_views_per_day': ('django.db.models.fields.IntegerField', [], {}),
            'page_views_per_month': ('django.db.models.fields.IntegerField', [], {}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unique_users_per_day': ('django.db.models.fields.IntegerField', [], {}),
            'unique_users_per_month': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'websites'", 'null': 'True', 'to': u"orm['my_user.CustomUser']"}),
            'vertical_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'websites'", 'to': u"orm['website.Category']"})
        },
        u'website.widget': {
            'Meta': {'object_name': 'Widget'},
            'clips': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'widget'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['audience.Video']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sections': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'widget'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['website.Section']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'widget'", 'null': 'True', 'to': u"orm['my_user.CustomUser']"}),
            'widget_format': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'widget'", 'to': u"orm['website.WidgetFormat']"})
        },
        u'website.widgetformat': {
            'Meta': {'object_name': 'WidgetFormat'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['website']