# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Arch'
        db.create_table('packages_arch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16, db_index=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('packages', ['Arch'])

        # Adding model 'Package'
        db.create_table('packages_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.Section'])),
            ('distversion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.DistVersion'])),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.Repository'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('size_compressed', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('size_uncompressed', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('requires', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('conflicts', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('suggests', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('build', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True, blank=True)),
            ('arch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.Arch'])),
            ('extension', self.gf('django.db.models.fields.CharField')(default='txz', max_length=4, db_index=True)),
            ('pc_checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('packages', ['Package'])

        # Adding model 'Section'
        db.create_table('packages_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.Repository'])),
            ('distversion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.DistVersion'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('crawl', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('pc_checksum', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal('packages', ['Section'])

        # Adding model 'Mirror'
        db.create_table('packages_mirror', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.Repository'])),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True, blank=True)),
            ('alive', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True, blank=True)),
        ))
        db.send_create_signal('packages', ['Mirror'])

        # Adding model 'Repository'
        db.create_table('packages_repository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('default_mirror', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='default_mirror', null=True, to=orm['packages.Mirror'])),
            ('encoding', self.gf('django.db.models.fields.CharField')(default='utf-8', max_length=16)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('crawl', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('packages', ['Repository'])

        # Adding model 'SubRepository'
        db.create_table('packages_subrepository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.Repository'])),
        ))
        db.send_create_signal('packages', ['SubRepository'])

        # Adding model 'DistVersion'
        db.create_table('packages_distversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('packages', ['DistVersion'])

        # Adding model 'SearchLog'
        db.create_table('packages_searchlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('distversion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.DistVersion'], null=True)),
            ('advanced', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('packages', ['SearchLog'])


    def backwards(self, orm):
        
        # Deleting model 'Arch'
        db.delete_table('packages_arch')

        # Deleting model 'Package'
        db.delete_table('packages_package')

        # Deleting model 'Section'
        db.delete_table('packages_section')

        # Deleting model 'Mirror'
        db.delete_table('packages_mirror')

        # Deleting model 'Repository'
        db.delete_table('packages_repository')

        # Deleting model 'SubRepository'
        db.delete_table('packages_subrepository')

        # Deleting model 'DistVersion'
        db.delete_table('packages_distversion')

        # Deleting model 'SearchLog'
        db.delete_table('packages_searchlog')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'packages.arch': {
            'Meta': {'object_name': 'Arch'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16', 'db_index': 'True'})
        },
        'packages.distversion': {
            'Meta': {'object_name': 'DistVersion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'packages.mirror': {
            'Meta': {'object_name': 'Mirror'},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True', 'blank': 'True'}),
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['packages.Repository']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'packages.package': {
            'Meta': {'object_name': 'Package'},
            'arch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['packages.Arch']"}),
            'build': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'conflicts': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'distversion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['packages.DistVersion']"}),
            'extension': ('django.db.models.fields.CharField', [], {'default': "'txz'", 'max_length': '4', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'pc_checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['packages.Repository']"}),
            'requires': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['packages.Section']"}),
            'size_compressed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'size_uncompressed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'suggests': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'packages.repository': {
            'Meta': {'object_name': 'Repository'},
            'crawl': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'default_mirror': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_mirror'", 'null': 'True', 'to': "orm['packages.Mirror']"}),
            'encoding': ('django.db.models.fields.CharField', [], {'default': "'utf-8'", 'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'packages.searchlog': {
            'Meta': {'object_name': 'SearchLog'},
            'advanced': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'distversion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['packages.DistVersion']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        'packages.section': {
            'Meta': {'object_name': 'Section'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'crawl': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True', 'blank': 'True'}),
            'distversion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['packages.DistVersion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pc_checksum': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['packages.Repository']"})
        },
        'packages.subrepository': {
            'Meta': {'object_name': 'SubRepository'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['packages.Repository']"})
        }
    }

    complete_apps = ['packages']
