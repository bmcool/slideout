from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from mezzanine.conf import settings

from order.models import *

import uuid
import time

class Member(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")
    
    def __unicode__(self):
        return self.user.username

def level_upload_to(instance, filename):
    print "%s/%s/%s/%s.%s" % ("resource", instance.owner.user.username, "levels", str(time.time()), str(uuid.uuid4()))
    return "%s/%s/%s/%s.%s" % ("resource", instance.owner.user.username, "levels", str(time.time()), str(uuid.uuid4()))

class Level(OrderedModel):
    owner = models.ForeignKey(Member)
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    level = models.FileField(verbose_name=_("Level"), upload_to=level_upload_to, help_text=_("upload your json level file that created by 'Tiled map editor'"))
    published = models.BooleanField(_("Published"), default=False)
    
    def __unicode__(self):
        return self.title

# def sprite_upload_to(instance, filename):
    # return "%s/%s/%s/%s.%s" % ("resource", instance.owner.user.username, "sprites", str(time.time), str(uuid.uuid4()))

# class Sprite(models.Model):
    # owner = models.ForeignKey(Member)
    # sprite = models.FileField(verbose_name=_("Sprite"), upload_to=sprite_upload_to, help_text=_("upload your sprite that tile size is 32x32"))

# def player_upload_to(instance, filename):
    # return "%s/%s/%s/%s.%s" % ("resource", instance.owner.user.username, "players", str(time.time), str(uuid.uuid4()))

# class Player(models.Model):
    # owner = models.ForeignKey(Member)
    # player = models.FileField(verbose_name=_("Player"), upload_to=player_upload_to, help_text=_("upload your player that tile size is 32x32"))

# class MemberSprite(models.Model):
    # member = models.ForeignKey(Member, unique=True)
    # sprite = models.ForeignKey(Sprite)

# class MemberPlayer(models.Model):
    # member = models.ForeignKey(Member, unique=True)
    # player = models.ForeignKey(Player)
