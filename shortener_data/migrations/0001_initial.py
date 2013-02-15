# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserAgentType'
        db.create_table(u'chimp_shortener_data_useragenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('is_human', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'chimp_shortener_data', ['UserAgentType'])

        # Adding model 'RequestData'
        db.create_table(u'chimp_shortener_data_requestdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chimp_shortener.Link'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('meta', self.gf('django.db.models.fields.TextField')()),
            ('accept', self.gf('django.db.models.fields.TextField')()),
            ('accept_encoding', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('accept_language', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('cache_control', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('connection', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('referer', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('via', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('x_forwarded_for', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('remote_addr', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('user_agent_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chimp_shortener_data.UserAgentType'])),
            ('user_agent_has_url', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'chimp_shortener_data', ['RequestData'])


    def backwards(self, orm):
        # Deleting model 'UserAgentType'
        db.delete_table(u'chimp_shortener_data_useragenttype')

        # Deleting model 'RequestData'
        db.delete_table(u'chimp_shortener_data_requestdata')


    models = {
        u'chimp_shortener.link': {
            'Meta': {'object_name': 'Link'},
            '_hash': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2083'})
        },
        u'chimp_shortener_data.requestdata': {
            'Meta': {'object_name': 'RequestData'},
            'accept': ('django.db.models.fields.TextField', [], {}),
            'accept_encoding': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'accept_language': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'cache_control': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'connection': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chimp_shortener.Link']"}),
            'meta': ('django.db.models.fields.TextField', [], {}),
            'referer': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'remote_addr': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'user_agent_has_url': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_agent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chimp_shortener_data.UserAgentType']"}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'x_forwarded_for': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'chimp_shortener_data.useragenttype': {
            'Meta': {'object_name': 'UserAgentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_human': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['chimp_shortener_data']