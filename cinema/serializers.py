from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from cinema.models import Movie, Genre, Actor, CinemaHall


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=50,
        required=True,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class ActorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)

    def create(self, validated_data):
        return Actor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name",
                                                 instance.first_name)
        instance.last_name = validated_data.get("last_name",
                                                instance.last_name)
        instance.save()
        return instance


class CinemaHallSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50, required=True)
    rows = serializers.IntegerField(required=True)
    seats_in_row = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return CinemaHall.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.rows = validated_data.get("rows", instance.rows)
        instance.seats_in_row = validated_data.get("seats_in_row",
                                                   instance.seats_in_row)
        instance.save()
        return instance


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    actors = serializers.PrimaryKeyRelatedField(many=True,
                                                queryset=Actor.objects.all())
    genres = serializers.PrimaryKeyRelatedField(many=True,
                                                queryset=Genre.objects.all())
    duration = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ["id",
                  "title",
                  "description",
                  "duration",
                  "actors",
                  "genres"]

    def create(self, validated_data):
        actors_data = validated_data.pop("actors")
        genres_data = validated_data.pop("genres")
        movie = Movie.objects.create(**validated_data)

        movie.actors.set(actors_data)
        movie.genres.set(genres_data)

        return movie

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.duration = validated_data.get("duration", instance.duration)

        instance.save()

        return instance
