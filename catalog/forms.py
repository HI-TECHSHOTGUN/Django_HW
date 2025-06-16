from django.forms import ModelForm, ValidationError

from catalog.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'photo', 'category', 'price',]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание'
        })
        self.fields['photo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Добавьте фотографию'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите категорию'
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите цену'
        })

    bad_words = [
        "казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно",
        "обман", "полиция", "радар"
    ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        for word in self.bad_words:
            word_lower = word.lower()
            if name and word_lower in name.lower():
                raise ValidationError(f"В названии нельзя использовать слово '{word}'.")
            if description and word_lower in description.lower():
                raise ValidationError(f"В описании нельзя использовать слово '{word}'.")

        return cleaned_data

    def clean_price(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')

        if price <= 0:
            raise ValidationError('Цена не может быть отрицательной или равна нулю')

        if isinstance(price, int):
            raise ValidationError(f'Цена не может быть не число{type(price)}')

        cleaned_data['price'] = price
        return cleaned_data