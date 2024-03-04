import logging
from rest_framework import serializers
from haberler.models import Makale, Gazeteci
from datetime import datetime
from django.utils.timesince import timesince


class GazeteciSerializer(serializers.ModelSerializer):
    # makaleler = MakaleSerializer(many=True, read_only=True)
    makaleler = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="makale-detay"
    )

    class Meta:
        model = Gazeteci
        fields = "__all__"


class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()
    # yazar = serializers.StringRelatedField()
    # yazar = GazeteciSerializer()

    class Meta:
        model = Makale
        # fields = ["yazar", "baslik"] gösterilenler ve update edilenler
        # exclude = ["id"] hariç tutmaya yarıyor
        fields = "__all__"

    def validate_baslik(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(f"baslik 5 karakterden düşük olamaz: ")
        return value

    def get_time_since_pub(self, data):
        logging.warning(data)
        now = datetime.now()
        pub_date = data.yayinlanma_tarihi
        time_delta = timesince(pub_date, now)
        return f"{time_delta}"


class MakaleSerializerGet(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()
    # yazar = serializers.StringRelatedField()
    yazar = GazeteciSerializer()

    class Meta:
        model = Makale
        # fields = ["yazar", "baslik"] gösterilenler ve update edilenler
        # exclude = ["id"] hariç tutmaya yarıyor
        fields = "__all__"

    def validate_baslik(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(f"baslik 5 karakterden düşük olamaz: ")
        return value

    def get_time_since_pub(self, data):
        logging.warning(data)
        now = datetime.now()
        pub_date = data.yayinlanma_tarihi
        time_delta = timesince(pub_date, now)
        return f"{time_delta}"


## STANDART SERIALIZATION ##
class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    aktif = serializers.BooleanField()
    yayinlanma_tarihi = serializers.DateField()
    yaratilma_tarihi = serializers.DateField(read_only=True)
    güncellenme_tarihi = serializers.DateField(read_only=True)

    def validate_baslik(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(f"baslik 5 karakterden düşük olamaz: ")
        return value

    def validate(self, data):
        if data["aciklama"] == data["baslik"]:
            raise serializers.ValidationError(f"Açıklama ve başlık aynı olamaz:")
        self.initial_data.pop("_state", None)
        self.initial_data.pop("yaratilma_tarihi", None)
        self.initial_data.pop("id", None)
        self.initial_data.pop("güncellenme_tarihi", None)
        # İstenmeyen alanları kontrol et
        istenmeyen_alanlar = set(self.initial_data.keys()) - set(
            [
                "yazar",
                "baslik",
                "aktif",
                "aciklama",
                "metin",
                "sehir",
                "yayinlanma_tarihi",
            ]
        )
        if istenmeyen_alanlar:
            raise serializers.ValidationError(
                f'İstenmeyen alanlar: {", ".join(istenmeyen_alanlar)}'
            )
        return data

    def create(self, validated_data):
        try:
            print(validated_data)
            return Makale.objects.create(**validated_data)
        except Exception as e:
            print("error creating ", e)

    def update(self, instance, validated_data):
        try:
            instance.yazar = validated_data.get("yazar", instance.yazar)
            instance.baslik = validated_data.get("baslik", instance.baslik)
            instance.aciklama = validated_data.get("aciklama", instance.aciklama)
            instance.metin = validated_data.get("metin", instance.metin)
            instance.sehir = validated_data.get("sehir", instance.sehir)
            instance.yayinlanma_tarihi = validated_data.get(
                "yayinlanma_tarihi", instance.yayinlanma_tarihi
            )
            instance.aktif = validated_data.get("aktif", instance.aktif)
            instance.save()
            return instance
        except Exception as e:
            print("error burada", e)
