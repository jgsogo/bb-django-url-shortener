# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Link.url'
        db.alter_column(u'chimp_shortener_link', 'url', self.gf('django.db.models.fields.CharField')(max_length=2083))

    def backwards(self, orm):

        # Changing field 'Link.url'
        db.alter_column(u'chimp_shortener_link', 'url', self.gf('django.db.models.fields.CharField')(max_length=512))

    models = {
        u'chimp_shortener.link': {
            'Meta': {'object_name': 'Link'},
            '_hash': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2083'})
        }
    }

    complete_apps = ['chimp_shortener']