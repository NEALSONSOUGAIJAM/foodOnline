from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager



# Create your models here.

# it has two method
#it does not contain any field and contain only methods
# 1st method is to create regular user and 2nd method is to creat super user


# baseuse manager allow  to edit the user and super user created
class UserManager(BaseUserManager):
    def create_user(self, first_name,last_name, username, email, password=None):
        if not email:
            raise ValueError('user must have email')
        if not username:
            raise ValueError('user must have username')
        # start creating user
        user = self.model(
            email= self.normalize_email(email),
            username = username,
            first_name =first_name,
            last_name = last_name,
        )
        user.set_password(password)# set_password is to take p and encode the p and store it in the database
        user.save(using=self._db)# it will take default databse that will configure in the setting file
        return user
    
    def create_superuser(self, first_name,last_name, username, email, password=None):
         #  already create user to create superuser firdt creat user
         user = self.create_user(
            email= self.normalize_email(email),
            username = username,
            password = password,
            first_name =first_name,
            last_name = last_name,
        )
         user.is_admin =True
         user.is_active = True
         user.is_staff = True
         user.is_superadmin = True
         user.save(using=self._db)
         return user


#it contain fielname

class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE=(
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True)
    phone_no = models.CharField(max_length=50,blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)

    #required field

    date_joined =models.DateField(auto_now_add= True)
    last_login =models.DateField(auto_now_add= True)
    created_date =models.DateField(auto_now_add= True)
    modified_date =models.DateField(auto_now= True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =['username','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm ,obj =None):
        return self.is_admin
    
    def has_module_perms(self,app_lebel):
        return True
    
    def get_role(self):
        if self.role ==1:
            user_role ='Vendor'
        elif self.role ==2:
            user_role ='Customer'    
            return user_role



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)# one user can have one user profile
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
   # location = gismodels.PointField(blank=True, null=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def full_address(self):
    #     return f'{self.address_line_1}, {self.address_line_2}'

    def __str__(self):
        return self.user.email



   ### self.location = Point(float(self.longitude), float(self.latitude))
       #     return super(UserProfile, self).save(*args, **kwargs)
        #return super(UserProfile, self).save(*args, **kwargs)
        