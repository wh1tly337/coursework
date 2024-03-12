from datetime import datetime

import pytz
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .forms import (
    OrdersForm, ContactForm,
    RefoundForm, CatalogForm,
    SizeForm, UsersRegisterForm,
    UsersEnteranceForm
)
from .models import AssortmentAdding, Orders, Cart, Users


def for_cart():
    """ Общий класс для доступа всех функций к данным корзины. """
    cart = Cart.objects.all()
    amount = Cart.objects.aggregate(Sum('price'))['price__sum']

    return cart, amount


def for_login():
    """ Общий класс для доступа всех функций к данным логина. """
    login = Users.objects.filter(status=True).exists()

    return login


def home(request):
    items = AssortmentAdding.objects.all()
    login = for_login()
    cart, amount = for_cart()

    context = {
        'items': items,
        'amount': amount,
        'cart': cart,
        'login': login
    }

    return render(request, 'main/home.html', context)


def catalog(request):
    login = for_login()
    cart, amount = for_cart()

    try:
        # Настройка сортровки товаров
        choices = {
            '1': AssortmentAdding.objects.all(),
            '2': AssortmentAdding.objects.order_by('-price'),
            '3': AssortmentAdding.objects.order_by('price'),
            '4': AssortmentAdding.objects.order_by('-add_date'),
        }

        temp = request.GET['sort_field']
        form = CatalogForm(initial={'sort_field': temp})
        items = choices.get(temp)

    except Exception:
        # Используется до применения сортировки
        temp = ''
        form = CatalogForm()
        items = AssortmentAdding.objects.all()

    paginator = Paginator(items, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'items': items,
        'form': form,
        'temp': temp,
        'page_obj': page_obj,
        'amount': amount,
        'cart': cart,
        'login': login
    }

    return render(request, 'main/shoe_catalog.html', context)


def about_us(request):
    login = for_login()
    cart, amount = for_cart()

    context = {
        'amount': amount,
        'cart': cart,
        'login': login
    }

    return render(request, 'main/about_us.html', context)


def contact_us(request):
    form = ContactForm()
    login = for_login()
    cart, amount = for_cart()

    if request.method == 'POST':
        # Отправка данных из формы связи
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            # Оповещение по почте о поступившем сообщении
            contact_name = request.POST['contact_name']
            contact_email = request.POST['contact_email']
            contact_description = request.POST['contact_description']
            message = 'Заявка обработана ИС "СникерШаг"\nИмя пользователя: ' \
                      + contact_name + '\nПочта пользователя: ' + contact_email \
                      + '\nТекст обращения: ' + contact_description
            send_mail(
                subject='Пришло новое обращение с сайта',
                message=message,
                from_email=f"{settings.EMAIL_HOST_USER}",
                recipient_list=['wh1tly337@gmail.com'],
                fail_silently=False
            )

            return redirect('appeal')
        else:
            context = {
                'form': form,
                'amount': amount,
                'cart': cart,
                'login': login,
                'error': 'Введите вреный адрес электронной почты, используя @'
            }

            return render(request, 'main/contact_us.html', context)

    context = {
        'form': form,
        'amount': amount,
        'cart': cart,
        'login': login,
        'error': ''
    }

    return render(request, 'main/contact_us.html', context)


def product_card(request, pk):
    item = get_object_or_404(AssortmentAdding, pk=pk)
    form = SizeForm(currentid=pk)
    login = for_login()
    cart, amount = for_cart()
    success = ''

    if request.method == 'POST':
        try:
            size = request.POST['size_field']
            if size == '0':
                context = {
                    'item': item, 'form': form,
                    'cart': cart, 'amount': amount,
                    'login': login,
                    'error': 'Вы забыли выбрать размер'
                }

                return render(request, 'main/product_card.html', context)
            elif size == '-1':
                context = {
                    'item': item, 'form': form,
                    'cart': cart, 'amount': amount,
                    'login': login,
                    'error': 'К сожалению, пар данного размера нет в ассортименте'
                }

                return render(request, 'main/product_card.html', context)
            else:
                info_assortment = AssortmentAdding.objects.in_bulk()

                image = info_assortment[pk].main_image
                item_id = info_assortment[pk].id
                name = str(info_assortment[pk].name)
                price = info_assortment[pk].price
                success = 'Товар добавлен в корзину'

                info_cart = Cart.objects.all()
                if len(info_cart) > 0:
                    for element in info_cart:
                        if int(element.get_cart_id()) == int(item_id):
                            if int(element.get_cart_size()) == int(size):
                                return redirect(f"product_id={pk}")

                # Добавление товара в корзину
                Cart.objects.create(
                    item_id=item_id, image=image,
                    name=name, size=size,
                    price=price, quantity=1
                )

                # Удаление размеров из карточки товара
                assortment = AssortmentAdding.objects.filter(id=item_id)
                sizes = assortment[0].get_sizes().split(' ')
                count_actual_sizes = 0
                for j in range(len(sizes)):
                    if sizes[j] == size:
                        sizes[j] = ''
                    if sizes[j] == '':
                        count_actual_sizes += 1
                AssortmentAdding.objects.filter(id=item_id).update(
                    sizes=' '.join(sizes),
                    update_date=datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime("%Y-%m-%d %H:%M:%S")
                )

                # Пересоздание формы для обновления информации в ней
                form = SizeForm(currentid=pk)

                # Оповещение о том что заканчиаются размеры
                if count_actual_sizes > 4:
                    message = f'Оповещение от ИС "СникерШаг"\
                    {"\n"}Низкое количество размеров товара.\
                    {"\n"}ID товара: {item_id}\
                    {"\n"}Название: {assortment[0].get_item_name()}\
                    {"\n"}Оставшиеся размеры: {sizes}\
                    {"\n"}Необходимо дозаказать отсутствующие размеры'
                    send_mail(
                        subject='У товара заканчиваются размеры',
                        message=message,
                        from_email="{settings.EMAIL_HOST_USER}",
                        recipient_list=['wh1tly337@gmail.com'],
                        fail_silently=False
                    )
        except Exception:
            pass

    context = {
        'item': item,
        'form': form,
        'amount': amount,
        'cart': cart,
        'login': login,
        'error': '',
        'success': success
    }

    return render(request, 'main/product_card.html', context)


def cart(request):
    login = for_login()
    cart, amount = for_cart()

    if request.method == 'POST':
        try:
            # Удаление товара из корзины
            item_id, size = request.POST['deletebtn'].split(' ')
            Cart.objects.filter(
                item_id=item_id,
                size=size
            ).delete()

            # Пересоздание элементов для правильного отображение итоговой суммы после удаления
            cart, amount = for_cart()

            # Добавление товара обратно в ассортимент
            assortment = AssortmentAdding.objects.filter(id=item_id)
            sizes = assortment[0].get_sizes().split(' ')
            counter = 0
            for j in range(len(sizes)):
                if int(36 + counter) == int(size):
                    sizes[j] = str(size)
                    AssortmentAdding.objects.filter(id=item_id).update(
                        sizes=' '.join(sizes),
                        update_date=None
                    )
                counter += 1
        except Exception:
            pass

    context = {
        'amount': amount,
        'cart': cart,
        'login': login
    }

    return render(request, 'main/cart.html', context)


def chect_out(request):
    form = OrdersForm()
    login = for_login()
    cart, amount = for_cart()

    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            form.save()

            cart_items = Cart.objects.all()
            # Если корзина пуста, то заказ не оформится
            if len(cart_items) == 0:
                context = {
                    'form': form,
                    'amount': amount,
                    'cart': cart,
                    'login': login,
                    'error_form': '',
                    'error_cart': 'Ваша козина пуста'
                }

                return render(request, 'main/out_form.html', context)

            result_id, result_name, final_price = '', '', 0
            for i in range(len(cart_items)):
                item_id = cart_items[i].get_cart_id()
                item_name = cart_items[i].get_cart_name()
                size = cart_items[i].get_cart_size()

                result_id += f"{item_id}({size}) "
                result_name += f"{item_name}"
                final_price += int(cart_items[i].get_cart_price())

            # Добавление общей суммы, id товаров и их размеров в таблицу с заказами
            Orders.objects.filter(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                city=form.cleaned_data['city'],
                post_index=form.cleaned_data['post_index'],
                adres=form.cleaned_data['adres'],
                phone_number=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email'],
                payment_method=form.cleaned_data['payment_method'],
            ).update(
                items_id=result_id,
                items_names=result_name,
                final_price=final_price
            )

            # Удаление всех данных из корзины
            Cart.objects.all().delete()

            return redirect('purchase')
        else:
            context = {
                'form': form,
                'amount': amount,
                'cart': cart,
                'login': login,
                'error_form': 'Введите вреный адрес электронной почты, используя @',
                'error_cart': ''
            }

            return render(request, 'main/out_form.html', context)

    context = {
        'form': form,
        'amount': amount,
        'cart': cart,
        'login': login,
        'error_form': '',
        'error_cart': ''
    }

    return render(request, 'main/out_form.html', context)


def refound(request):
    form = RefoundForm()
    login = for_login()
    cart, amount = for_cart()

    if request.method == 'POST':
        form = RefoundForm(request.POST)
        if form.is_valid():
            try:
                # Проверка на правильность введенных данных для возврата
                info = Orders.objects.in_bulk()
                first_name = info[form.cleaned_data['refound_id']].first_name
                last_name = info[form.cleaned_data['refound_id']].last_name
                phone = info[form.cleaned_data['refound_id']].phone_number
                email = info[form.cleaned_data['refound_id']].email
                if (
                        phone == form.cleaned_data['phone_number']
                        and email == form.cleaned_data['email']
                        and first_name == form.cleaned_data['first_name']
                        and last_name == form.cleaned_data['last_name']
                ):
                    Orders.objects.filter(order_id=form.cleaned_data['refound_id']).update(
                        status=Orders.REFOUND,
                        refound_description=form.cleaned_data['refound_description'],
                        end_date=datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime("%Y-%m-%d %H:%M:%S")
                    )

                    return redirect('appeal')
                else:
                    context = {
                        'form': form,
                        'amount': amount,
                        'cart': cart,
                        'login': login,
                        'error': 'Такого заказа нет, проверьте правильность введенных данных'
                    }

                    return render(request, 'main/refound.html', context)
            except Exception:
                context = {
                    'form': form,
                    'amount': amount,
                    'cart': cart,
                    'login': login,
                    'error': 'Такого заказа нет, проверьте правильность введенных данных'
                }

                return render(request, 'main/refound.html', context)
        else:
            context = {
                'form': form,
                'amount': amount,
                'cart': cart,
                'login': login,
                'error': 'Введите вреный адрес электронной почты, используя @'
            }

            return render(request, 'main/refound.html', context)

    context = {
        'form': form,
        'amount': amount,
        'cart': cart,
        'login': login,
        'error': ''
    }

    return render(request, 'main/refound.html', context)


def purchase(request):
    login = for_login()
    cart, amount = for_cart()

    context = {
        'amount': amount,
        'cart': cart,
        'login': login
    }

    return render(request, 'main/purchase.html', context)


def appeal(request):
    login = for_login()
    cart, amount = for_cart()

    context = {
        'amount': amount,
        'cart': cart,
        'login': login
    }

    return render(request, 'main/appeal.html', context)


def comming_soon(request, exception):
    login = for_login()
    cart, amount = for_cart()

    context = {
        'amount': amount,
        'cart': cart,
        'login': login
    }

    return render(request, 'main/comming_soon.html', context)


def entrance(request):
    form = UsersEnteranceForm()
    login = for_login()
    cart, amount = for_cart()

    if request.method == 'POST':
        # Отправка данных из формы входа
        form = UsersEnteranceForm(request.POST)
        if form.is_valid():
            try:
                # Проверка на правильность введенных данных при входе
                info = Users.objects.filter(email=form.cleaned_data['email'])

                # TODO Добавить добавление в корзину по id пользователя (в целом работу id с корзиной)
                # TODO Добавить вывод имени аккаунта куда-то в header
                # TODO Добавить кнопку удаление аккаунта
                # TODO Сделать новые кнопки и формы покрасивше

                if info[0].password == form.cleaned_data['password']:
                    Users.objects.filter(email=form.cleaned_data['email']).update(status="True")

                    return redirect('home')
                else:
                    context = {
                        'form': form,
                        'amount': amount,
                        'cart': cart,
                        'login': login,
                        'error': 'Такого аккаунта нет или данные введены неверно'
                    }

                    return render(request, 'main/entrance.html', context)
            except Exception:
                context = {
                    'form': form,
                    'amount': amount,
                    'cart': cart,
                    'login': login,
                    'error': 'Такого аккаунта нет или данные введены неверно'
                }

                return render(request, 'main/entrance.html', context)
        else:
            context = {
                'form': form,
                'amount': amount,
                'cart': cart,
                'login': login,
                'error': 'Введите вреный адрес электронной почты, используя @'
            }

            return render(request, 'main/entrance.html', context)

    context = {
        'form': form,
        'amount': amount,
        'cart': cart,
        'login': login,
        'error': ''
    }

    return render(request, 'main/entrance.html', context)


def registration(request):
    form = UsersRegisterForm()
    login = for_login()
    cart, amount = for_cart()

    if request.method == 'POST':
        # Отправка данных из формы регистрации
        form = UsersRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            Users.objects.filter(email=form.cleaned_data['email']).update(status="True")

            return redirect('home')
        else:
            context = {
                'form': form,
                'amount': amount,
                'cart': cart,
                'login': login,
                'error': 'Введите вреный адрес электронной почты, используя @'
            }

            return render(request, 'main/registration.html', context)

    context = {
        'form': form,
        'amount': amount,
        'cart': cart,
        'login': login,
        'error': ''
    }

    return render(request, 'main/registration.html', context)


def logout(request):
    Users.objects.update(status=False)

    return redirect('home')
