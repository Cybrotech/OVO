# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'website_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'website', ['Category'])

        # Adding model 'Website'
        db.create_table(u'website_website', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('vertical_category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='websites', to=orm['website.Category'])),
            ('unique_users_per_day', self.gf('django.db.models.fields.IntegerField')()),
            ('page_views_per_day', self.gf('django.db.models.fields.IntegerField')()),
            ('unique_users_per_month', self.gf('django.db.models.fields.IntegerField')()),
            ('page_views_per_month', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'website', ['Website'])

        # Adding model 'Section'
        db.create_table(u'website_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections', to=orm['website.Website'])),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('section_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'website', ['Section'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'website_category')

        # Deleting model 'Website'
        db.delete_table(u'website_website')

        # Deleting model 'Section'
        db.delete_table(u'website_section')


    models = {
        u'website.category': {
            'Meta': {'object_name': 'Category'},
            'category_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'created_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'website.section': {
            'Meta': {'object_name': 'Section'},
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
            'vertical_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'websites'", 'to': u"orm['website.Category']"})
        }
    }

    complete_apps = ['website']