from django.contrib import admin
from .models import Quiz, Question, Choice, UserResponse, QuizResponse

# Existing ChoiceInline and QuestionAdmin classes

class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_choice', 'quiz_session')
    search_fields = ['user__username', 'quiz_session']

class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score')
    search_fields = ['student__username', 'quiz__name']

class ChoiceInline(admin.TabularInline):  # You can also use admin.StackedInline
    model = Choice
    extra = 1  # Number of empty choice forms
    fields = ('text', 'is_correct')  # Add 'is_correct' to be able to select the correct choice from the admin

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'score')  # Display 'text' and 'score' in the admin listing
    search_fields = ['text']  # Allow search by 'text'
    
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'cutoff_mark', 'timer')  # Display these fields in the admin listing

# Register your models here
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(UserResponse, UserResponseAdmin)
admin.site.register(QuizResponse, QuizResponseAdmin)
