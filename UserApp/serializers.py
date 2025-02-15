from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from .constants import *
import logging

logger = logging.getLogger("django")



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, **kwargs):
        try:
            validated_data = {**self.validated_data, **kwargs}
            request_method = self.context.get('request',{}).method  # Get HTTP method
            user_id = self.context.get('request',{}).parser_context.get('kwargs', {}).get('pk', None) # Get ID from url
            
            # update the data for user
            if request_method == "PUT" and user_id:
                try:
                    user = CustomUser.objects.get(id=user_id)
                    for attr, value in self.validated_data.items():
                        if attr == "password":
                            user.password = make_password(value)
                        else:
                            if attr == 'role':
                                if value == 'admin':
                                    user.is_superuser = True
                                    user.is_staff = True
                                    user.role = value
                                elif value == 'user':
                                    user.is_superuser = False
                                    user.is_staff = False
                                    user.role = value
                                else:
                                    serializers.ValidationError({"role": "Invalid role, 'admin', 'user' is allowed."})
                            else:
                                setattr(user, attr, value)
                    user.save()
                    return user
                except CustomUser.DoesNotExist:
                    raise serializers.ValidationError({"id": "User with this ID does not exist."})

            validated_data = {**self.validated_data, **kwargs}

            # Hash the password before saving
            validated_data['password'] = make_password(validated_data.get('password'))

            # Create user object
            user = CustomUser(**validated_data)

            # If the role is 'admin', grant admin privileges
            if validated_data.get('role') == 'admin':
                user.is_superuser = True
                user.is_staff = True
            user.save()
            return user
        except Exception as e:
            logger.error(str(e))
            raise serializers.ValidationError({"error": GLOBAL_ERROR_MSG})