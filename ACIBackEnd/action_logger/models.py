import json

from django.db import models

# Create your models here.

class LoggerManager(models.Manager):

    def log_action(self, user_id, request_ip, content_type_id, object_id, object_dict, action_flag, change_message=""):
        if isinstance(change_message, list):
            change_message = json.dumps(change_message)
            self.model.objects.create(user_id=user_id, request_ip=request_ip, content_type_id=content_type_id,
                                      object_id=object_id,
                                      object_dict=object_dict, action_flag=action_flag, change_message=change_message)


