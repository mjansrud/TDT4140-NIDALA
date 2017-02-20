from django.shortcuts import render
from .forms import LoginForm
def index(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            pass
        else:
            print('Not valid')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'nidala/index.html', context)
