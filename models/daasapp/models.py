from django.db import models
import json, os
import datetime
from django.contrib.auth import hashers
import hmac, uuid
from django.conf import settings

# User superclass
class User(models.Model):
    username = models.CharField(max_length=65, unique=True)
    password = models.CharField(max_length=200) # stored as hash
    email_address = models.EmailField()
    date_joined = models.DateTimeField()
    is_active = models.BooleanField()
    f_name = models.CharField(max_length=16)
    l_name = models.CharField(max_length=16)
    bio = models.TextField()

    # gets called in 'create_user' view if exp API did not already hash
    def set_password(self, raw_pw):
      self.password = hashers.make_password(raw_pw)

    def to_json(self): 
      return dict(
        username = self.username,
        password = self.password,
        email_address = self.email_address,
      	date_joined = self.date_joined,
        is_active = self.is_active,
        f_name = self.f_name,
        l_name = self.l_name,
        bio = self.bio,
        user_id = self.id
      )
    
    def __unicode__(self):
      return self.id

    def __str__(self):
      return "ID is %s, Username is %s, password is %s, email address is %s" % (self.id, self.username, self.password, self.email_address)
	
    #TODO jobs #(list of all Job objects that belong to the user)

class Authenticator(models.Model):
  user_id = models.IntegerField() # user primary key
  #authenticator = models.CharField(primary_key=True, editable=False, max_length=255) # set by HMAC algorithm
  authenticator = models.CharField(primary_key=True, default=hmac.new(key = settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256').hexdigest(), max_length=255) # set by HMAC algorithm

  date_created = models.DateTimeField() 
  # should time be baked into the authenticator token? attacker could compromise time-validity of tokens if compromised database. ask prof

  def to_json(self): 
    return dict(
      user_id = self.user_id,
      date_created = self.date_created,
      authenticator = self.authenticator
    )
  
  def __unicode__(self):
    return self.authenticator



# Listings Class
class Listing(models.Model):
    owner = models.ForeignKey('User') #@sam what additional steps do we need
    drone = models.ForeignKey('Drone') #is this set up for done??
    price_per_day = models.FloatField() # [ask TAs how to do price, also just look at project descriptions to see what we need to do for this]
    time_posted = models.DateTimeField()
    description = models.TextField()
    #listing_status = models.CharField(choices = [(str(i),['available','unavailable'][i-1]) for i in range(1,3)], max_length=50, default='1') # take out for now (unsure of how to integrate)

    def to_json(self):
      return dict(
        owner = self.owner.to_json(), # need to serialize the foreignkey object
        drone = self.drone.to_json(),
        price_per_day=self.price_per_day,
        time_posted = self.time_posted,
        description = self.description,
        #listing_status = self.listing_status,
        listing_id = self.id
      )

    def __unicode__(self):
      return self.id
''' 
our future plans.... :-) stay tuned!
# Host subclass extends from User class
class Host(models.Model):

    # calculation based on specific equation
    host_reputation = models.FloatField()
    user = models.OneToOneField(User)
    drones_owned = models.OneToManyField(Drone)
    drones_available = models.OneToManyField(Drone)
    drones_deployed = models.OneToManyField(Drone)


# Client subclass extends from User class
class Client(models.Model):
    client_reputation = models.FloatField()
    user = models.OneToOneField(User)

'''

class Drone(models.Model):
    model_name = models.CharField(max_length=50)
    drone_desc = models.TextField()
    demo_link = models.URLField() # (link to photo gallery or videos)
    permissions = models.TextField()
    owner_email = models.EmailField()
    battery_level = models.FloatField()
    maintenance_status = models.TextField()
    available_for_hire = models.BooleanField()
    owner = models.ForeignKey('User')
    last_checked_out = models.DateTimeField() 
    
    #TODO location (tuple(float, float))
    # picture = models.ImageField() (image format)

    # POST APIs are in ../api-posts.py
    def to_json(self):
      return dict(
        model_name = self.model_name,
        drone_desc = self.drone_desc,
        demo_link = self.demo_link,
      	permissions = self.permissions,
        owner_email = self.owner_email,
        battery_level = self.battery_level,
        maintenance_status = self.maintenance_status,
        available_for_hire = self.available_for_hire,
        owner = self.owner.to_json(), # need to serialize the foreignkey object
        last_checked_out = self.last_checked_out,
        drone_id = self.id
      )

    def __str__(self):
      return "Drone model name is %s, description is %s, id number is %s" % (self.model_name, self.drone_desc, self.id)

    def __unicode__(self):
      return self.id

''' more future plans for our marketplace...
# [all of the subprocesses happening between client wanting a drone and drone returning to owner]
class Jobs(models.Model):
    transaction_id = models.CharField()
    drone_id = models.CharField()
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    price_per_day = models.FloatField() # [ask TAs how to do price, also just look at project descriptions to see what we need to do for this]
    transaction_time = models.DateTimeField()
    job_status_choices = ['cancelled', 'active', 'inactive']
    job_status = models.CharField(choices = job_status_choices)
    #TODO schedule (Schedule object)


class Schedule(models.Model): # [perhaps create superclass and have separate jobs/drone schedules]
    schedule_id = models.CharField()
    time_leased = models.DateTimeField()
    time_returned = models.DateTimeField()

#Client_Reputation: [to be determined. includes block cipher stuffs.]

#Host_Reputation: [to be determined. includes block cipher stuffs.]
'''
