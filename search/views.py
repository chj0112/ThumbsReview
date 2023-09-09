from django.shortcuts import render


# Create your views here.
def main(request):
    return render(request, 'search/main.html')


def base(request):
    return render(request, 'search/base.html')


def list(request):
    value = request.GET['value']
    return render(request, 'search/list.html', {'value': value})


def info(request):
    return render(request, 'search/info.html')


def test(request):
    return render(request, 'search/test.html')


def kakao(request):
    return render(request, 'search/kakao.html')