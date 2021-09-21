from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

ORDER_CHOICES = (
    ("1", 'Take Away'),
    ("2", 'Delivery'),
    ("3", 'Instant')
)


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
    order_type = forms.ChoiceField(choices=ORDER_CHOICES)
