from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from pymongo import MongoClient

# Sample data for users, teams, activities, leaderboard, and workouts
USERS = [
    {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
    {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
    {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
    {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
    {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
    {"name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
]

TEAMS = [
    {"name": "Marvel", "members": ["Iron Man", "Captain America", "Black Widow"]},
    {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman"]},
]

ACTIVITIES = [
    {"user": "Superman", "activity": "Flying", "duration": 120},
    {"user": "Batman", "activity": "Martial Arts", "duration": 90},
    {"user": "Iron Man", "activity": "Suit Training", "duration": 60},
]

LEADERBOARD = [
    {"user": "Superman", "points": 300},
    {"user": "Iron Man", "points": 250},
    {"user": "Batman", "points": 200},
]

WORKOUTS = [
    {"name": "Strength Training", "level": "Advanced"},
    {"name": "Cardio Blast", "level": "Intermediate"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["octofit_db"]

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Insert test data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Ensure unique index on email
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
