 
from rest_framework import serializers
 
from flights.models import Booking, Flight
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model 
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["destination", "time", "price", "id"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "id"]


class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "passengers", "id"]
   

class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["date", "passengers"]

# DRF Task3: Register View 
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField (write_only=True) # to hash the password and not return it with request
    class Meta:
        model = User 
        fields = "username", "password", "first_name", "last_name"
        
        def create(self, validated_data):
            username = validated_data["username"]
            password = validated_data["password"]
            first_name = validated_data["first_name"]
            last_name = validated_data["last_name"]

            new_user = User(username=username)
            new_user.set_password(password)
            new_user.save()
            return validated_data

# DRF Task4: create&login
class LoginSerializer(serializers.Serializer): #no modelserializer t login because it doesn't make obj's
    username = serializers.CharField()
    password = serializers.CharField(write_only=True) #the attribute is write only so the password become hased
    token = serializers.CharField(read_only=True, allow_blank=True) # token = access , samething different name
    
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Username Not Found ")
    
        if user.check_password(password):
            payload = RefreshToken.for_user(user)
            token = str(payload.access_token)
            raise serializers.ValidationError("username or password is not valid")  
            
            data["token"] = token    
            return data 
        
        else: 
            raise serializers.ValidationError("username or password is not valid")

# DRF Task5: permission
class CreateFlightSerilazer(serializers.ModelSerializer):
    passengers = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Booking
        fields = ["id","date","flight","passengers"]
