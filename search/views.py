from django.shortcuts import render
from modules import scrapping
from modules import test_h5


# Create your views here.
def main(request):
    return render(request, 'search/main.html')


def base(request):
    return render(request, 'search/base.html')


def list(request):
    value = request.GET['value']
    store_list = scrapping.kakao(value)
    return render(request, 'search/list.html', {'value': value, 'store_list': store_list})


def info(request):
    return render(request, 'search/info.html')


def test(request):
    return render(request, 'search/test.html')


def kakao(request):
    return render(request, 'search/kakao.html')


def store(request, store_id):
    store_name = scrapping.review(store_id)
    # model('input.tsv')
    test_h5.Our_model('modules/input.tsv')
    f = open('modules/output.tsv', 'r', encoding='utf-8')
    f.readline()
    reviews = []
    for line in f:
        tmp = []
        tmp = line.split('\t')
        print(tmp)
        reviews.append({'review': tmp[1].replace('<br/>', '\n'), 'taste_r': tmp[2], 'taste_pn': tmp[3], 'service_r': tmp[4], 'service_pn': tmp[5].replace('\n', '')})
    return render(request, 'search/store.html', {'store_name': store_name, 'reviews': reviews})
