from django.shortcuts import render, redirect
from django import views
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.db.models import Q, F, Sum, Count

from .models import Shop, Department, Item
from .forms import ComparedDepartmentsForm


class IndexView(views.View):
    def get(self, request):
        shops = Shop.objects.all()
        return render(request, 'index.html', context={'shops': shops})

    def post(self, request):
        return redirect('shop', shop_id=request.POST.get('shop'))


class ShopView(views.View):
    def get(self, request, shop_id):
        shop = Shop.objects.filter(id=shop_id).prefetch_related('departments').first()

        if not shop:
            return redirect('index')
        return render(request, 'shop.html', context={'shop': shop})


class ItemCreate(CreateView):
    template_name = 'item_add.html'
    model = Item
    fields = ['name', 'description', 'is_sold', 'price', 'comments']

    def form_valid(self, form):
        self.object = Item(department_id=self.kwargs['department_id'], **form.cleaned_data)
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('shop', args=[self.kwargs['shop_id']])


class ItemDelete(DeleteView):
    model = Item
    template_name = 'item_delete.html'
    pk_url_kwarg = 'item_id'

    def get_success_url(self):
        return reverse('shop', args=[self.kwargs['shop_id']])


class ItemUpdate(UpdateView):
    model = Item
    template_name = 'item_update.html'
    fields = ['name', 'description', 'is_sold', 'price', 'comments']
    pk_url_kwarg = 'item_id'

    def form_valid(self, form):
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('shop', args=[self.kwargs['shop_id']])


class DepartmentCreate(CreateView):
    model = Department
    fields = ['sphere', 'staff_amount']
    template_name = 'item_add.html'
    pk_url_kwarg = 'department_id'

    def form_valid(self, form):
        self.object = Department(shop_id=self.kwargs['shop_id'], **form.cleaned_data)
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('shop', args=[self.kwargs['shop_id']])


class DepartmentDelete(DeleteView):
    model = Department
    template_name = 'department_delete.html'
    pk_url_kwarg = 'department_id'

    def get_success_url(self):
        return reverse('shop', args=[self.kwargs['shop_id']])


class DepartmentUpdate(UpdateView):
    model = Department
    template_name = 'department_update.html'
    pk_url_kwarg = 'department_id'
    fields = ['sphere', 'staff_amount']

    def form_valid(self, form):
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('shop', args=[self.kwargs['shop_id']])


class ShopInfoView(DetailView):
    model = Shop
    template_name = 'shop_information.html'
    pk_url_kwarg = 'shop_id'


class ShopDelete(DeleteView):
    model = Shop
    template_name = 'shop_delete.html'
    pk_url_kwarg = 'shop_id'

    def get_success_url(self):
        return reverse('index')


class ShopUpdate(UpdateView):
    model = Shop
    template_name = 'shop_update.html'
    pk_url_kwarg = 'shop_id'
    fields = '__all__'

    def form_valid(self, form):
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


class FilteredItemsView(ListView):
    model = Item
    template_name = 'item_list.html'

    def get_queryset(self):
        choice: int = self.kwargs['number']

        result = self.model.objects.none()

        if choice == 1:
            result = Item.objects.filter(
                department__shop__name__startswith='К'
            )

        elif choice == 2:
            result = Item.objects.filter(
                price__gt=10,
                department__staff_amount__lt=50
            )

        elif choice == 3:
            result = Item.objects.filter(
                Q(price__gt=20) | Q(department__shop__staff_amount__gt=50)
            )

        elif choice == 4:
            result = Item.objects.filter(
                department_id__in=[1, 3, 5, 6]
            )

        elif choice == 5:
            result = Item.objects.filter(
                Q(price__gt=10, name__contains='а') | Q(price__lt=20, name__contains='о')
            )

        elif choice == 6:
            result = Item.objects.filter(
                price=F('department__staff_amount') + 10
            )

        return result


class FilteredShopsView(ListView):
    model = Shop
    template_name = 'shop_list.html'

    def get_queryset(self):
        choice: int = self.kwargs['number']

        result = self.model.objects.none()

        if choice == 1:
            result = Shop.objects.annotate(
                staff_all_deps=Sum('departments__staff_amount')
            ).filter(staff_amount=F('staff_all_deps'))

        elif choice == 2:
            result = Shop.objects.filter(
                departments__items__price__gte=5
            ).distinct()

        elif choice == 4:
            result = Shop.objects.annotate(
                add_info=Count(
                    'departments__items',
                    filter=Q(departments__items__price__lte=10) | Q(departments__items__name__contains='а')
                )
            )

        return result


class ComparedDepartmentsView(FormView):
    template_name = 'department_compare.html'
    form_class = ComparedDepartmentsForm
    success_url = 'TableComparedDepartments/'

    @staticmethod
    def choice_filter(department, choice: int):
        result = 0

        if choice == 0:
            result = department.staff_amount

        elif choice == 1:
            result = department.items.filter(is_sold=True).aggregate(Sum('price'))
            result = result.get('price__sum')

        elif choice == 2:
            result = department.items.filter(is_sold=False).aggregate(Sum('price'))
            result = result.get('price__sum')

        elif choice == 3:
            result = department.items.aggregate(Sum('price'))
            result = result.get('price__sum')

        elif choice == 4:
            result = department.items.filter(is_sold=True).aggregate(Count('id'))
            result = result.get('id__count')

        elif choice == 5:
            result = department.items.filter(is_sold=False).aggregate(Count('id'))
            result = result.get('id__count')

        elif choice == 6:
            result = department.items.aggregate(Count('id'))
            result = result.get('id__count')

        result = 0 if result is None else result

        return result

    def form_valid(self, form):
        main = form.cleaned_data.get('main')
        secondary = form.cleaned_data.get('secondary')
        criteria_id = form.cleaned_data.get('criteria')
        all_criteria = form.fields['criteria']
        lst = []
        for i in criteria_id:
            lst.append([
                all_criteria.choices[int(i)][1],
                self.choice_filter(main, int(i)),
                self.choice_filter(secondary, int(i))
            ])
        return render(self.request, 'department_table.html', context={
            'main': main,
            'secondary': secondary,
            'lst': lst
        })


class DisabledView(TemplateView):
    template_name = 'disabled.html'
