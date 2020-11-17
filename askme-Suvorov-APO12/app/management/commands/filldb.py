from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Rating, Question, Answer, Tag, RatingAuthors
from random import choice
from faker import Faker
from random import randint
from django.db import transaction


class Command(BaseCommand):
    f = Faker()
    
    def add_arguments(self, parser):
        parser.add_argument('--users', help = 'Fill users in data base')
        parser.add_argument('--answers', help = 'Fill answers in data base')
        parser.add_argument('--questions', help = 'Fill questions in data base')
        parser.add_argument('--tags', help = 'Fill tags in data base')
        parser.add_argument('--likes', help = 'Fill likes in data base')


    @transaction.atomic
    def fill_users(self, cnt = 10_000):
        user_names = set()        
        while len(user_names) < cnt:
            user_names.add(f.user_name() + f.user_name()[-3:])

        for i in range(cnt):
            user = User.objects.create(
                username = user_names.pop(),
                email = f.email(),
                password = f.password(),
            )
            Profile.objects.create(
                user = user,
                nick_name = f.word()[:50],
            )
       
 
    @transaction.atomic
    def fill_questions(self, cnt = 100_000):
        authors = Profile.objects.all()
        tags = Tag.objects.all()
        for i in range(cnt):
            question = Question.objects.create(
                author = choice(authors),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title = f.sentence()[:128],
            )        
            for _ in range(randint(0, 4)):
                question.tags.add(choice(tags))

   
    @transaction.atomic
    def fill_answers(self, cnt = 1_000_000):
        authors = Profile.objects.all()        
        questions = Question.objects.all()
        for i in range(cnt):
            Answer.objects.create(
                author = choice(authors),
                question = choice(questions),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                flag_correct_answer=f.pybool(),                
            )


    @transaction.atomic
    def fill_tags(self, cnt = 10_000):
        tags = set()
        while len(tags) < cnt:
            tags.add(f.word()[:10] + f.word()[:10])

        for _ in range(cnt):
            Tag.objects.create(
                name = tags.pop(),        
            )


    @transaction.atomic
    def fill_likes(self, cnt = 200_000):
        authors = Profile.objects.all()
        likes = Rating.objects.all()       
        for _ in range(cnt):
            like = choice(likes)
            count_likes = randint(0, 3)
            count_dislikes = randint(0, 3)
            like.count_likes += count_likes
            like.count_dislikes += count_dislikes 
            like.save()           
            for _ in range(count_likes + count_dislikes):
                RatingAuthors.objects.create(
                    rating = like,
                    profile = choice(authors),
                    type_opinion = f.pybool(),                                 
                )


    def handle(self, *args, **options):
        if options['tags']:
            self.fill_tags(int(options['tags']))        
        if options['users']:
            self.fill_users(int(options['users']))
        if options['questions']:
            self.fill_questions(int(options['questions']))
        if options['answers']:
            self.fill_answers(int(options['answers']))
        if options['likes']:
            self.fill_likes(int(options['likes']))
        
        
