from django import forms
from produtc.models import Product, ProductReview


class NewProductForms(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput())

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'category', 'address', 'phone_number', 'tg_username')

    def save(self, request, commit=True):
        product = self.instance
        product.author = request.user
        super().save(commit)
        return product

    def __init__(self, *args, **kwargs):
        super(NewProductForms, self).__init__(*args, **kwargs)
        # Add placeholder and class in input
        self.fields['images'].widget.attrs.update({'multiple': True})


class UpdateProductForms(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput())

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'category', 'address', 'phone_number', 'tg_username')

    def __init__(self, *args, **kwargs):
        super(UpdateProductForms, self).__init__(*args, **kwargs)
        # Add placeholder and class in input
        self.fields['images'].widget.attrs.update({'multiple': True})



class ProductReviewForms(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Sizning sharhingiz'}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
