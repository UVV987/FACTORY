from django.shortcuts import render
from django.template.defaulttags import register
import datetime
from django.conf import settings
import qrcode.image.svg
import qrcode
from .models import Factory, Detal
import uuid
from copy import copy


@register.filter
def get_range(l):
    return range(len(l))

def get_data(name, request, not_null_date, dt):
    if request.POST.get(name) != '' and request.POST.get(name) != None:
        t = request.POST.get(name).split('T')
        t[0] = t[0].split('-')
        t[1] = t[1].split(':')
        t[0][0] = int(t[0][0])
        t[0][1] = int(t[0][1])
        t[0][2] = int(t[0][2])
        t[1][0] = int(t[1][0])
        t[1][1] = int(t[1][1])
        dt_ = datetime.datetime(int(t[0][0]), int(t[0][1]), int(t[0][2]), int(t[1][0]), int(t[1][1]))
        if dt_ < dt:
            if (dt_ - dt).total_seconds() / 60.0 < 15: # ОПЕРАТОР "КУРИТ"
                t[1][1] = dt.timetuple()[4]
        return t, not_null_date+1
    else:
        return ([9999, 1, 1], [12, 15]) if name[0] == 's' else ([9999, 1, 2], [12, 20]), not_null_date

def forecast(start_data, start_data1):
    if start_data < start_data1:
        return start_data
    else:
        return start_data1

def finish(end_start, end_start1):
    if end_start > end_start1 or end_start1.year > 6000:
        return end_start
    else:
        return end_start1

# ЗАЛИВКА ЦВЕТАМИ
def get_met(factory):
    out_mets = ['9999', '9999', '9999', '9999', '9999']
    mets = []
    detal = Detal.objects.all().filter(factory=factory.id)

    if len(detal) != 0:
        for i in detal:
            buff = []
            buff.append(i.start_data3.strftime('%Y'))
            buff.append(i.start_data4.strftime('%Y'))
            buff.append(i.start_data5.strftime('%Y'))
            buff.append(i.start_data6.strftime('%Y'))
            buff.append(i.start_data7.strftime('%Y'))
            buff.append(i.fill3)
            buff.append(i.fill4)
            buff.append(i.fill5)
            buff.append(i.fill6)
            buff.append(i.fill7)
            mets.append(buff)


        for i in range(5):
            buff = []
            buff_2 = []
            for j in range(len(mets)):
                buff.append(int(mets[j][i]))
                buff_2.append(mets[j][i+5])

            if set(buff) == set([9999]) and set(buff_2) == set([False]):
                out_mets[i] = '9999'
            else:
                out_mets[i] = '1'

    return out_mets[0], out_mets[1], out_mets[2], out_mets[3], out_mets[4]

def calculated_bar(dt, start, end, end_, fill=False):
    if fill:
        bar = 100
    else:
        if start > dt:
            bar = 0
        elif end > dt:
            bar = 100 - ((end-dt).total_seconds()/(end-start).total_seconds())*100
        else:
            bar = 100

        time_from_start = (dt-start).total_seconds()/60.0
        time_all = (end-start).total_seconds()/60.0
        if end_ != '':
            time_all = time_all*float(end_)-(start-datetime.datetime(1, 1, 1, 0, 0, 0)).total_seconds()/60.0
        time_from_start_otk = time_from_start-time_all

        time_from_start_otk_part = time_from_start_otk/20*100

        if time_from_start_otk_part > 0:
            if time_from_start_otk_part > 100:
                bar = 100
            else:
                bar = time_from_start_otk_part

    return bar

def calculated_bar_2(factory, dt):
    out_bars = [0, 0, 0, 0, 0]
    bars = []
    detal = Detal.objects.all().filter(factory=factory.id)

    if len(detal) != 0:
        for i in detal:
            buff = []
            buff.append(calculated_bar(dt, i.start_data3.replace(tzinfo=None), i.end_start3.replace(tzinfo=None), i.end3, i.fill3) if i.otk3[-7:] != 'back 1|' else 0)
            buff.append(calculated_bar(dt, i.start_data4.replace(tzinfo=None), i.end_start4.replace(tzinfo=None), i.end4, i.fill4) if i.otk4[-7:] != 'back 1|' else 0)
            buff.append(calculated_bar(dt, i.start_data5.replace(tzinfo=None), i.end_start5.replace(tzinfo=None), i.end5, i.fill5) if i.otk5[-7:] != 'back 1|' else 0)
            buff.append(calculated_bar(dt, i.start_data6.replace(tzinfo=None), i.end_start6.replace(tzinfo=None), i.end6, i.fill6) if i.otk6[-7:] != 'back 1|' else 0)
            buff.append(calculated_bar(dt, i.start_data7.replace(tzinfo=None), i.end_start7.replace(tzinfo=None), i.end7, i.fill7) if i.otk7[-7:] != 'back 1|' else 0)
            buff.append(i.start_data3.strftime('%Y'))
            buff.append(i.start_data4.strftime('%Y'))
            buff.append(i.start_data5.strftime('%Y'))
            buff.append(i.start_data6.strftime('%Y'))
            buff.append(i.start_data7.strftime('%Y'))
            buff.append(i.fill3)
            buff.append(i.fill4)
            buff.append(i.fill5)
            buff.append(i.fill6)
            buff.append(i.fill7)
            bars.append(buff)

        for i in range(5):
            buff = 0
            counter = 0
            for j in range(len(bars)):
                buff += bars[j][i]
                if bars[j][i+5] != '9999' or bars[j][i+10]:
                    counter += 1

            if counter != 0:
                out_bars[i] = buff/counter
            else:
                out_bars[i] = buff

    return out_bars

def give_color(history, start_data, end_data, dt, otk, end):
    time_from_start = (dt-start_data).total_seconds()/60.0 
    time_all = (end_data-start_data).total_seconds()/60.0
    if end != '':
        time_all = time_all*float(end)-(start_data-datetime.datetime(1, 1, 1, 0, 0, 0)).total_seconds()/60.0
    time_from_start_otk = time_from_start-time_all
    time_all_otk = 20

    if time_from_start > time_all:
        time_from_start = time_all

    if time_from_start_otk > time_all_otk:
        time_from_start_otk = time_all_otk

    colors = []

    if time_from_start == time_all:
        otk = otk.split('|')[:-1]
        for i in range(len(otk)):
            otk[i] = otk[i].split()
            otk[i][1] = float(otk[i][1])

        if len(otk) != 0 and otk[-1][0] == 'back':
            colors.append(['red', 100])
        elif len(otk) == 0:
            colors.append(['gray', time_from_start_otk/time_all_otk*100])
        elif len(otk) == 1:
            if otk[0][1]*time_all_otk < 5:
                colors.append(['green', time_from_start_otk/time_all_otk*100])
            else:
                colors.append(['gray', (otk[0][1]*time_all_otk)/time_all_otk*100])
                colors.append(['green', (time_from_start_otk-otk[0][1]*time_all_otk)/time_all_otk*100])
        else:
            length = 0
            if otk[0][1]*time_all_otk > 5:
                colors.append(['gray', (otk[0][1]*time_all_otk)/time_all_otk*100])
                length = otk[0][1]*time_all_otk
            else:
                colors.append(['green', (otk[0][1]*time_all_otk)/time_all_otk*100])
                length = otk[0][1]*time_all_otk

            buff = 'green'
            i = 1
            while i < len(otk):
                colors.append([buff, (otk[i][1]*time_all_otk-length)/time_all_otk*100])
                length = otk[i][1]*time_all_otk

                if buff == 'green':
                    buff = 'red'
                else:
                    buff = 'green'

                i += 1

            colors.append([buff, (time_from_start_otk-length)/time_all_otk*100])
    else:
        history = history.split('|')[:-1]
        for i in range(len(history)):
            history[i] = history[i].split()
            history[i][1] = float(history[i][1])

        if len(history) == 0:
            colors.append(['gray', time_from_start/time_all*100])
        elif len(history) == 1:
            if history[0][1]*time_all < 5:
                colors.append(['green', time_from_start/time_all*100])
            else:
                colors.append(['gray', (history[0][1]*time_all)/time_all*100])
                colors.append(['green', (time_from_start-history[0][1]*time_all)/time_all*100])
        else:
            length = 0
            if history[0][1]*time_all > 5:
                colors.append(['gray', (history[0][1]*time_all)/time_all*100])
                length = history[0][1]*time_all
            else:
                colors.append(['green', (history[0][1]*time_all)/time_all*100])
                length = history[0][1]*time_all

            buff = 'green'
            i = 1
            while i < len(history):
                colors.append([buff, (history[i][1]*time_all-length)/time_all*100])
                length = history[i][1]*time_all

                if buff == 'green':
                    buff = 'red'
                else:
                    buff = 'green'

                i += 1

            colors.append([buff, (time_from_start-length)/time_all*100])

    for i in range(len(colors)):
        colors[i][1] = str(colors[i][1])

    return colors

def give_color_2(factory, dt):
    out_colors = [[], [], [], [], []]
    colors = []
    detal = Detal.objects.all().filter(factory=factory.id)

    if len(detal) != 0:
        for i in detal:
            buff = []
            buff.append([['green', '100.0']] if i.fill3 else give_color(i.history3, i.start_data3.replace(tzinfo=None), i.end_start3.replace(tzinfo=None), dt, i.otk3, i.end3))
            buff.append([['green', '100.0']] if i.fill4 else give_color(i.history4, i.start_data4.replace(tzinfo=None), i.end_start4.replace(tzinfo=None), dt, i.otk4, i.end4))
            buff.append([['green', '100.0']] if i.fill5 else give_color(i.history5, i.start_data5.replace(tzinfo=None), i.end_start5.replace(tzinfo=None), dt, i.otk5, i.end5))
            buff.append([['green', '100.0']] if i.fill6 else give_color(i.history6, i.start_data6.replace(tzinfo=None), i.end_start6.replace(tzinfo=None), dt, i.otk6, i.end6))
            buff.append([['green', '100.0']] if i.fill7 else give_color(i.history7, i.start_data7.replace(tzinfo=None), i.end_start7.replace(tzinfo=None), dt, i.otk7, i.end7))
            colors.append(buff)

        for i in range(len(colors)):
            buff = []
            for j in colors[i]:
                buff_ = []
                for o in j:
                    if float(o[1]) > 0:
                        for _ in range(int(str(o[1])[:str(o[1]).find(".")])):
                            buff_.append(o[0])
                for _ in range(100-len(buff_)):
                    buff_.append('')
                if len(buff_) == 0:
                    buff_ = ['']*100
                buff.append(copy(buff_))
            colors[i] = copy(buff)

        for i in range(5):
            for j in range(100):
                color = ''
                for o in range(len(colors)):
                    if colors[o][i][j] == 'gray':
                        color = 'gray'
                    elif colors[o][i][j] == 'green' and color == '':
                        color = 'green'
                    elif colors[o][i][j] == 'red':
                        color = 'red'
                        break

                out_colors[i].append([color, 1])

    return out_colors[0], out_colors[1], out_colors[2], out_colors[3], out_colors[4]

def give_bg_color(start_data, end_data, dt):
    time_from_start = (dt-start_data).total_seconds()/60.0
    time_all = (end_data-start_data).total_seconds()/60.0

    if time_from_start > time_all:
        return 'blue'
    else:
        return 'white'

def give_bg_color_2(factory, dt):
    out_colors = ['', '', '', '', '']
    colors = []
    detal = Detal.objects.all().filter(factory=factory.id)

    if len(detal) != 0:
        for i in detal:
            buff = []
            buff.append(give_bg_color(i.start_data3.replace(tzinfo=None), i.end_start3.replace(tzinfo=None), dt))
            buff.append(give_bg_color(i.start_data4.replace(tzinfo=None), i.end_start4.replace(tzinfo=None), dt))
            buff.append(give_bg_color(i.start_data5.replace(tzinfo=None), i.end_start5.replace(tzinfo=None), dt))
            buff.append(give_bg_color(i.start_data6.replace(tzinfo=None), i.end_start6.replace(tzinfo=None), dt))
            buff.append(give_bg_color(i.start_data7.replace(tzinfo=None), i.end_start7.replace(tzinfo=None), dt))
            colors.append(buff)

        for i in range(5):
            color = 'blue'
            for j in range(len(colors)):
                if colors[j][i] == 'white':
                    color = 'white'

            out_colors[i] = color

    return out_colors[0], out_colors[1], out_colors[2], out_colors[3], out_colors[4]


def operator(request):
    error = False
    dt = datetime.datetime.now()

    if request.method == 'POST':
        not_null_date = -2
        start_data, not_null_date = get_data('start_data', request, not_null_date, dt)
        end_data, not_null_date = get_data('end_start', request, not_null_date, dt)
        start_data1, not_null_date = get_data('start_data1', request, not_null_date, dt)
        end_data1, not_null_date = get_data('end_start1', request, not_null_date, dt)
        start_data2, not_null_date = get_data('start_data2', request, not_null_date, dt)
        end_data2, not_null_date = get_data('end_start2', request, not_null_date, dt)

        if start_data > end_data or start_data1 > end_data1 or start_data2 > end_data2:
            error = True
        elif not_null_date <= 0 and request.POST.get('fill1') != 'on' and request.POST.get('fill2') != 'on':
            error = True
        else:
            try:
                f = Factory()
                f.name = request.POST.get('name')
                f.order_number = request.POST.get('order_number')
                f.contract = request.POST.get('contract')
                f.weight = request.POST.get('weight')
                f.unit = request.POST.get('unit')
                f.start_data = datetime.datetime(int(start_data[0][0]), int(start_data[0][1]), int(start_data[0][2]), int(start_data[1][0]), int(start_data[1][1])) # день, месяц, год
                f.end_start = datetime.datetime(int(end_data[0][0]), int(end_data[0][1]), int(end_data[0][2]), int(end_data[1][0]), int(end_data[1][1]))
                f.start_data1 = datetime.datetime(int(start_data1[0][0]), int(start_data1[0][1]), int(start_data1[0][2]), int(start_data1[1][0]), int(start_data1[1][1]))
                f.end_start1 = datetime.datetime(int(end_data1[0][0]), int(end_data1[0][1]), int(end_data1[0][2]), int(end_data1[1][0]), int(end_data1[1][1]))
                f.start_data2 = datetime.datetime(int(start_data2[0][0]), int(start_data2[0][1]), int(start_data2[0][2]), int(start_data2[1][0]), int(start_data2[1][1]))
                f.end_start2 = datetime.datetime(int(end_data2[0][0]), int(end_data2[0][1]), int(end_data2[0][2]), int(end_data2[1][0]), int(end_data2[1][1]))
                f.fill1 = True if request.POST.get('fill1') == 'on' else False
                f.fill2 = True if request.POST.get('fill2') == 'on' else False
                f.save()
                qr_info = f'{f.id}\n{request.POST.get("order_number")}\n{request.POST.get("name")}\n{request.POST.get("contract")}'
                qr_name = f'{settings.MEDIA_ROOT}/{uuid.uuid4()}.svg'
                qr = qrcode.make(qr_info, image_factory=qrcode.image.svg.SvgImage)
                qr.save(qr_name)
                f.qr = qr_name
                f.save()
            except:
                error = True

    objects = []
    for i in Factory.objects.all().order_by('-id'):
        old = finish(i.end_start, i.end_start1)
        old = finish(old, i.end_start2)
        old = old.replace(tzinfo=None)
        object = dict()
        object['qr'] = i.qr
        object['met'] = i.start_data.strftime('%Y')
        object['met1'] = i.start_data1.strftime('%Y')
        object['met2'] = i.start_data2.strftime('%Y')
        object['met3'], object['met4'], object['met5'], object['met6'], object['met7'] = get_met(i)
        object['id'] = i.id
        object['name'] = i.name
        object['old'] = old.strftime("%d.%m.%Y")
        object['order_number'] = i.order_number
        object['contract'] = i.contract
        object['weight'] = i.weight
        object['weight_total'] = i.weight * i.unit
        object['unit'] = i.unit
        object['start_data'] = i.start_data.strftime("%d.%m.%Y")
        object['end_start'] = i.end_start.strftime("%d.%m.%Y")
        object['start_data1'] = i.start_data1
        object['end_start1'] = i.end_start1
        object['start_data2'] = i.start_data2
        object['end_start2'] = i.end_start2
        object['fill1'] = i.fill1
        object['fill2'] = i.fill2

        i.start_data1 = i.start_data1.replace(tzinfo=None)
        i.end_start1 = i.end_start1.replace(tzinfo=None)
        i.start_data2 = i.start_data2.replace(tzinfo=None)
        i.end_start2 = i.end_start2.replace(tzinfo=None)
        # КОНТРОЛЬ ПРИЁМА ЗАКАЗА ЦВЕТАМИ
        object['color1'] = [['green', 100]] if i.fill1 else give_color(i.history1, i.start_data1, i.end_start1, dt, i.otk1, i.end1)
        object['color2'] = [['green', 100]] if i.fill2 else give_color(i.history2, i.start_data2, i.end_start2, dt, i.otk2, i.end2)
        object['color3'], object['color4'], object['color5'], object['color6'], object['color7'] = give_color_2(i, dt)

        object['color1_'] = give_bg_color(i.start_data1, i.end_start1, dt)
        object['color2_'] = give_bg_color(i.start_data2, i.end_start2, dt)
        object['color3_'], object['color4_'], object['color5_'], object['color6_'], object['color7_'] = give_bg_color_2(i, dt)

        object['meter'] = []
        object['meter'].append(calculated_bar(dt, i.start_data1, i.end_start1, i.end1, i.fill1) if i.otk1[-7:] != 'back 1|' else 0)
        object['meter'].append(calculated_bar(dt, i.start_data2, i.end_start2, i.end2, i.fill2) if i.otk2[-7:] != 'back 1|' else 0)
        object['meter'] += calculated_bar_2(i, dt)

        for i in range(len(object['meter'])):
            object['meter'][i] = f'{round(object["meter"][i])}%'

        objects.append(object)

    return render(request, 'users/operator.html', {'title': 'Оператор', 'objects': objects, 'error': error})


def detal(request, id):
    error = False
    dt = datetime.datetime.now()
    factory = Factory.objects.all().filter(id=id)[0]

    # СОЗДАЕМ ПРОГНОЗ ПРОИЗВОДСТВА ПО ДНЯМ
    start = forecast(factory.start_data, factory.start_data1)
    start = forecast(start, factory.start_data2)
    start = start.replace(tzinfo=None)

    old = finish(factory.end_start, factory.end_start1)
    old = finish(old, factory.end_start2)
    old = old.replace(tzinfo=None)

    if request.method == 'POST':
        not_null_date = -2
        start_data, not_null_date = get_data('start_data', request, not_null_date, dt) #это центральная дата, её вносим всегда
        end_data, not_null_date = get_data('end_start', request, not_null_date, dt) #это центральная дата, её вносим всегда
        start_data3, not_null_date = get_data('start_data3', request, not_null_date, dt)
        end_data3, not_null_date = get_data('end_start3', request, not_null_date, dt)
        start_data4, not_null_date = get_data('start_data4', request, not_null_date, dt)
        end_data4, not_null_date = get_data('end_start4', request, not_null_date, dt)
        start_data5, not_null_date = get_data('start_data5', request, not_null_date, dt)
        end_data5, not_null_date = get_data('end_start5', request, not_null_date, dt)
        start_data6, not_null_date = get_data('start_data6', request, not_null_date, dt)
        end_data6, not_null_date = get_data('end_start6', request, not_null_date, dt)
        start_data7, not_null_date = get_data('start_data7', request, not_null_date, dt)
        end_data7, not_null_date = get_data('end_start7', request, not_null_date, dt)

        if start_data > end_data or start_data3 > end_data3 or start_data4 > end_data4 or start_data5 > end_data5 or start_data6 > end_data6 or start_data7 > end_data7:
            error = True
        elif not_null_date <= 0  and request.POST.get('fill3') != 'on' and request.POST.get('fill4') != 'on' and request.POST.get('fill5') != 'on' and request.POST.get('fill6') != 'on' and request.POST.get('fill7') != 'on':
            error = True
        else:
            try:
                f = Detal()
                f.factory = Factory.objects.all().filter(id=id)[0]
                f.name = request.POST.get('name')
                f.order_number = request.POST.get('order_number')
                f.weight = request.POST.get('weight')
                f.unit = request.POST.get('unit')
                f.start_data = datetime.datetime(int(start_data[0][0]), int(start_data[0][1]), int(start_data[0][2]), int(start_data[1][0]), int(start_data[1][1])) # день, месяц, год
                f.end_start = datetime.datetime(int(end_data[0][0]), int(end_data[0][1]), int(end_data[0][2]), int(end_data[1][0]), int(end_data[1][1]))
                f.start_data3 = datetime.datetime(int(start_data3[0][0]), int(start_data3[0][1]), int(start_data3[0][2]), int(start_data3[1][0]), int(start_data3[1][1]))
                f.end_start3 = datetime.datetime(int(end_data3[0][0]), int(end_data3[0][1]), int(end_data3[0][2]), int(end_data3[1][0]), int(end_data3[1][1]))
                f.start_data4 = datetime.datetime(int(start_data4[0][0]), int(start_data4[0][1]), int(start_data4[0][2]), int(start_data4[1][0]), int(start_data4[1][1]))
                f.end_start4 = datetime.datetime(int(end_data4[0][0]), int(end_data4[0][1]), int(end_data4[0][2]), int(end_data4[1][0]), int(end_data4[1][1]))
                f.start_data5 = datetime.datetime(int(start_data5[0][0]), int(start_data5[0][1]), int(start_data5[0][2]), int(start_data5[1][0]), int(start_data5[1][1]))
                f.end_start5 = datetime.datetime(int(end_data5[0][0]), int(end_data5[0][1]), int(end_data5[0][2]), int(end_data5[1][0]), int(end_data5[1][1]))
                f.start_data6 = datetime.datetime(int(start_data6[0][0]), int(start_data6[0][1]), int(start_data6[0][2]), int(start_data6[1][0]), int(start_data6[1][1]))
                f.end_start6 = datetime.datetime(int(end_data6[0][0]), int(end_data6[0][1]), int(end_data6[0][2]), int(end_data6[1][0]), int(end_data6[1][1]))
                f.start_data7 = datetime.datetime(int(start_data7[0][0]), int(start_data7[0][1]), int(start_data7[0][2]), int(start_data7[1][0]), int(start_data7[1][1]))
                f.end_start7 = datetime.datetime(int(end_data7[0][0]), int(end_data7[0][1]), int(end_data7[0][2]), int(end_data7[1][0]), int(end_data7[1][1]))
                f.fill3 = True if request.POST.get('fill3') == 'on' else False
                f.fill4 = True if request.POST.get('fill4') == 'on' else False
                f.fill5 = True if request.POST.get('fill5') == 'on' else False
                f.fill6 = True if request.POST.get('fill6') == 'on' else False
                f.fill7 = True if request.POST.get('fill7') == 'on' else False
                f.save()
                qr_info = f'{f.id}\n{request.POST.get("order_number")}\n{request.POST.get("name")}'
                qr_name = f'{settings.MEDIA_ROOT}/{uuid.uuid4()}.svg'
                qr = qrcode.make(qr_info, image_factory=qrcode.image.svg.SvgImage)
                qr.save(qr_name)
                f.qr = qr_name
                f.save()
            except:
                error = True

    objects = []
    for i in Detal.objects.all().filter(factory=id).order_by('-id'):
        object = dict()
        object['qr'] = i.qr
        object['met'] = i.start_data.strftime('%Y')
        object['met3'] = i.start_data3.strftime('%Y')
        object['met4'] = i.start_data4.strftime('%Y')
        object['met5'] = i.start_data5.strftime('%Y')
        object['met6'] = i.start_data6.strftime('%Y')
        object['met7'] = i.start_data7.strftime('%Y')
        object['id'] = i.id
        object['name'] = i.name
        object['order_number'] = i.order_number
        object['old'] = old.strftime("%d.%m.%Y") # ВЫВОДИМ ДАТУ ПРОГНОЗ ОТГРУЗКИ
        object['weight'] = i.weight
        object['weight_total'] = i.weight * i.unit
        object['unit'] = i.unit
        object['start_data'] = i.start_data.strftime("%d.%m.%Y")
        object['end_start'] = i.end_start.strftime("%d.%m.%Y")
        object['start_data3'] = i.start_data3
        object['end_start3'] = i.end_start3
        object['start_data4'] = i.start_data4
        object['end_start4'] = i.end_start4
        object['start_data5'] = i.start_data5
        object['end_start5'] = i.end_start5
        object['start_data6'] = i.start_data6
        object['end_start6'] = i.end_start6
        object['start_data7'] = i.start_data7
        object['end_start7'] = i.end_start7
        object['fill3'] = i.fill3
        object['fill4'] = i.fill4
        object['fill5'] = i.fill5
        object['fill6'] = i.fill6
        object['fill7'] = i.fill7

        i.start_data3 = i.start_data3.replace(tzinfo=None)
        i.end_start3 = i.end_start3.replace(tzinfo=None)
        i.start_data4 = i.start_data4.replace(tzinfo=None)
        i.end_start4 = i.end_start4.replace(tzinfo=None)
        i.start_data5 = i.start_data5.replace(tzinfo=None)
        i.end_start5 = i.end_start5.replace(tzinfo=None)
        i.start_data6 = i.start_data6.replace(tzinfo=None)
        i.end_start6 = i.end_start6.replace(tzinfo=None)
        i.start_data7 = i.start_data7.replace(tzinfo=None)
        i.end_start7 = i.end_start7.replace(tzinfo=None)

        # КОНТРОЛЬ ПРИЁМА ЗАКАЗА ЦВЕТАМИ
        object['color3'] = [['green', 100]] if i.fill3 else give_color(i.history3, i.start_data3, i.end_start3, dt, i.otk3, i.end3)
        object['color4'] = [['green', 100]] if i.fill4 else give_color(i.history4, i.start_data4, i.end_start4, dt, i.otk4, i.end4)
        object['color5'] = [['green', 100]] if i.fill5 else give_color(i.history5, i.start_data5, i.end_start5, dt, i.otk5, i.end5)
        object['color6'] = [['green', 100]] if i.fill6 else give_color(i.history6, i.start_data6, i.end_start6, dt, i.otk6, i.end6)
        object['color7'] = [['green', 100]] if i.fill7 else give_color(i.history7, i.start_data7, i.end_start7, dt, i.otk7, i.end7)
        object['color3_'] = give_bg_color(i.start_data3, i.end_start3, dt)
        object['color4_'] = give_bg_color(i.start_data4, i.end_start4, dt)
        object['color5_'] = give_bg_color(i.start_data5, i.end_start5, dt)
        object['color6_'] = give_bg_color(i.start_data6, i.end_start6, dt)
        object['color7_'] = give_bg_color(i.start_data7, i.end_start7, dt)

        object['meter'] = []
        object['meter'].append(calculated_bar(dt, i.start_data3, i.end_start3, i.end3, i.fill3) if i.otk3[-7:] != 'back 1|' else 0)
        object['meter'].append(calculated_bar(dt, i.start_data4, i.end_start4, i.end4, i.fill4) if i.otk4[-7:] != 'back 1|' else 0)
        object['meter'].append(calculated_bar(dt, i.start_data5, i.end_start5, i.end5, i.fill5) if i.otk5[-7:] != 'back 1|' else 0)
        object['meter'].append(calculated_bar(dt, i.start_data6, i.end_start6, i.end6, i.fill6) if i.otk6[-7:] != 'back 1|' else 0)
        object['meter'].append(calculated_bar(dt, i.start_data7, i.end_start7, i.end7, i.fill7) if i.otk7[-7:] != 'back 1|' else 0)

        for i in range(len(object['meter'])):
            object['meter'][i] = round(object['meter'][i]) # PROGRESSBAR

        objects.append(object)

    return render(request, 'users/detal.html', {'title': 'Оператор', 'objects': objects, 'id': id, 'error': error})


def about(request):
    dt = datetime.datetime.now()

    objects = []
    for i in Factory.objects.all().order_by('-id'):
        old = finish(i.end_start, i.end_start1)
        old = finish(old, i.end_start2)

        for j in Detal.objects.all().filter(factory=i.id):
            old = finish(old, j.end_start)
            old = finish(old, j.end_start3)
            old = finish(old, j.end_start4)
            old = finish(old, j.end_start5)
            old = finish(old, j.end_start6)
            old = finish(old, j.end_start7)

        old = old.replace(tzinfo=None) # СОЗДАЕМ ПРОГНОЗ ПРОИЗВОДСТВА КОНЕЧНАЯ ДАТА
        object = dict()
        object['qr'] = i.qr
        object['met'] = i.start_data.strftime('%Y')
        object['met1'] = i.start_data1.strftime('%Y')
        object['met2'] = i.start_data2.strftime('%Y')
        object['met3'], object['met4'], object['met5'], object['met6'], object['met7'] = get_met(i)
        object['id'] = i.id
        object['name'] = i.name
        object['old'] = old.strftime("%d.%m.%Y")
        object['order_number'] = i.order_number
        object['contract'] = i.contract
        object['weight'] = i.weight
        object['weight_total'] = i.weight * i.unit
        object['unit'] = i.unit
        object['start_data'] = i.start_data.strftime("%d.%m.%Y")
        object['end_start'] = i.end_start.strftime("%d.%m.%Y")
        object['start_data1'] = i.start_data1
        object['end_start1'] = i.end_start1
        object['start_data2'] = i.start_data2
        object['end_start2'] = i.end_start2
        object['fill1'] = i.fill1
        object['fill2'] = i.fill2

        i.start_data1 = i.start_data1.replace(tzinfo=None)
        i.end_start1 = i.end_start1.replace(tzinfo=None)
        i.start_data2 = i.start_data2.replace(tzinfo=None)
        i.end_start2 = i.end_start2.replace(tzinfo=None)
        # КОНТРОЛЬ ПРИЁМА ЗАКАЗА ЦВЕТАМИ
        object['color1'] = [['green', 100]] if i.fill1 else give_color(i.history1, i.start_data1, i.end_start1, dt, i.otk1, i.end1)
        object['color2'] = [['green', 100]] if i.fill2 else give_color(i.history2, i.start_data2, i.end_start2, dt, i.otk2, i.end2)
        object['color3'], object['color4'], object['color5'], object['color6'], object['color7'] = give_color_2(i, dt)

        object['color1_'] = give_bg_color(i.start_data1, i.end_start1, dt)
        object['color2_'] = give_bg_color(i.start_data2, i.end_start2, dt)
        object['color3_'], object['color4_'], object['color5_'], object['color6_'], object['color7_'] = give_bg_color_2(i, dt)

        object['meter'] = []
        object['meter'].append(calculated_bar(dt, i.start_data1, i.end_start1, i.end1, i.fill1) if i.otk1[-7:] != 'back 1|' else 0)
        object['meter'].append(calculated_bar(dt, i.start_data2, i.end_start2, i.end2, i.fill2) if i.otk2[-7:] != 'back 1|' else 0)
        object['meter'] += calculated_bar_2(i, dt)

        for i in range(len(object['meter'])):
            object['meter'][i] = round(object['meter'][i]) # PROGRESSBAR

        objects.append(object)

    return render(request, 'users/about.html', {'objects': objects})


def abouttoo(request, id):
    dt = datetime.datetime.now()

 # СОЗДАЕМ ПЛАН ПРОИЗВОДСТВА ПО ДНЯМ
    factory = Factory.objects.all().filter(id=id)[0] # Получаем Factory по id и считаем для него прогрессбар
    top1 = (factory.end_start.replace(tzinfo=None)-factory.start_data.replace(tzinfo=None)).days
 # СОЗДАЕМ ПРОГНОЗ ПРОИЗВОДСТВА ПО ДНЯМ
    start = forecast(factory.start_data, factory.start_data1)
    start = forecast(start, factory.start_data2)

    old = finish(factory.end_start, factory.end_start1)
    old = finish(old, factory.end_start2)

    objects = []
    for i in Detal.objects.all().filter(factory=id):
        object = dict()
        object['met'] = i.start_data.strftime('%Y')
        object['met3'] = i.start_data3.strftime('%Y')
        object['met4'] = i.start_data4.strftime('%Y')
        object['met5'] = i.start_data5.strftime('%Y')
        object['met6'] = i.start_data6.strftime('%Y')
        object['met7'] = i.start_data7.strftime('%Y')
        object['id'] = i.id
        object['name'] = i.name
        object['order_number'] = i.order_number
        object['old'] = old.strftime("%d.%m.%Y")
        object['weight'] = i.weight
        object['weight_total'] = i.weight * i.unit
        object['unit'] = i.unit
        object['start_data'] = i.start_data.strftime("%d.%m.%Y")
        object['end_start'] = i.end_start.strftime("%d.%m.%Y")
        object['start_data3'] = i.start_data3
        object['end_start3'] = i.end_start3
        object['start_data4'] = i.start_data4
        object['end_start4'] = i.end_start4
        object['start_data5'] = i.start_data5
        object['end_start5'] = i.end_start5
        object['start_data6'] = i.start_data6
        object['end_start6'] = i.end_start6
        object['start_data7'] = i.start_data7
        object['end_start7'] = i.end_start7
        object['fill3'] = i.fill3
        object['fill4'] = i.fill4
        object['fill5'] = i.fill5
        object['fill6'] = i.fill6
        object['fill7'] = i.fill7

        start = forecast(start, i.start_data)
        start = forecast(start, i.start_data3)
        start = forecast(start, i.start_data4)
        start = forecast(start, i.start_data5)
        start = forecast(start, i.start_data6)
        start = forecast(start, i.start_data7)

        old = finish(old, i.end_start)
        old = finish(old, i.end_start3)
        old = finish(old, i.end_start4)
        old = finish(old, i.end_start5)
        old = finish(old, i.end_start6)
        old = finish(old, i.end_start7)

        i.start_data3 = i.start_data3.replace(tzinfo=None)
        i.end_start3 = i.end_start3.replace(tzinfo=None)
        i.start_data4 = i.start_data4.replace(tzinfo=None)
        i.end_start4 = i.end_start4.replace(tzinfo=None)
        i.start_data5 = i.start_data5.replace(tzinfo=None)
        i.end_start5 = i.end_start5.replace(tzinfo=None)
        i.start_data6 = i.start_data6.replace(tzinfo=None)
        i.end_start6 = i.end_start6.replace(tzinfo=None)
        i.start_data7 = i.start_data7.replace(tzinfo=None)
        i.end_start7 = i.end_start7.replace(tzinfo=None)

        # КОНТРОЛЬ ПРИЁМА ЗАКАЗА ЦВЕТАМИ
        object['color3'] = [['green', 100]] if i.fill3 else give_color(i.history3, i.start_data3, i.end_start3, dt, i.otk3, i.end3)
        object['color4'] = [['green', 100]] if i.fill4 else give_color(i.history4, i.start_data4, i.end_start4, dt, i.otk4, i.end4)
        object['color5'] = [['green', 100]] if i.fill5 else give_color(i.history5, i.start_data5, i.end_start5, dt, i.otk5, i.end5)
        object['color6'] = [['green', 100]] if i.fill6 else give_color(i.history6, i.start_data6, i.end_start6, dt, i.otk6, i.end6)
        object['color7'] = [['green', 100]] if i.fill7 else give_color(i.history7, i.start_data7, i.end_start7, dt, i.otk7, i.end7)
        object['color3_'] = give_bg_color(i.start_data3, i.end_start3, dt)
        object['color4_'] = give_bg_color(i.start_data4, i.end_start4, dt)
        object['color5_'] = give_bg_color(i.start_data5, i.end_start5, dt)
        object['color6_'] = give_bg_color(i.start_data6, i.end_start6, dt)
        object['color7_'] = give_bg_color(i.start_data7, i.end_start7, dt)

        object['meter'] = []
        object['meter'].append(calculated_bar(dt, i.start_data3, i.end_start3, i.end3, i.fill3) if i.otk3[-7:] != 'back 1|' else 0)
        object['meter'].append(calculated_bar(dt, i.start_data4, i.end_start4, i.end4, i.fill4) if i.otk4[-7:] != 'back 1|' else 0)
        object['meter'].append(calculated_bar(dt, i.start_data5, i.end_start5, i.end5, i.fill5) if i.otk5[-7:] != 'back 1|' else 0)
        object['meter'].append(calculated_bar(dt, i.start_data6, i.end_start6, i.end6, i.fill6) if i.otk6[-7:] != 'back 1|' else 0)
        object['meter'].append(calculated_bar(dt, i.start_data7, i.end_start7, i.end7, i.fill7) if i.otk7[-7:] != 'back 1|' else 0)

        for i in range(len(object['meter'])):
            object['meter'][i] = round(object['meter'][i]) # PROGRESSBAR

        objects.append(object)

    start = start.replace(tzinfo=None)
    old = old.replace(tzinfo=None)
    top2 = (old-start).days # ПРОГНОЗ ПРОИЗВОДСТВА В ДНЯХ
    try:
        top = (top1/top2)*150
    except:
        top = 100
    top3 = 100 - ((old-dt).total_seconds()/(old-start).total_seconds())*100 # ФАКТ ПРОИЗВОДСТВА

    return render(request, 'users/abouttoo.html', {'objects': objects, 'id': id, 'top': top, 'top1': top1, 'top2': top2, 'top3': top3})


def pin(request, id):
    error = False
    detail = Detal.objects.all().filter(id=id)[0]
    factory = Factory.objects.all().filter(id=detail.factory.id)[0]

    # СОЗДАЕМ ПРОГНОЗ ПРОИЗВОДСТВА ПО ДНЯМ
    start = forecast(factory.start_data, factory.start_data1)
    start = forecast(start, factory.start_data2)
    start = forecast(start, factory.start_data3)
    start = forecast(start, factory.start_data4)
    start = forecast(start, factory.start_data5)
    start = forecast(start, factory.start_data6)
    start = forecast(start, factory.start_data7)

    old = finish(factory.end_start, factory.end_start1)
    old = finish(old, factory.end_start2)
    old = finish(old, factory.end_start3)
    old = finish(old, factory.end_start4)
    old = finish(old, factory.end_start5)
    old = finish(old, factory.end_start6)
    old = finish(old, factory.end_start7)

    dt = datetime.datetime.now()

    objects = []
    object = dict()
    object['id'] = detail.id
    object['name'] = detail.name
    object['order_number'] = detail.order_number
    object['weight'] = detail.weight
    object['weight_total'] = detail.weight * detail.unit
    object['unit'] = detail.unit
    object['start_data'] = detail.start_data.strftime("%d.%m.%Y")
    object['end_start'] = detail.end_start.strftime("%d.%m.%Y")
    object['start_data1'] = detail.start_data1
    object['end_start1'] = detail.end_start1
    object['start_data2'] = detail.start_data2
    object['end_start2'] = detail.end_start2
    object['start_data3'] = detail.start_data3
    object['end_start3'] = detail.end_start3
    object['start_data4'] = detail.start_data4
    object['end_start4'] = detail.end_start4
    object['start_data5'] = detail.start_data5
    object['end_start5'] = detail.end_start5
    object['start_data6'] = detail.start_data6
    object['end_start6'] = detail.end_start6
    object['start_data7'] = detail.start_data7
    object['end_start7'] = detail.end_start7

    start = forecast(start, detail.start_data)
    start = forecast(start, detail.start_data1)
    start = forecast(start, detail.start_data2)
    start = forecast(start, detail.start_data3)
    start = forecast(start, detail.start_data4)
    start = forecast(start, detail.start_data5)
    start = forecast(start, detail.start_data6)
    start = forecast(start, detail.start_data7)

    old = finish(old, detail.end_start)
    old = finish(old, detail.end_start1)
    old = finish(old, detail.end_start2)
    old = finish(old, detail.end_start3)
    old = finish(old, detail.end_start4)
    old = finish(old, detail.end_start5)
    old = finish(old, detail.end_start6)
    old = finish(old, detail.end_start7)

    object['meter'] = []
    object['meter'].append(calculated_bar(dt, detail.start_data1.replace(tzinfo=None), detail.end_start1.replace(tzinfo=None), i.end1))
    object['meter'].append(calculated_bar(dt, detail.start_data2.replace(tzinfo=None), detail.end_start2.replace(tzinfo=None), i.end2))
    object['meter'].append(calculated_bar(dt, detail.start_data3.replace(tzinfo=None), detail.end_start3.replace(tzinfo=None), i.end3))
    object['meter'].append(calculated_bar(dt, detail.start_data4.replace(tzinfo=None), detail.end_start4.replace(tzinfo=None), i.end4))
    object['meter'].append(calculated_bar(dt, detail.start_data5.replace(tzinfo=None), detail.end_start5.replace(tzinfo=None), i.end5))
    object['meter'].append(calculated_bar(dt, detail.start_data6.replace(tzinfo=None), detail.end_start6.replace(tzinfo=None), i.end6))
    object['meter'].append(calculated_bar(dt, detail.start_data7.replace(tzinfo=None), detail.end_start7.replace(tzinfo=None), i.end7))

    for i in range(len(object['meter'])):
        object['meter'][i] = round(object['meter'][i]) # PROGRESSBAR

    objects.append(object)

    start = start.replace(tzinfo=None)
    old = old.replace(tzinfo=None)

    top1 = (factory.end_start.replace(tzinfo=None)-factory.start_data.replace(tzinfo=None)).days
    top2 = (old-start).days # ПРОГНОЗ ПРОИЗВОДСТВА В ДНЯХ
    top = (top1/top2)*150
    top3 = 100 - ((old-dt).total_seconds()/(old-start).total_seconds())*100 # ФАКТ ПРОИЗВОДСТВА

    return render(request, 'users/pin.html', {'objects': objects, 'id': id, 'top1': top1, 'top': top, 'top2': top2, 'top3': top3})

def index(request):
    return render(request, 'users/index.html', {'title': 'Главная страница'})

def meeting(request):
    return render(request, 'users/meeting.html')

def contracts(request):
    return render(request, 'users/contracts.html')
