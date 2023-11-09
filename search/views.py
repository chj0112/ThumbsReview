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
    taste_p, taste_n, taste_e, service_p, service_n, service_e = 0, 0, 0, 0, 0, 0
    for line in f:
        tmp = []
        tmp = line.split('\t')
        print(tmp)
        last = tmp[5].replace('\n', '')

        if tmp[2] == '1.0':
            if tmp[3] == '1.0':
                taste_p += 1
            elif tmp[3] == '0.0':
                taste_n += 1
        else:
            taste_e += 1

        if tmp[4] == '1.0':
            if last == '1.0':
                service_p += 1
            elif last == '0.0':
                service_n += 1
        else:
            service_e += 1

        reviews.append({'review': tmp[1].replace('<br/>', '\n'), 'taste_r': tmp[2], 'taste_pn': tmp[3], 'service_r': tmp[4], 'service_pn': last})
    return render(request, 'search/store.html', {'store_name': store_name, 'reviews': reviews, 'taste_p': taste_p, 'taste_n': taste_n, 'taste_e': taste_e, 'service_p': service_p, 'service_n': service_n, 'service_e': service_e})


def model_test(request):
    value = request.GET['value']
    fi = open('modules/input.tsv', 'w', encoding='utf-8')
    fi.write('\treview\n')
    fi.write('0\t' + value + '\n')
    fi.close()
    test_h5.Our_model('modules/input.tsv')
    fo = open('modules/output.tsv', 'r', encoding='utf-8')
    fo.readline()
    result = fo.readline().split('\t')

    return render(request, 'search/model_test.html', {'review': result[1].replace('<br/>', '\n'), 'taste_r': result[2], 'taste_pn': result[3], 'service_r': result[4], 'service_pn': result[5].replace('\n', '')})
