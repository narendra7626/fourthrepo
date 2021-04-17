from django.shortcuts import render,redirect
from django.views.generic import TemplateView,DetailView,UpdateView,View,CreateView,FormView
from myapp.models import *
from django.urls import reverse,reverse_lazy
from myapp.forms import CheckoutForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# Create your views here.
class EcomMixin(object):
    def dispatch(self,request,*args,**kwargs):
        cart_id=request.session.get("cart_id")
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            if request.user.is_authenticated:
                cart_obj.customer=request.user.Customer
                cart_obj.save()
        return super().dispatch(request,*args,**kwargs)

def home(request):
    product=Product.objects.all()
    paginator=Paginator(product,3)
    page_number=request.GET.get('page')
    product_obj=paginator.get_page(page_number)
    return render(request,'index.html',{'product_list':product_obj})


def search(request):
    q=request.GET['q']
    product=Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request,'search.html',{'product_list':product})


class CategoryView(EcomMixin,TemplateView):
    template_name="cat_list.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['cat_list']=Category.objects.all().order_by('-id')
        return context

class CategoryProductList(EcomMixin,TemplateView):
    template_name="cat_product_list.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cat_slug=self.kwargs['slug']
        category=Category.objects.get(slug=cat_slug)
        context['category']=category
        context['category_product_list']=Product.objects.filter(category=category).order_by('-id')
        return context

class ProductDetail(EcomMixin,TemplateView):
    template_name="product_detail.html"
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        url_slug=self.kwargs['slug']
        product=Product.objects.get(slug=url_slug)
        related_products=Product.objects.filter(category=product.category).exclude(slug=url_slug)[:4]
        product.viewcount+=1
        product.save()
        context['product']=product
        context['related']=related_products
        return context


class Cart_Add(TemplateView):
    template_name="cart_add.html"
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        product_id=self.kwargs['pro_id']
        product_obj=Product.objects.get(id=product_id)
        cart_id=self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            this_product_in_cart=cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct=this_product_in_cart.last()
                cartproduct.quantity+=1
                cartproduct.subtotal+=product_obj.sell_price
                cartproduct.save()
                cart_obj.total+=product_obj.sell_price
                cart_obj.save()
            else:
                cartproduct=CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.sell_price,quantity=1,subtotal=product_obj.sell_price)
                cart_obj.total+=product_obj.sell_price
                cart_obj.save()

        else:
            cart_obj=Cart.objects.create(total=0)
            self.request.session['cart_id']=cart_obj.id
            cartproduct=CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.sell_price,quantity=1,subtotal=product_obj.sell_price)
            cart_obj.total=product_obj.sell_price
            cart_obj.save()


        return context

def mycart(request):
    cart=Cart.objects.all()
    return render(request,'mycart.html',{'cart':cart})






class ManageCartView(EcomMixin,View):
    def get(self,request,*args,**kwargs):
        cp_id=self.kwargs['cp_id']
        action=request.GET.get('action')
        cp_obj=CartProduct.objects.get(id=cp_id)
        cart_obj=cp_obj.cart

        if(action=="inc"):
            cp_obj.quantity+=1
            cp_obj.subtotal+=cp_obj.rate
            cp_obj.save()
            cart_obj.total+=cp_obj.rate
            cart_obj.save()
        elif(action=="dec"):
            cp_obj.quantity-=1
            cp_obj.subtotal-=cp_obj.rate
            cp_obj.save()
            cart_obj.total-=cp_obj.rate
            cart_obj.save()
            if(cp_obj.quantity==0):
                cp_obj.delete()

        elif(action=="rmv"):
            cart_obj.total -=cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()

        else:
            pass
        return redirect('mycart')

class EmptyCartView(View):
    def get(self,request,*args,**kwargs):
        cart_id=request.session.get("cart_id",None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total=0
            cart.save()
        return redirect('mycart')

class CheckOutView(LoginRequiredMixin,EcomMixin,CreateView):
    login_url='/login/'
    template_name="checkout.html"
    form_class=CheckoutForm
    success_url=reverse_lazy('home')


    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)

        else:
            cart_obj=None
        context['cart']=cart_obj
        return context

    def form_valid(self,form):
        cart_id=self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            form.instance.cart=cart_obj
            form.instance.subtotal=cart_obj.total
            form.instance.discount=0
            form.instance.total=cart_obj.total
            form.instance.order_status="Order Received"
            del self.request.session['cart_id']

        else:
            return redirect('home')
        return super().form_valid(form)
