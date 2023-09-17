# from django.core.mail import send_mail
from .models import (
    User,
    UserConfirmation,
    VIA_EMAIL,
    VIA_PHONE,
    NEW,
    CODE_VERIFIED,
    DONE,
    PHOTO_STEP,
)
from rest_framework import exceptions
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shared.utils import check_email_or_phone, send_email


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True) # ma'lumotni faqatgina olish uchun ishlatilinadi
    # yani biz ID ni yaratishimiz shart emas

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)
        # Modelga bog'liq bo'lmagan holda yangi maydon yaratish
        # bu yerda modelda mavjud bo'lmagan email_phone_number
        # fieldini yaratamiz
        
    class Meta:
        model = User
        fields = (
            'id',
            'auth_type',
            'auth_status'
        )
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False}
        }
    
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        print(user)
        # user -> email -> email jo'natish kerak
        # phone number bo'lsa telefoniga kodni jo'natishi kerak
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            print(code)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            print(code)
            # send_phone_code(user.phone_number, code)
        user.save()
        return user

    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    @staticmethod
    def auth_validate(data):
        user_input = str(data.get('email_phone_number')).lower()
        input_type = check_email_or_phone(user_input)
        
        if input_type == 'email':
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL
            }
        elif input_type == 'phone':
            data = {
                'phone_number': user_input,
                'auth_type': VIA_PHONE
            }
        else:
            data = {
                'success': False,
                'message': 'you must send email or phone number'
            }
            raise ValidationError(data)

        return data
    
    def validate_email_phone_number(self, value):
        value = value.lower()
        print(f"{value=}****======****")

        return value

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())

        return data
