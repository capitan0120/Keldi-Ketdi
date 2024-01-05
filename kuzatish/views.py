from datetime import datetime, timedelta, time
from django.utils import timezone
from operator import itemgetter


from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Xodimlar, KeldiKetdi
from .forms import XodimlarForm, KeldiKetdiForm

def haftaning_boshlangichi():
    bugun = timezone.now().date()
    hafta_kunlari = ['dushanba', 'seshanba', 'chorshanba', 'payshanba', 'juma', 'shanba']
    dushanba = hafta_kunlari[0]
    k = hafta_kunlari.index(hafta_kunlari[bugun.weekday()]) - hafta_kunlari.index(dushanba)
    boshlangichi = bugun - timedelta(days=k)
    return boshlangichi

from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from .models import Xodimlar, KeldiKetdi

def calendar_data():
    xodimlar = Xodimlar.objects.all()
    calendar_data = {}

    for xodim in xodimlar:
        kelish_ketishlar = KeldiKetdi.objects.filter(
            Q(xodim=xodim) & Q(kelish_vaqti__year=2023) & Q(kelish_vaqti__month=12)
        ).order_by('kelish_vaqti')

        kelish_ketishlar_list = [kelish.kelish_vaqti for kelish in kelish_ketishlar if kelish.kelish_vaqti]

        if kelish_ketishlar_list:
            calendar_data[xodim] = kelish_ketishlar_list
    print(calendar_data)
    return calendar_data

def oylik_malumotlar(request):
    context = {
        'oylik_malumotlar': calendar_data(),
    }
    return render(request, 'example.html', context)



def xodimlar_list(request):
    xodimlar = Xodimlar.objects.all()
    # Xodimlarni va kelish vaqtlarini jadvalga joylashtiramiz
    xodimlar_va_vaqtlar = []
    bugungi_sana = datetime.now().date()
    for xodim in xodimlar:
        kelish_vaqtlar = KeldiKetdi.objects.filter(Q(xodim=xodim) & (Q(kelish_vaqti__date=bugungi_sana) | Q(kelish_vaqti__isnull=True)))
        for vaqt in kelish_vaqtlar:
            # Agar kelish_vaqti mavjud bo'lsa, uni olish
            if vaqt.kelish_vaqti:
                kelish_vaqti = timezone.localtime(vaqt.kelish_vaqti)
                xodimlar_va_vaqtlar.append({
                    'xodim': xodim,
                    'kelish_vaqti': kelish_vaqti,
                })
            else:
                # Agar kelish_vaqti mavjud emas bo'lsa, faqat xodimni qo'shamiz
                xodimlar_va_vaqtlar.append({
                    'xodim': xodim,
                    'kelish_vaqti': None,  # None bo'lishi mumkin
                })
    xodimlar_va_vaqtlar.sort(key=lambda x: x['kelish_vaqti'] if x['kelish_vaqti'] else timezone.make_aware(datetime.max, timezone.utc), reverse=True)
    return render(request, 'xodimlar.html', {
        'xodimlar_va_vaqtlar': xodimlar_va_vaqtlar,
    })

def oylik_view(request):
    sanalar = KeldiKetdi.objects.filter(kelish_vaqti__year='2023', kelish_vaqti__month='12')
    return render(request, 'oylik.html', {
        'sanalar': sanalar,
    })

def haftalik_view(request):
    xodimlar = Xodimlar.objects.all()
    bugun = timezone.now().date()
    boshlangichi = haftaning_boshlangichi()
    hafta_kunlari = ['dushanba', 'seshanba', 'chorshanba', 'payshanba', 'juma', 'shanba']

    week_dict = {}
    for xodim in xodimlar:
        week_dict[xodim] = {}
        for kun in hafta_kunlari:
            hafta_kuniga_teng_kunlar = KeldiKetdi.objects.filter(
                Q(xodim=xodim) & Q(kelish_vaqti__date=boshlangichi + timedelta(days=hafta_kunlari.index(kun))))
            if hafta_kuniga_teng_kunlar.exists():
                kelish_vaqtlari = [timezone.localtime(hafta.kelish_vaqti) for hafta in hafta_kuniga_teng_kunlar]
                week_dict[xodim][kun] = kelish_vaqtlari
            else:
                week_dict[xodim][kun] = None

    context = {
        'bugun': bugun,
        'hafta_kunlari': hafta_kunlari,
        'week_dict': week_dict,
    }
    return render(request, 'haftalik.html', context)

def haftalik_tarix(request, pk):
    xodim = Xodimlar.objects.get(pk=pk)
    one_week_ago = datetime.today() - timedelta(days=7)
    haftalik = KeldiKetdi.objects.filter(xodim__id=pk, kelish_vaqti__gte=one_week_ago)
    return render(request, 'haftalik_tarix.html', {
        'xodim': xodim,
        'haftalik': haftalik,
    })
def xodim_detail(request, pk):
    xodimlar = Xodimlar.objects.get(pk=pk)
    k_K_vaqt = KeldiKetdi.objects.filter(xodim__id=pk).values()
    return render(request, 'xodim.html', {
        'xodimlar': xodimlar,
        'k_k_vaqt': k_K_vaqt
    })

from datetime import datetime

def period_view(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        period = KeldiKetdi.objects.filter(kelish_vaqti__date__range=[start_date, end_date])
        # for i in period:
        #     print(i.xodim)

        return render(request, 'the_employee.html', {
            'periods': period,
            'start_d': start_date_str,
            'end_d': end_date_str,
        })

    return render(request, 'period.html')


def create_view(request):
    form = XodimlarForm()
    if request.method=='POST':
        form = XodimlarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('xodimlar-ruyxati')
    context = {
        'form': form,
    }
    return render(request, 'create.html', context)

def xodimlar_ruyxati(request):
    search = request.GET.get('search', '')
    if search is None:
        xodimlar_ruyxati = Xodimlar.objects.all()
    else:
        xodimlar_ruyxati = Xodimlar.objects.filter(Q(ismi__icontains=search) | Q(familiyasi__icontains=search))
    return render(request, 'xodimlar_ruyxati.html', {
        'xodimlar_ruyxati': xodimlar_ruyxati,
        'search': search,
    })


def index(request):
    return render(request, 'index.html')