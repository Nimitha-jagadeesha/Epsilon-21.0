from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm,ProfileRegisterForm
from .models import Score, Question, Display
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.views import LogoutView
import random
class YourCustomLogoutView(LogoutView):

    def get_next_page(self):
        next_page = super(YourCustomLogoutView, self).get_next_page()
        messages.add_message(
            self.request, messages.SUCCESS,
            'You successfully log out!'
        )
        return next_page

def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """ 
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect('Home') 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

def home(request):
    return render(request, 'epsilon/home.html')


def learderboard(request):
    list = ['-points', 'last_submit']
    Scoreboard = Score.objects.filter(visible = True).order_by(*list)
    return render(request, 'epsilon/leaderboards.html', {'Scoreboard': Scoreboard})

@login_excluded('app:redirect_to_view')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        p_form = ProfileRegisterForm(request.POST)
        if form.is_valid() and p_form.is_valid():
            user = form.save()
            p_form.instance.user = user
            p_form.full_clean()
            p_form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created ! You can now login')
            return redirect(reverse('login'))
    else:
        form = UserRegisterForm()
        p_form = ProfileRegisterForm()
    return render(request, 'epsilon/register.html', {'form': form,'p_form':p_form})


@csrf_exempt
@login_required
def arena(request):
    number = request.user.score.question_number
    if(number==0):
        number = random.randint(1,Question.objects.count())
        Score.objects.filter(user=request.user).update(
                question_number=number)
        Score.objects.filter(user=request.user).update(
                picked=request.user.score.picked+[number] )
    question = Question.objects.filter(
        number=number).first()
    x = False
    display = Display.objects.all()[0].display
    display = display|request.user.is_superuser
    try:
        if question.image != 'none.jpg':
            x = True
    except:
        pass
    if request.method == 'POST':
        answer = request.POST.get('answer')
        answer = answer.replace(" ","")
        answer = answer.replace(".","")
        if  not Question.objects.filter(number=request.user.score.question_number).first():
            return redirect('Arena')
        crct_answer = Question.objects.filter(
            number=request.user.score.question_number).first().answer
        crct_answer =crct_answer.replace(" ","")
        crct_answer = crct_answer.replace(".","")
        if answer.lower().strip() == crct_answer.lower() or (request.user.score.question_number == 13 and answer.lower().strip() == "tomandjerry"):
            numbers = Score.objects.filter(user=request.user).first()
            numbers = numbers.picked
            qlen = Question.objects.count()
            numlist = range(1,qlen+1)
            numlist =[el for el in numlist if el not in numbers]
            if len(numlist )== 0:
                number = qlen+1
            else:
                number = random.choice(numlist)
            
            Score.objects.filter(user=request.user).update(
                question_number=number)
            Score.objects.filter(user=request.user).update(
                picked=request.user.score.picked+[number] )
            Score.objects.filter(user=request.user).update(
                points=request.user.score.points+1)
            Score.objects.filter(user=request.user).update(
                last_submit=timezone.now())
            question = Question.objects.filter(
                number=request.user.score.question_number).first()
            return redirect('Arena')
            try:
                if question.image != 'none.jpg':
                    x = True
            except:
                x = False
        else:
            messages.warning(request, 'Wrong answer :( Try again!')
            try:
                if question.image != 'none.jpg':
                    x = True
            except:
                x = False
            return render(request, 'epsilon/arena.html', {'question': question,'x':x,'display':display,'qnum':request.user.score.points+1})
    if question == None:
         return render(request, 'epsilon/arena.html', {'done': True})
    return render(request, 'epsilon/arena.html', {'question': question,'x':x,'display':display, 'qnum':request.user.score.points+1})