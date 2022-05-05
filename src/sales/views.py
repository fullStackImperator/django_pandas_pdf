from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
import pandas as pd
# Create your views here.

def home_view(request):
    sales_df = None
    positions_df = None
    form = SalesSearchForm(request.POST or None)

    if request.method == 'POST':
        date_from = request.POST.get('date_from')  
        date_to = request.POST.get('date_to') 
        chart_type = request.POST.get('chart_type')   
        # print(date_from,date_to,chart_type)

        # qs = Sale.objects.all()
        qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(qs) > 0:
            sales_df = pd.DataFrame(qs.values())
            positions_data = []
            for sale in qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                    }

                    positions_data.append(obj) 
        
            positions_df= pd.DataFrame(positions_data)
            print('position df')
            print(positions_df)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            # print(sales_df)
        else: 
            print('no data')

        # obj = Sale.objects.get(id=1)
        # obj2 = qs2.get(id=1)
        # print(qs)
        # # print(obj)
        # # print(obj2)
        # print(qs.values())
        # print(qs.values_list())
        # print('###################!')
        # # df1 = pd.DataFrame(qs.values())
        # print(df1)
        # print('###################')
        # df2 = pd.DataFrame(qs.values_list())
        # print(df2)
        # # print('###################')


    context = {'form': form, 'sales_df': sales_df, 'positions_df':positions_df}
    return render(request, 'sales/home.html', context)

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'
    # context_object_name = 'qs'  --> means use qs in template to loop through list instead of object_list

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'   