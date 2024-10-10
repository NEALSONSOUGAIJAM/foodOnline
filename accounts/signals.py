from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from . models import User,UserProfile



# create a receiver--function (signals)

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):#created will return it true when profile/object is created
    print(created)
    if created:
        UserProfile.objects.create(user=instance)#create user profile as soon as user is created
    else:
        try:
            profile = UserProfile.objects.get(user=instance)#update
            profile.save()
        except:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)

#one way of connecting the receiver to the sender (user is a sender)
#post_save.connect(post_save_create_profile_receiver,sender=User)

            


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):#just before the user is created
    pass
# post_save.connect(post_save_create_profile_receiver, sender=User)