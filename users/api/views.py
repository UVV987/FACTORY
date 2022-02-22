from users.models import *
from django.http import HttpResponse
from django.shortcuts import render
import datetime


def get_model(department, id):
    if department == 'km' or department == 'kmd':
        return Factory.objects.all().filter(id=id)[0]
    else:
        return Detal.objects.all().filter(id=id)[0]


def notice(request, department):
    out = ''
    for i in Factory.objects.all():
        if department == 'km' and not i.sent1:
            out += str(i.id) + ','
            i.sent1 = True
        elif department == 'kmd' and not i.sent2:
            out += str(i.id) + ','
            i.sent2 = True

    for i in Detal.objects.all():
        if department == 'tmc' and not i.sent3:
            out += str(i.id) + ','
            i.sent3 = True
        elif department == 'zagatovka' and not i.sent4:
            out += str(i.id) + ','
            i.sent4 = True
        elif department == 'sborka' and not i.sent5:
            out += str(i.id) + ','
            i.sent5 = True
        elif department == 'svarka' and not i.sent6:
            out += str(i.id) + ','
            i.sent6 = True
        elif department == 'upakovka' and not i.sent7:
            out += str(i.id) + ','
            i.sent7 = True
        i.save()
    return HttpResponse(out)

def qr_start(request, department):
    if request.method == 'POST':
        model = get_model(department, request.POST.get('id'))
        dt = datetime.datetime.now()

        if department == 'km':
            model.history1 = f'start {1 - (model.end_start1.replace(tzinfo=None)-dt).total_seconds()/(model.end_start1.replace(tzinfo=None)-model.start_data1.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'kmd':
            model.history2 = f'start {1 - (model.end_start2.replace(tzinfo=None)-dt).total_seconds()/(model.end_start2.replace(tzinfo=None)-model.start_data2.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'tmc':
            model.history3 = f'start {1 - (model.end_start3.replace(tzinfo=None)-dt).total_seconds()/(model.end_start3.replace(tzinfo=None)-model.start_data3.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'zagatovka':
            model.history4 = f'start {1 - (model.end_start4.replace(tzinfo=None)-dt).total_seconds()/(model.end_start4.replace(tzinfo=None)-model.start_data4.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'sborka':
            model.history5 = f'start {1 - (model.end_start5.replace(tzinfo=None)-dt).total_seconds()/(model.end_start5.replace(tzinfo=None)-model.start_data5.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'svarka':
            model.history6 = f'start {1 - (model.end_start6.replace(tzinfo=None)-dt).total_seconds()/(model.end_start6.replace(tzinfo=None)-model.start_data6.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'upakovka':
            model.history7 = f'start {1 - (model.end_start7.replace(tzinfo=None)-dt).total_seconds()/(model.end_start7.replace(tzinfo=None)-model.start_data7.replace(tzinfo=None)).total_seconds()}|'
        model.save()

    return HttpResponse('')

def stop(request, department):
    if request.method == 'POST':
        model = get_model(department, request.POST.get('id'))
        dt = datetime.datetime.now()

        if department == 'km':
            moment = 1 - (model.end_start1.replace(tzinfo=None)-dt).total_seconds()/(model.end_start1.replace(tzinfo=None)-model.start_data1.replace(tzinfo=None)).total_seconds()
            if len(model.history1.split('|')) != 1 and len(model.history1.split('|')) % 2 != 0:
                model.history1 += f'break {moment}|'
            else:
                model.history1 += f'stop {moment}|'
        elif department == 'kmd':
            moment = 1 - (model.end_start2.replace(tzinfo=None)-dt).total_seconds()/(model.end_start2.replace(tzinfo=None)-model.start_data2.replace(tzinfo=None)).total_seconds()
            if len(model.history2.split('|')) != 1 and len(model.history2.split('|')) % 2 != 0:
                model.history2 += f'break {moment}|'
            else:
                model.history2 += f'stop {moment}|'
        elif department == 'tmc':
            moment = 1 - (model.end_start3.replace(tzinfo=None)-dt).total_seconds()/(model.end_start3.replace(tzinfo=None)-model.start_data3.replace(tzinfo=None)).total_seconds()
            if len(model.history3.split('|')) != 1 and len(model.history3.split('|')) % 2 != 0:
                model.history3 += f'break {moment}|'
            else:
                model.history3 += f'stop {moment}|'
        elif department == 'zagatovka':
            moment = 1 - (model.end_start4.replace(tzinfo=None)-dt).total_seconds()/(model.end_start4.replace(tzinfo=None)-model.start_data4.replace(tzinfo=None)).total_seconds()
            if len(model.history4.split('|')) != 1 and len(model.history4.split('|')) % 2 != 0:
                model.history4 += f'break {moment}|'
            else:
                model.history4 += f'stop {moment}|'
        elif department == 'sborka':
            moment = 1 - (model.end_start5.replace(tzinfo=None)-dt).total_seconds()/(model.end_start5.replace(tzinfo=None)-model.start_data5.replace(tzinfo=None)).total_seconds()
            if len(model.history5.split('|')) != 1 and len(model.history5.split('|')) % 2 != 0:
                model.history5 += f'break {moment}|'
            else:
                model.history5 += f'stop {moment}|'
        elif department == 'svarka':
            moment = 1 - (model.end_start6.replace(tzinfo=None)-dt).total_seconds()/(model.end_start6.replace(tzinfo=None)-model.start_data6.replace(tzinfo=None)).total_seconds()
            if len(model.history6.split('|')) != 1 and len(model.history6.split('|')) % 2 != 0:
                model.history6 += f'break {moment}|'
            else:
                model.history6 += f'stop {moment}|'
        elif department == 'upakovka':
            moment = 1 - (model.end_start7.replace(tzinfo=None)-dt).total_seconds()/(model.end_start7.replace(tzinfo=None)-model.start_data7.replace(tzinfo=None)).total_seconds()
            if len(model.history7.split('|')) != 1 and len(model.history7.split('|')) % 2 != 0:
                model.history7 += f'break {moment}|'
            else:
                model.history7 += f'stop {moment}|'
        model.save()

    return HttpResponse('')

def qr_start_otk(request, department):
    if request.method == 'POST':
        model = get_model(department, request.POST.get('id'))
        dt = datetime.datetime.now()

        if department == 'km':
            model.otk1 = f'start {(dt-model.end_start1.replace(tzinfo=None)).total_seconds()/(model.end_start1.replace(tzinfo=None)-model.start_data1.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'kmd':
            model.otk2 = f'start {(dt-model.end_start2.replace(tzinfo=None)).total_seconds()/(model.end_start2.replace(tzinfo=None)-model.start_data2.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'tmc':
            model.otk3 = f'start {(dt-model.end_start3.replace(tzinfo=None)).total_seconds()/(model.end_start3.replace(tzinfo=None)-model.start_data3.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'zagatovka':
            model.otk4 = f'start {(dt-model.end_start4.replace(tzinfo=None)).total_seconds()/(model.end_start4.replace(tzinfo=None)-model.start_data4.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'sborka':
            model.otk5 = f'start {(dt-model.end_start5.replace(tzinfo=None)).total_seconds()/(model.end_start5.replace(tzinfo=None)-model.start_data5.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'svarka':
            model.otk6 = f'start {(dt-model.end_start6.replace(tzinfo=None)).total_seconds()/(model.end_start6.replace(tzinfo=None)-model.start_data6.replace(tzinfo=None)).total_seconds()}|'
        elif department == 'upakovka':
            model.otk7 = f'start {(dt-model.end_start7.replace(tzinfo=None)).total_seconds()/(model.end_start7.replace(tzinfo=None)-model.start_data7.replace(tzinfo=None)).total_seconds()}|'
        model.save()

    return HttpResponse('')

def stop_otk(request, department):
    if request.method == 'POST':
        model = get_model(department, request.POST.get('id'))
        dt = datetime.datetime.now()

        if department == 'km':
            moment = (dt-model.end_start1.replace(tzinfo=None)).total_seconds()/(model.end_start1.replace(tzinfo=None)-model.start_data1.replace(tzinfo=None)).total_seconds()
            if len(model.otk1.split('|')) != 1 and len(model.otk1.split('|')) % 2 != 0:
                model.otk1 += f'break {moment}|'
            else:
                model.otk1 += f'stop {moment}|'
        elif department == 'kmd':
            moment = (dt-model.end_start2.replace(tzinfo=None)).total_seconds()/(model.end_start2.replace(tzinfo=None)-model.start_data2.replace(tzinfo=None)).total_seconds()
            if len(model.otk2.split('|')) != 1 and len(model.otk2.split('|')) % 2 != 0:
                model.otk2 += f'break {moment}|'
            else:
                model.otk2 += f'stop {moment}|'
        elif department == 'tmc':
            moment = (dt-model.end_start3.replace(tzinfo=None)).total_seconds()/(model.end_start3.replace(tzinfo=None)-model.start_data3.replace(tzinfo=None)).total_seconds()
            if len(model.otk3.split('|')) != 1 and len(model.otk3.split('|')) % 2 != 0:
                model.otk3 += f'break {moment}|'
            else:
                model.otk3 += f'stop {moment}|'
        elif department == 'zagatovka':
            moment = (dt-model.end_start4.replace(tzinfo=None)).total_seconds()/(model.end_start4.replace(tzinfo=None)-model.start_data4.replace(tzinfo=None)).total_seconds()
            if len(model.otk4.split('|')) != 1 and len(model.otk4.split('|')) % 2 != 0:
                model.otk4 += f'break {moment}|'
            else:
                model.otk4 += f'stop {moment}|'
        elif department == 'sborka':
            moment = (dt-model.end_start5.replace(tzinfo=None)).total_seconds()/(model.end_start5.replace(tzinfo=None)-model.start_data5.replace(tzinfo=None)).total_seconds()
            if len(model.otk5.split('|')) != 1 and len(model.otk5.split('|')) % 2 != 0:
                model.otk5 += f'break {moment}|'
            else:
                model.otk5 += f'stop {moment}|'
        elif department == 'svarka':
            moment = (dt-model.end_start6.replace(tzinfo=None)).total_seconds()/(model.end_start6.replace(tzinfo=None)-model.start_data6.replace(tzinfo=None)).total_seconds()
            if len(model.otk6.split('|')) != 1 and len(model.otk6.split('|')) % 2 != 0:
                model.otk6 += f'break {moment}|'
            else:
                model.otk6 += f'stop {moment}|'
        elif department == 'upakovka':
            moment = (dt-model.end_start7.replace(tzinfo=None)).total_seconds()/(model.end_start7.replace(tzinfo=None)-model.start_data7.replace(tzinfo=None)).total_seconds()
            if len(model.otk7.split('|')) != 1 and len(model.otk7.split('|')) % 2 != 0:
                model.otk7 += f'break {moment}|'
            else:
                model.otk7 += f'stop {moment}|'
        model.save()

    return HttpResponse('')

def back(request, department):
    if request.method == 'POST':
        model = get_model(department, request.POST.get('id'))

        if department == 'km':
            model.otk1 += 'back 1|'
        elif department == 'kmd':
            model.otk2 += 'back 1|'
        elif department == 'tmc':
            model.otk3 += 'back 1|'
        elif department == 'zagatovka':
            model.otk4 += 'back 1|'
        elif department == 'sborka':
            model.otk5 += 'back 1|'
        elif department == 'svarka':
            model.otk6 += 'back 1|'
        elif department == 'upakovka':
            model.otk7 += 'back 1|'

        model.save()

    return HttpResponse('')

def end(request, department):
    if request.method == 'POST':
        model = get_model(department, request.POST.get('id'))
        dt = datetime.datetime.now()

        if department == 'km':
            model.end1 += f'{(-(dt-model.end_start1.replace(tzinfo=None)).total_seconds()/(model.end_start1.replace(tzinfo=None)-model.start_data1.replace(tzinfo=None)).total_seconds())/100}'
        elif department == 'kmd':
            model.end2 += f'{(-(dt-model.end_start2.replace(tzinfo=None)).total_seconds()/(model.end_start2.replace(tzinfo=None)-model.start_data2.replace(tzinfo=None)).total_seconds())/100}'
        elif department == 'tmc':
            model.end3 += f'{(-(dt-model.end_start3.replace(tzinfo=None)).total_seconds()/(model.end_start3.replace(tzinfo=None)-model.start_data3.replace(tzinfo=None)).total_seconds())/100}'
        elif department == 'zagatovka':
            model.end4 += f'{(-(dt-model.end_start4.replace(tzinfo=None)).total_seconds()/(model.end_start4.replace(tzinfo=None)-model.start_data4.replace(tzinfo=None)).total_seconds())/100}'
        elif department == 'sborka':
            model.end5 += f'{(-(dt-model.end_start5.replace(tzinfo=None)).total_seconds()/(model.end_start5.replace(tzinfo=None)-model.start_data5.replace(tzinfo=None)).total_seconds())/100}'
        elif department == 'svarka':
            model.end6 += f'{(-(dt-model.end_start6.replace(tzinfo=None)).total_seconds()/(model.end_start6.replace(tzinfo=None)-model.start_data6.replace(tzinfo=None)).total_seconds())/100}'
        elif department == 'upakovka':
            model.end7 += f'{(-(dt-model.end_start7.replace(tzinfo=None)).total_seconds()/(model.end_start7.replace(tzinfo=None)-model.start_data7.replace(tzinfo=None)).total_seconds())/100}'

        model.save()

    return HttpResponse('')

def give_qr(request, id, model):
    if model == 'factory':
        department = 'km'
    else:
        department = ''

    return render(request, 'qr.html', {'svg': ''.join(open(str(get_model(department, id).qr), 'r').readlines()).replace('svg', 'svg style="transform: scale(3);"')})

def give_csrf(request):
    return render(request, 'csrf.html')
