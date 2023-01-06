from rest_framework import serializers
from django.db import transaction
from .models import *


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input-type': 'password'}, write_only=True, required=False)
    password = serializers.CharField(style={'input-type': 'password'}, write_only=True, required=False)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'password2', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']

    # def validate_email(self, value):
    #     if not self.context.get('is_update', False):
    #         qs = User.objects.filter(email__exact=value)
    #         if qs.exists():
    #             raise serializers.ValidationError("User with this email already exists")
    #     return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password should be minimum 6 characters long")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__exact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username already exists")
        return value

    def validate(self, data):
        if self.context.get('is_update_password'):
            pw = data.get('password')
            pw2 = data.pop('password2')
            if pw != pw2:
                raise serializers.ValidationError("Password must match")
            return data
        return data

    def create(self, validated_data):
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        is_active = validated_data.get("is_active", False)
        email = validated_data.get("email")
        password = validated_data.get("password")
        # user_obj = User(email=email, first_name=first_name, last_name=last_name)
        user_obj, created = User.objects.update_or_create(email=email, first_name=first_name, last_name=last_name)
        user_obj.set_password(password)
        # user_obj.username = uuid.uuid4()
        # user_obj.username = email.split("@", 1)[0]
        user_obj.username = email
        user_obj.is_active = is_active
        user_obj.save()
        return user_obj

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        if validated_data.get('password'):
            instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    # avatar = Base64ImageField(
    #     max_length=None, use_url=True
    # )
    # avatar = serializers.ImageField(required=False, max_length=10000, validators=[
    #     FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif', 'bmp']), validate_file_size])

    class Meta:
        model = Student
        # fields = '__all__'
        fields = [
            'user',
            'contact_no',
            'street_address',
            'city_name',
            'state',
            'zip_code',
            'country',
            'avatar',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        # secret_key = generate_user_secret_key()
        referral_code = validated_data.get('referral_code', None)

        # pin = generate_random_pin()
        with transaction.atomic():
            user_obj = UserSerializer.create(serializer, validated_data=user_data)
            referrer = None
            # if referral_code:
            #     try:
            #         referrals = Referral.objects.filter(patient__referral_code=referral_code)
            #         if referrals:
            #             referrer = referrals.first().patient
            #             referrer.referral_eligible_discount = True
            #     except Customer.DoesNotExist:
            #         pass
            if referrer is not None:
                customer = Student.objects.create(user=user_obj,
                                                  referral_eligible_discount=True, **validated_data)
            else:
                customer = Student.objects.create(user=user_obj, **validated_data)

        return customer

    def update(self, instance, validated_data):
        # request = self.context.get('request', None)
        request = self.context['request']
        if 'user' in validated_data:
            user_data = validated_data.pop("user")

            user_serializer = UserSerializer(instance=instance.user, data=user_data, context={"request": request},
                                             partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.city_name = validated_data.get('city_name', instance.city_name)
        instance.street_address = validated_data.get('street_address', instance.street_address)
        instance.contact_no = validated_data.get('contact_no', instance.contact_no)
        instance.save()
        return instance


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = '__all__'


class StudyModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMode
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        # fields = [
        #     'id',
        #     'degree',
        #     'semester',
        #     'category',
        #     'difficulty',
        #     'study_mode',
        #     'name',
        #     'rating',
        #     'price',
        #     'credit_hours',
        #     'photo',
        #     'photo_url'
        # ]

    def get_quantity(self, obj):
        self.quantity = 1
        return self.quantity

    def get_total_price(self, obj):
        total_price = self.quantity * obj.price
        return total_price
