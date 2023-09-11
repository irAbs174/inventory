from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, FileResponse
from .models import (SiteOrders, Fractions)
from django.conf import settings
from datetime import datetime


@csrf_exempt
@login_required
def orders_index(request):
    if request.method == 'POST':
        job = request.POST.get('job')
        if job == 'submit_new_orders':
            fractions_orders_value = Fractions.objects.all()
            order_code = request.POST.get('order_code')
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            package_status = request.POST.get('package_status')
            send_method = request.POST.get('send_method')
            order_desc = request.POST.get('order_desc')
            if order_code != "":
                if full_name !="":
                    if phone_number != "":
                        if order_desc != "":
                            # get database
                            order = SiteOrders.objects.filter(
                                order_code = order_code,)
                            if package_status == "بسته بندی نشده":
                                order.update(
                                    submit_by = request.user.email,
                                    order_code = order_code,
                                    full_name = full_name,
                                    phone_number = phone_number,
                                    package_status = False,
                                    send_status = False,
                                    order_time = datetime.now(),
                                    send_method = send_method,)
                                # Success message
                                new_orders_value = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders_value = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders_value = SiteOrders.objects.filter(send_status = True)
                                message = 'سفارش با موفقیت به روز رسانی شد'
                                page = request.GET.get('page', 1)
                                paginator0 = Paginator(new_orders_value, 50)
                                paginator1 = Paginator(packaged_orders_value, 50)
                                paginator2 = Paginator(sended_orders_value, 50)
                                paginator3 = Paginator(fractions_orders_value, 50)
                                try:
                                    new_orders = paginator0.page(page)
                                    packaged_orders = paginator1.page(page)
                                    sended_orders = paginator2.page(page)
                                    fractions_orders = paginator3.page(page)
                                except PageNotAnInteger:
                                    new_orders = paginator0.page(1)
                                    packaged_orders = paginator1.page(1)
                                    sended_orders = paginator3.page(1)
                                    fractions_orders = paginator2.page(1)
                                except EmptyPage:
                                    new_orders = paginator0.page(paginator0.num_pages)
                                    packaged_orders = paginator1.page(paginator1.num_pages)
                                    sended_orders = paginator2.page(paginator2.num_pages)
                                    fractions_orders = paginator3.page(paginator3.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                            elif package_status =="بسته بندی شده":
                                order.update(
                                    submit_by = request.user.email,
                                    order_code = order_code,
                                    full_name = full_name,
                                    phone_number = phone_number,
                                    package_status = True,
                                    send_status = False,
                                    order_time = datetime.now(),
                                    send_method = send_method,)
                                # Success message
                                new_orders_value = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders = SiteOrders.objects.filter(send_status = True)
                                message = 'سفارش با موفقیت به روز رسانی شد'
                                page = request.GET.get('page', 1)
                                paginator = Paginator(new_orders_value, 50)
                                try:
                                    new_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    new_orders = paginator.page(1)
                                except EmptyPage:
                                    new_orders = paginator.page(paginator.num_pages)
                                fractions_orders = Fractions.objects.all()
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                            elif package_status == "کسری(اگر محصول در انبار موجود نیست انتخاب کنید)":
                                for i in order:
                                    factor = i.factor_file
                                    desc = i.order_desc
                                Fractions.objects.create(
                                order_code = order_code,
                                full_name = full_name,
                                phone_number = phone_number,
                                package_status = False,
                                send_status = False,
                                send_method = "روش ارسال انتخاب نشده",
                                factor_file = factor, 
                                order_time = datetime.now(),
                                order_desc = desc,
                                )
                                order.delete()
                                # Success message
                                new_orders_value = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders = SiteOrders.objects.filter(send_status = True)
                                message = 'سفارش با موقیت ایجاد شد'
                                page = request.GET.get('page', 1)
                                paginator = Paginator(new_orders_value, 50)
                                try:
                                    new_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    new_orders = paginator.page(1)
                                except EmptyPage:
                                    new_orders = paginator.page(paginator.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                            else:
                                new_orders_value = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders = SiteOrders.objects.filter(send_status = True)
                                message = 'توضیحات سفارش خالیست'
                                page = request.GET.get('page', 1)
                                paginator = Paginator(new_orders_value, 50)
                                try:
                                    new_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    new_orders = paginator.page(1)
                                except EmptyPage:
                                    new_orders = paginator.page(paginator.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                        else:
                            new_orders_value = SiteOrders.objects.filter(send_status = False, package_status = False)
                            packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                            sended_orders = SiteOrders.objects.filter(send_status = True)
                            message = 'توضیحات سفارش خالیست'
                            page = request.GET.get('page', 1)
                            paginator = Paginator(new_orders_value, 50)
                            try:
                                new_orders = paginator.page(page)
                            except PageNotAnInteger:
                                new_orders = paginator.page(1)
                            except EmptyPage:
                                new_orders = paginator.page(paginator.num_pages)
                            context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                            return render(request, 'orders/orders_index.html', context = context)
                    else:
                        new_orders_value = SiteOrders.objects.filter(send_status = False, package_status = False)
                        packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                        sended_orders = SiteOrders.objects.filter(send_status = True)
                        message = 'شماره تلفن وارد نشده'  
                        page = request.GET.get('page', 1)
                        paginator = Paginator(new_orders_value, 50)
                        try:
                            new_orders = paginator.page(page)
                        except PageNotAnInteger:
                            new_orders = paginator.page(1)
                        except EmptyPage:
                            new_orders = paginator.page(paginator.num_pages)
                        context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                        return render(request, 'orders/orders_index.html', context = context)
                else:
                    new_orders_value = SiteOrders.objects.filter(send_status = False, package_status = False)
                    packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                    sended_orders = SiteOrders.objects.filter(send_status = True)
                    message = 'نام و نام خانوادگی وارد نشده'
                    page = request.GET.get('page', 1)
                    paginator = Paginator(new_orders_value, 50)
                    try:
                        new_orders = paginator.page(page)
                    except PageNotAnInteger:
                        new_orders = paginator.page(1)
                    except EmptyPage:
                        new_orders = paginator.page(paginator.num_pages)
                    context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                    return render(request, 'orders/orders_index.html', context = context)
            else:
                new_orders_value = SiteOrders.objects.filter(send_status = False, package_status = False)
                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                sended_orders = SiteOrders.objects.filter(send_status = True)
                message = 'کد سفارش وارد نشده'
                page = request.GET.get('page', 1)
                paginator = Paginator(new_orders_value, 50)
                try:
                    new_orders = paginator.page(page)
                except PageNotAnInteger:
                    new_orders = paginator.page(1)
                except EmptyPage:
                    new_orders = paginator.page(paginator.num_pages)
                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                return render(request, 'orders/orders_index.html', context = context)
        elif job == 'submit_packaged_orders':
            fractions_orders = Fractions.objects.all()
            order_code = request.POST.get('order_code')
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            package_status = request.POST.get('package_status')
            send_status = request.POST.get('send_status')
            send_method = request.POST.get('send_method')
            order_desc = request.POST.get('order_desc')
            if order_code != "":
                if full_name !="":
                    if phone_number != "":
                        if order_desc != "":
                            # get database
                            order = SiteOrders.objects.filter(
                                order_code = order_code,
                            )
                            if send_status == "پست نشده":
                                order.update(send_status = False, submit_by = request.user.email,)
                                # Success message
                                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders_value = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders = SiteOrders.objects.filter(send_status = True)
                                message = 'سفارش با موفقیت به روز رسانی شد'
                                page = request.GET.get('page', 1)
                                paginator = Paginator(packaged_orders_value, 50)
                                try:
                                    packaged_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    packaged_orders = paginator.page(1)
                                except EmptyPage:
                                    packaged_orders = paginator.page(paginator.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                            elif send_status == "پست شده":
                                order.update(send_status = True, submit_by = request.user.email, order_time = datetime.now())
                                # Success message
                                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders_value = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders = SiteOrders.objects.filter(send_status = True)
                                message = 'سفارش با موفقیت به روز رسانی شد'
                                page = request.GET.get('page', 1)
                                paginator = Paginator(packaged_orders_value, 50)
                                try:
                                    packaged_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    packaged_orders = paginator.page(1)
                                except EmptyPage:
                                    packaged_orders = paginator.page(paginator.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                            else:
                                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders_value = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders = SiteOrders.objects.filter(send_status = True)
                                message = 'شماره تلفن وارد نشده'  
                                page = request.GET.get('page', 1)
                                paginator = Paginator(packaged_orders_value, 50)
                                try:
                                    packaged_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    packaged_orders = paginator.page(1)
                                except EmptyPage:
                                    packaged_orders = paginator.page(paginator.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                        else:
                            new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                            packaged_orders_value = SiteOrders.objects.filter(package_status = True, send_status = False)
                            sended_orders = SiteOrders.objects.filter(send_status = True)
                            message = 'توضیحات سفارش خالیست'  
                            page = request.GET.get('page', 1)
                            paginator = Paginator(packaged_orders_value, 50)
                            try:
                                packaged_orders = paginator.page(page)
                            except PageNotAnInteger:
                                packaged_orders = paginator.page(1)
                            except EmptyPage:
                                packaged_orders = paginator.page(paginator.num_pages)
                            context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                            return render(request, 'orders/orders_index.html', context = context)
                    else:
                        new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                        packaged_orders_value = SiteOrders.objects.filter(package_status = True, send_status = False)
                        sended_orders = SiteOrders.objects.filter(send_status = True)
                        message = 'شماره تلفن وارد نشده'  
                        page = request.GET.get('page', 1)
                        paginator = Paginator(packaged_orders_value, 50)
                        try:
                            packaged_orders = paginator.page(page)
                        except PageNotAnInteger:
                            packaged_orders = paginator.page(1)
                        except EmptyPage:
                            packaged_orders = paginator.page(paginator.num_pages)
                        context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                        return render(request, 'orders/orders_index.html', context = context)
                else:
                    new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                    packaged_orders_value = SiteOrders.objects.filter(package_status = True, send_status = False)
                    sended_orders = SiteOrders.objects.filter(send_status = True)
                    message = 'نام و نام خانوادگی وارد نشده'
                    page = request.GET.get('page', 1)
                    paginator = Paginator(packaged_orders_value, 50)
                    try:
                        packaged_orders = paginator.page(page)
                    except PageNotAnInteger:
                        packaged_orders = paginator.page(1)
                    except EmptyPage:
                        packaged_orders = paginator.page(paginator.num_pages)
                    context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                    return render(request, 'orders/orders_index.html', context = context)
            else:
                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                packaged_orders_value = SiteOrders.objects.filter(package_status = True, send_status = False)
                sended_orders = SiteOrders.objects.filter(send_status = True)
                message = 'کد سفارش وارد نشده'
                page = request.GET.get('page', 1)
                paginator = Paginator(packaged_orders_value, 50)
                try:
                    packaged_orders = paginator.page(page)
                except PageNotAnInteger:
                    packaged_orders = paginator.page(1)
                except EmptyPage:
                    packaged_orders = paginator.page(paginator.num_pages)
                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                return render(request, 'orders/orders_index.html', context = context)
        elif job == 'submit_sended_orders':
            fractions_orders = Fractions.objects.all()
            order_code = request.POST.get('order_code')
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            package_status = request.POST.get('package_status')
            send_status = request.POST.get('send_status')
            send_method = request.POST.get('send_method')
            order_desc = request.POST.get('order_desc')
            if order_code != "":
                if full_name !="":
                    if phone_number != "":
                        if order_desc != "":
                            # get database
                            order = SiteOrders.objects.filter(
                                order_code = order_code,
                            )
                            if send_status == "پست نشده":
                                order.update(send_status = False, submit_by = request.user.email,)
                                # Success message
                                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders_value = SiteOrders.objects.filter(send_status = True)
                                message = 'سفارش با موفقیت به روز رسانی شد'
                                page = request.GET.get('page', 1)
                                paginator = Paginator(sended_orders_value, 50)
                                try:
                                    sended_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    sended_orders = paginator.page(1)
                                except EmptyPage:
                                    sended_orders = paginator.page(paginator.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                            elif send_status == "پست شده":
                                order.update(send_status = True, submit_by = request.user.email,)
                                # Success message
                                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders_value = SiteOrders.objects.filter(send_status = True)
                                message = 'سفارش با موفقیت به روز رسانی شد'
                                page = request.GET.get('page', 1)
                                paginator = Paginator(sended_orders_value, 50)
                                try:
                                    sended_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    sended_orders = paginator.page(1)
                                except EmptyPage:
                                    sended_orders = paginator.page(paginator.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                            else:
                                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders_value = SiteOrders.objects.filter(send_status = True)
                                message = 'شماره تلفن وارد نشده'  
                                page = request.GET.get('page', 1)
                                paginator = Paginator(sended_orders_value, 50)
                                try:
                                    sended_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    sended_orders = paginator.page(1)
                                except EmptyPage:
                                    sended_orders = paginator.page(paginator.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                        else:
                            new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                            packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                            sended_orders_value = SiteOrders.objects.filter(send_status = True)
                            message = 'توضیحات سفارش خالیست'  
                            page = request.GET.get('page', 1)
                            paginator = Paginator(sended_orders_value, 50)
                            try:
                                sended_orders = paginator.page(page)
                            except PageNotAnInteger:
                                sended_orders = paginator.page(1)
                            except EmptyPage:
                                sended_orders = paginator.page(paginator.num_pages)
                            context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                            return render(request, 'orders/orders_index.html', context = context)
                    else:
                        new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                        packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                        sended_orders_value = SiteOrders.objects.filter(send_status = True)
                        message = 'شماره تلفن وارد نشده'  
                        page = request.GET.get('page', 1)
                        paginator = Paginator(sended_orders_value, 50)
                        try:
                            sended_orders = paginator.page(page)
                        except PageNotAnInteger:
                            sended_orders = paginator.page(1)
                        except EmptyPage:
                            sended_orders = paginator.page(paginator.num_pages)
                        context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                        return render(request, 'orders/orders_index.html', context = context)
                else:
                    new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                    packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                    sended_orders_value = SiteOrders.objects.filter(send_status = True)
                    message = 'نام و نام خانوادگی وارد نشده'
                    page = request.GET.get('page', 1)
                    paginator = Paginator(sended_orders_value, 50)
                    try:
                        sended_orders = paginator.page(page)
                    except PageNotAnInteger:
                        sended_orders = paginator.page(1)
                    except EmptyPage:
                        sended_orders = paginator.page(paginator.num_pages)
                    context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                    return render(request, 'orders/orders_index.html', context = context)
            else:
                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                sended_orders_value = SiteOrders.objects.filter(send_status = True)
                message = 'کد سفارش وارد نشده'
                page = request.GET.get('page', 1)
                paginator = Paginator(sended_orders_value, 50)
                try:
                    sended_orders = paginator.page(page)
                except PageNotAnInteger:
                    sended_orders = paginator.page(1)
                except EmptyPage:
                    sended_orders = paginator.page(paginator.num_pages)
                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                return render(request, 'orders/orders_index.html', context = context)
        elif job == 'submit_fraction_change':
            fractions_orders_value = Fractions.objects.all()
            order_code = request.POST.get('order_code')
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            package_status = request.POST.get('package_status')
            send_method = request.POST.get('send_method')
            order_desc = request.POST.get('order_desc')
            if order_code != "":
                if full_name !="":
                    if phone_number != "":
                        if order_desc != "":
                            # get database
                            if package_status == "کسری(اگر محصول در انبار موجود نیست انتخاب کنید)":
                                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders = SiteOrders.objects.filter(send_status = True)
                                message = 'وضعیت کنونی سفارش کسری است'
                                page = request.GET.get('page', 1)
                                paginator = Paginator(fractions_orders_value, 50)
                                try:
                                    fractions_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    fractions_orders = paginator.page(1)
                                except EmptyPage:
                                    fractions_orders = paginator.page(paginator.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                            else:
                                order = Fractions.objects.filter(order_code = order_code,)
                                for i in order:
                                    factor = i.factor_file
                                SiteOrders.objects.create(
                                    order_code = order_code,
                                    full_name = full_name,
                                    phone_number = phone_number,
                                    package_status = False,
                                    send_status = False,
                                    send_method = "روش ارسال انتخاب نشده",
                                    factor_file = factor,
                                    order_desc = order_desc,
                                )
                                order.delete()
                                # Success message
                                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders = SiteOrders.objects.filter(send_status = True)
                                message = 'سفارش با موفقیت به روز رسانی شد'
                                page = request.GET.get('page', 1)
                                paginator = Paginator(fractions_orders_value, 50)
                                try:
                                    fractions_orders = paginator.page(page)
                                except PageNotAnInteger:
                                    fractions_orders = paginator.page(1)
                                except EmptyPage:
                                    fractions_orders = paginator.page(paginator.num_pages)
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, 'orders/orders_index.html', context = context)
                        else:
                            new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                            packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                            sended_orders = SiteOrders.objects.filter(send_status = True)
                            message = 'توضیحات سفارش خالیست'  
                            page = request.GET.get('page', 1)
                            paginator = Paginator(fractions_orders_value, 50)
                            try:
                                fractions_orders = paginator.page(page)
                            except PageNotAnInteger:
                                fractions_orders = paginator.page(1)
                            except EmptyPage:
                                fractions_orders = paginator.page(paginator.num_pages)
                            context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                            return render(request, 'orders/orders_index.html', context = context)
                    else:
                        new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                        packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                        sended_orders = SiteOrders.objects.filter(send_status = True)
                        message = 'شماره تلفن وارد نشده'  
                        page = request.GET.get('page', 1)
                        paginator = Paginator(fractions_orders_value, 50)
                        try:
                            fractions_orders = paginator.page(page)
                        except PageNotAnInteger:
                            fractions_orders = paginator.page(1)
                        except EmptyPage:
                            fractions_orders = paginator.page(paginator.num_pages)
                        context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                        return render(request, 'orders/orders_index.html', context = context)
                else:
                    new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                    packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                    sended_orders = SiteOrders.objects.filter(send_status = True)
                    message = 'نام و نام خانوادگی وارد نشده'
                    page = request.GET.get('page', 1)
                    paginator = Paginator(fractions_orders_value, 50)
                    try:
                        fractions_orders = paginator.page(page)
                    except PageNotAnInteger:
                        fractions_orders = paginator.page(1)
                    except EmptyPage:
                        fractions_orders = paginator.page(paginator.num_pages)
                    context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                    return render(request, 'orders/orders_index.html', context = context)
            else:
                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                sended_orders = SiteOrders.objects.filter(send_status = True)
                message = 'کد سفارش وارد نشده'
                page = request.GET.get('page', 1)
                paginator = Paginator(fractions_orders_value, 50)
                try:
                    fractions_orders = paginator.page(page)
                except PageNotAnInteger:
                    fractions_orders = paginator.page(1)
                except EmptyPage:
                    fractions_orders = paginator.page(paginator.num_pages)
                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                return render(request, 'orders/orders_index.html', context = context)
        elif job == 'submit_search':
            fractions_orders = Fractions.objects.all()
            searched_text = request.POST.get('searched_text')
            if searched_text != "":
                order = SiteOrders.objects.filter(order_code__contains = searched_text)
                if order.exists():
                    search_result = SiteOrders.objects.filter(order_code__contains = searched_text)
                    new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                    packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                    sended_orders = SiteOrders.objects.filter(send_status = True)
                    message = ''
                    context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':search_result, 'message': message, 'fractions_orders':fractions_orders,}
                    return render(request, "orders/orders_index.html", context = context)
                else:
                    new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                    packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                    sended_orders = SiteOrders.objects.filter(send_status = True)
                    message = 'کد سفارش جستجو شده یافت نشد'
                    context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                    return render(request, "orders/orders_index.html", context = context)
            else:
                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                sended_orders = SiteOrders.objects.filter(send_status = True)
                message = 'کد سفارشی جستجو نکردید !'
                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                return render(request, "orders/orders_index.html", context = context)
        elif job == 'edit_search':
            fractions_orders = Fractions.objects.all()
            order_code = request.POST.get('order_code')
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            package_status = request.POST.get('package_status')
            send_status = request.POST.get('send_status')
            send_method = request.POST.get('send_method')
            order_desc = request.POST.get('order_desc')
            if order_code != "":
                if full_name !="":
                    if phone_number != "":
                        if order_desc != "":
                            if package_status == "بسته بندی شده":
                                PACKAGE = True
                            elif package_status == "بسته بندی نشده":
                                PACKAGE = False
                            if send_status == "پست شده":
                                SEND = True
                            elif send_status == "پست نشده":
                                SEND = False
                            order = SiteOrders.objects.filter(order_code = order_code,)
                            order.update(
                                submit_by = request.user.email,
                                order_code = order_code,
                                full_name = full_name,
                                phone_number = phone_number,
                                package_status = PACKAGE,
                                send_status = SEND,
                                send_method = send_method,
                                order_desc = order_desc,)
                            new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                            packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                            sended_orders = SiteOrders.objects.filter(send_status = True)
                            message = 'سفارش با موفقیت به روز رسانی شد'
                            context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                            return render(request, "orders/orders_index.html", context = context)
                        else:
                            new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                            packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                            sended_orders = SiteOrders.objects.filter(send_status = True)
                            message = 'توضیحات سفارش خالیست'  
                            context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                            return render(request, "orders/orders_index.html", context = context)
                    else:
                        new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                        packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                        sended_orders = SiteOrders.objects.filter(send_status = True)
                        message = 'شماره تلفن وارد نشده'  
                        context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                        return render(request, "orders/orders_index.html", context = context)
                else:
                    new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                    packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                    sended_orders = SiteOrders.objects.filter(send_status = True)
                    message = 'نام و نام خانوادگی وارد نشده'
                    context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                    return render(request, "orders/orders_index.html", context = context)
            else:
                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                sended_orders = SiteOrders.objects.filter(send_status = True)
                message = 'کد سفارش وارد نشده'
                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                return render(request, "orders/orders_index.html", context = context)
        elif job == 'submit_order':
            fractions_orders = Fractions.objects.all()
            order_code = request.POST.get('order_code')
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            order_desc = request.POST.get('order_desc')
            if order_code != "":
                if full_name !="":
                    if phone_number != "":
                        if order_desc != "":
                            # get database
                            order = SiteOrders.objects.filter(order_code = order_code,)
                            if order.exists():
                                # order is exist error
                                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders = SiteOrders.objects.filter(send_status = True)
                                message = 'سفارش از پیش موجود است' 
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, "orders/orders_index.html", context = context)
                            else:
                                fs = FileSystemStorage()
                                uploaded_file = request.FILES['myfile']
                                filename = fs.save(uploaded_file.name, uploaded_file)
                                SiteOrders.objects.create(
                                order_code = order_code,
                                full_name = full_name,
                                phone_number = phone_number,
                                package_status = False,
                                send_status = False,
                                send_method = "روش ارسال انتخاب نشده",
                                factor_file = filename,
                                order_desc = order_desc,
                                )
                                # Success message
                                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                                sended_orders = SiteOrders.objects.filter(send_status = True)
                                message = 'سفارش با موقیت ایجاد شد'
                                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                                return render(request, "orders/orders_index.html", context = context)
                        else:
                            new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                            packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                            sended_orders = SiteOrders.objects.filter(send_status = True)
                            message = 'توضیحات سفارش خالیست'  
                            context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                            return render(request, "orders/orders_index.html", context = context)
                    else:
                        new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                        packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                        sended_orders = SiteOrders.objects.filter(send_status = True)
                        message = 'شماره تلفن وارد نشده'  
                        context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                        return render(request, "orders/orders_index.html", context = context)
                else:
                    new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                    packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                    sended_orders = SiteOrders.objects.filter(send_status = True)
                    message = 'نام و نام خانوادگی وارد نشده'
                    context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                    return render(request, "orders/orders_index.html", context = context)
            else:
                new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
                packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
                sended_orders = SiteOrders.objects.filter(send_status = True)
                message = 'کد سفارش وارد نشده'
                context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
                return render(request, "orders/orders_index.html", context = context)
    else:
        fractions_orders = Fractions.objects.all()
        new_orders = SiteOrders.objects.filter(send_status = False, package_status = False)
        packaged_orders = SiteOrders.objects.filter(package_status = True, send_status = False)
        sended_orders_value = SiteOrders.objects.filter(send_status = True)
        message = ''
        page = request.GET.get('page', 1)
        paginator = Paginator(sended_orders_value, 50)
        try:
            sended_orders = paginator.page(page)
        except PageNotAnInteger:
            sended_orders = paginator.page(1)
        except EmptyPage:
            sended_orders = paginator.page(paginator.num_pages)
        context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
        return render(request, 'orders/orders_index.html', context = context)
    new_orders_value = SiteOrders.objects.filter(send_status = False, package_status = False)
    packaged_orders_value = SiteOrders.objects.filter(package_status = True, send_status = False)
    sended_orders_value = SiteOrders.objects.filter(send_status = True)
    fractions_orders_value = Fractions.objects.all()
    message = ''
    page = request.GET.get('page', 1)
    paginator = Paginator(sended_orders_value, 50)
    try:
        sended_orders = paginator.page(page)
    except PageNotAnInteger:
        sended_orders = paginator.page(1)
    except EmptyPage:
        sended_orders = paginator.page(paginator.num_pages)
    context = {'new_orders':new_orders,'packaged_orders':packaged_orders, 'sended_orders':sended_orders, 'search_result':'', 'message': message, 'fractions_orders':fractions_orders,}
    return render(request, 'orders/orders_index.html', context = context)

@csrf_exempt
@login_required
def download_factor(request, code):
    order = get_object_or_404(SiteOrders, order_code = code)
    upload_link = order.factor_file
    response = FileResponse(open(upload_link.path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{upload_link.name}"'
    return response