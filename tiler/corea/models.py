from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from mezzanine.conf import settings

from order.models import *

from xml.etree.ElementTree import ElementTree

import uuid
import time

class Member(models.Model):
    user = models.OneToOneField(User)
    
    class Meta:
        db_table = 'tiler_member'
        verbose_name = _("Member")
        verbose_name_plural = _("Members")
    
    def __unicode__(self):
        return self.user.username

def level_upload_to(instance, filename):
    print "%s/%s/%s/%s.%s" % ("resource", instance.owner.user.username, "levels", str(time.time()), str(uuid.uuid4()))
    return "%s/%s/%s/%s.%s" % ("resource", instance.owner.user.username, "levels", str(time.time()), str(uuid.uuid4()))

class BaseLevel(OrderedModel):
    owner = models.ForeignKey(Member, editable=False)
    title = models.CharField(_("Title"), max_length=100, blank=True)
    level = models.FileField(verbose_name=_("Level"), upload_to=level_upload_to, help_text=_("upload your tmx level file that created by 'Tiled map editor'"))
    published = models.BooleanField(_("Published"), default=False, help_text=_("If not published, only you can view this level"))
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.title
    
    def _normalize_type_attribute(self, attr):
        try:
            return int(attr)
        except ValueError:
            if attr == "True":
                return True
            elif attr == "False":
                return False
            else:
                return attr
    
    def _get_attributes_data(self, node):
        attributes = dict()
        for name, attr in node.items():
            attribute = self._normalize_type_attribute(attr)
            attributes.update({name:attribute})
        return attributes
    
    @property
    def lvl(self):
        lvl = dict()
        
        xmltree = ElementTree()
        xmltree.parse(self.level.path)
        
        lvl.update(self._get_attributes_data(xmltree.getroot()))
        
        layers = list()
        for layer_node in xmltree.findall('layer'):
            layer = dict()
            layer.update(self._get_attributes_data(layer_node))
            
            data = list()
            for tile_node in layer_node.findall('data/tile'):
                data.append(self._normalize_type_attribute(tile_node.get('gid')))
            layer["data"] = data
            layer["type"] = "tilelayer"
            layers.append(layer)
        
        for objectgroup_node in xmltree.findall('objectgroup'):
            objectgroup = dict()
            objectgroup.update(self._get_attributes_data(objectgroup_node))
            
            objects = list()
            for object in objectgroup_node.findall('object'):
                objects.append(self._get_attributes_data(object))
            objectgroup["objects"] = objects
            objectgroup["type"] = "objectgroup"
            layers.append(objectgroup)
                
        lvl["layers"] = layers
        return lvl
