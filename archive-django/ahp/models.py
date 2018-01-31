from django.db import models


# TODO: Update datatypes (i.e., CharField vs ints?)
# Climate categories
class Pollen(models.Model):
    zip_code = models.CharField(max_length=50)
    pollen_score = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


class SummerHigh(models.Model):
    zip_code = models.CharField(max_length=50)
    summer_high = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


class WinterLow(models.Model):
    zip_code = models.CharField(max_length=50)
    winter_low = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


class Humidity(models.Model):
    zip_code = models.CharField(max_length=50)
    humidity = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


# Social categories
class Walkability(models.Model):
    zip_code = models.CharField(max_length=50)
    walk_score = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


class Parkland(models.Model):
    zip_code = models.CharField(max_length=50)
    parkland = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


class SchoolRatings(models.Model):
    zip_code = models.CharField(max_length=50)
    school_ratings = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


class BusinessQuality(models.Model):
    zip_code = models.CharField(max_length=50)
    business_quality = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


# Economic categories
class Unemployment(models.Model):
    zip_code = models.CharField(max_length=50)
    unemployment = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


class CrimeRate(models.Model):
    zip_code = models.CharField(max_length=50)
    crime_rate = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


class ConsumerPriceIndex(models.Model):
    zip_code = models.CharField(max_length=50)
    consumer_price_index = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)


class Income(models.Model):
    zip_code = models.CharField(max_length=50)
    income = models.CharField(max_length=50)
    date_accessed = models.CharField(max_length=50)
