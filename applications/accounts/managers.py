from django.contrib.auth.models import BaseUserManager

# We inheritance from the class 'BaseUserManager' to override
# some functions that are already defined inside the class
class AccountManager(BaseUserManager):
    
    # Private method that only can be used in the underlying methods of this class
    def _create_user(self, first_name, last_name, username, email, password=None):
        
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        # self.model is refering to the madel that will use this manager
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        # Encrypting and setting the raw password given by the user 
        user.set_password(password)
        # Saving the user in our current database
        user.save(using=self._db)
        # Returning the user
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        # Using the private method _create_user described above to register a superuser
        user = self._create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        
        # Setting all the permissions to the superuser
        user.is_active    = True
        user.is_staff     = True
        user.is_superuser = True
        user.save(using=self._db)
       
        return user
