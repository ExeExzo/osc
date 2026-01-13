from rest_framework import serializers
from .models import CamperRegister, Camp
import re
from datetime import datetime, date
import pdfplumber


class CamperSerializer(serializers.ModelSerializer):
    parent_username = serializers.SerializerMethodField()
    parent_full_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    camp_name = serializers.SerializerMethodField()

    class Meta:
        model = CamperRegister
        fields = ['full_name', 'iin', 'birth_date', 'parent', 'parent_username', 'parent_full_name', 'camp_name', 'status', 'status_display']
        read_only_fields = fields

    def get_parent_username(self, obj):
        return obj.parent.username if obj.parent else None

    def get_parent_full_name(self, obj):
        return obj.parent.get_full_name() if obj.parent else None
    
    def get_camp_name(self, obj):
        return obj.camp.name if obj.camp else None


class CamperRegistrationSerializer(serializers.ModelSerializer):
    camp_id = serializers.IntegerField(write_only=True, required=True)
    uploaded_id = serializers.FileField(required=True)

    class Meta:
        model = CamperRegister
        fields = ["full_name", "iin", "birth_date", "uploaded_id", "camp_id"]
        read_only_fields = ["full_name", "iin", "birth_date"]

    def validate_camp_id(self, value):
        try:
            camp = Camp.objects.get(id=value)
        except Camp.DoesNotExist:
            raise serializers.ValidationError("Лагерь с таким ID не найден")
        return value

    def validate_uploaded_id(self, file):
        if file.content_type != "application/pdf":
            raise serializers.ValidationError("Загруженный файл должен быть PDF")
        if file.size > 5 * 1024 * 1024:  # 5MB ограничение
            raise serializers.ValidationError("Размер файла не должен превышать 5MB")
        return file

    def validate(self, attrs):
        pdf_file = attrs.get("uploaded_id")
        camp_id = attrs.get("camp_id")

        errors = []

        try:
            with pdfplumber.open(pdf_file) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            text = text.replace("\n", " ")
        except Exception:
            raise serializers.ValidationError({"uploaded_id": "Ошибка при обработке PDF"})

        # ---------- ИИН ----------
        iin_match = re.search(r"\b\d{12}\b", text)
        if not iin_match:
            errors.append("ИИН не найден или не состоит из 12 цифр")
        else:
            iin = iin_match.group()
            if CamperRegister.objects.filter(iin=iin, camp_id=camp_id).exists():
                raise serializers.ValidationError({"iin": "Ребёнок с таким ИИН уже зарегистрирован в этом лагере"})
            attrs["iin"] = iin

        # ---------- Дата рождения ----------
        dates = re.findall(r"\b\d{2}\.\d{2}\.\d{4}\b", text)
        if len(dates) >= 1:
            try:
                attrs["birth_date"] = datetime.strptime(dates[0], "%d.%m.%Y").date()
            except ValueError:
                errors.append("Неверный формат даты рождения")
        else:
            errors.append("Не удалось найти дату рождения")

        # ---------- ФИО ----------
        words = [w for w in text.split() if w.isalpha() and len(w) > 2]
        if len(words) >= 3:
            attrs["full_name"] = f"{words[0]} {words[1]} {words[2]}"
        else:
            errors.append("Не удалось определить ФИО")

        if errors:
            raise serializers.ValidationError({"errors": errors})

        return attrs

    def create(self, validated_data):
        camp_id = validated_data.pop("camp_id")
        camp = Camp.objects.get(id=camp_id)
        user = self.context["request"].user

        camper = CamperRegister.objects.create(
            parent=user,
            camp=camp,
            status="pending",
            **validated_data
        )
        return camper
    

class CampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camp
        fields = ['id', 'name', 'location', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']