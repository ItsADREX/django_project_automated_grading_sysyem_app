from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import QuizForm, QuestionForm, ChoiceFormSet,ChoiceForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Quiz, Question, Choice, QuizResponse, UserResponse  # Import at the top of your file
from django.http import JsonResponse  # Add this import





@login_required
@user_passes_test(lambda u: u.user_type == 'INSTRUCTOR')
def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.creator = request.user  # setting the creator to the current user
            quiz.instructor = request.user  # setting the instructor to the current user
            quiz.save()
            return redirect('add_questions', quiz_id=quiz.id)  # Added quiz_id
    else:
        quiz_form = QuizForm()

    return render(request, 'QuizApp/create_quiz.html', {'quiz_form': quiz_form})





from .models import Quiz, Question, Choice

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Quiz, Question, Choice

@login_required
@user_passes_test(lambda u: u.user_type == 'INSTRUCTOR')
def add_questions(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == 'POST':
        print(request.POST)  # Debug line to see what data is being POSTed
        questions = request.POST.getlist('questions[]')
        choices = request.POST.getlist('choices[]')
        is_correct = request.POST.getlist('is_correct[]')  # Assuming this captures the 'checked' status

        choice_index = 0
        for question_text in questions:
            question = Question.objects.create(text=question_text, quiz=quiz)
            for _ in range(4):  # Assuming 4 choices per question
                if choice_index < len(choices):
                    print(f'Saving choice: {choices[choice_index]}')  # Debug line
                    Choice.objects.create(
                        text=choices[choice_index],
                        is_correct=('true' == is_correct[choice_index].lower()) if choice_index < len(is_correct) else False,
                        question=question
                    )
                else:
                    print(f'Skipping choice at index: {choice_index}')  # Debug line
                choice_index += 1

        return redirect('instructor_dashboard')

    return render(request, 'QuizApp/add_questions.html', {'quiz': quiz})











from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice
from django.http import HttpResponse, FileResponse

from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, QuizResponse


@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = quiz.questions.all()

    quiz_data = {question: question.choice_set.all() for question in questions}

    score = None
    details = []

    if request.method == 'POST':
        score = 0  
        for question_id, choice_id in request.POST.items():
            if "question_" in question_id:
                actual_question_id = int(question_id.split("_")[1])
                question = Question.objects.get(id=actual_question_id)
                try:
                    correct_choice = Choice.objects.get(question=question, is_correct=True)
                except Choice.DoesNotExist:
                    continue  # Skip this iteration and go to the next one

                is_correct = str(correct_choice.id) == choice_id
                if is_correct:
                    score += question.score
                
                details.append({
                    'question': question.text,
                    'user_answer': Choice.objects.get(id=choice_id).text if choice_id else 'No Answer',
                    'correct_answer': correct_choice.text,
                    'is_correct': is_correct
                })

        # Save the score to QuizResponse right here
        QuizResponse.objects.create(student=request.user, quiz=quiz, score=score)

        return render(request, 'QuizApp/quiz_results.html', {'score': score, 'details': details, 'quiz_id': quiz_id})

    return render(request, 'QuizApp/take_quiz.html', {'quiz': quiz, 'quiz_data': quiz_data, 'score': score})







@login_required
def download_pdf(request, quiz_id):
    # Fetch details from the session
    details = request.session.get('quiz_details', [])
    score = request.session.get('quiz_score', 0)

    # Reset session data (optional)
    del request.session['quiz_details']
    del request.session['quiz_score']

    # Normally, you'd generate a PDF here using something like ReportLab,
    # but for the sake of example, let's just use plain HTML.
    html_content = f"<h1>Your Score: {score}</h1><h2>Detailed Results:</h2>"

    for detail in details:
        status = "Correct" if detail['is_correct'] else "Incorrect"
        html_content += f"<p><strong>Question:</strong> {detail['question']}<br>"
        html_content += f"<strong>Your Answer:</strong> {detail['user_answer']}<br>"
        html_content += f"<strong>Correct Answer:</strong> {detail['correct_answer']}<br>"
        html_content += f"<strong>Status:</strong> {status}</p>"

    return HttpResponse(html_content)




from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import portrait, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def generate_pdf(context):
    pdf = SimpleDocTemplate(
        "QuizResults.pdf",
        pagesize=letter
    )
    
    score = context['score']
    details = context['details']

    data = [["Quiz Results"]]
    data.append(["Your Score:", str(score)])
    data.append([" ", " "])
    data.append(["Question", "Your Answer", "Correct Answer", "Status"])

    for detail in details:
        status = "Correct" if detail['is_correct'] else "Incorrect"
        data.append([detail['question'], detail['user_answer'], detail['correct_answer'], status])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements = [table]
    pdf.build(elements)







def quiz_results(request, quiz_id, total_score):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'QuizApp/quiz_results.html', {'quiz': quiz, 'total_score': total_score})
    


@login_required
@user_passes_test(lambda u: u.user_type == 'STUDENT')
def student_dashboard(request):
    available_quizzes = Quiz.objects.all()
    taken_quizzes = QuizResponse.objects.filter(student=request.user)
    return render(request, 'QuizApp/student_dashboard.html', {'available_quizzes': available_quizzes, 'taken_quizzes': taken_quizzes})


@login_required
@user_passes_test(lambda u: u.user_type == 'INSTRUCTOR')
def instructor_dashboard(request):
    created_quizzes = Quiz.objects.filter(instructor=request.user)
    return render(request, 'QuizApp/instructor_dashboard.html', {'created_quizzes': created_quizzes})



@login_required
def edit_quiz(request, quiz_id):
    # Logic to edit an existing quiz. You can reuse parts of your quiz-creating logic here.
    pass
