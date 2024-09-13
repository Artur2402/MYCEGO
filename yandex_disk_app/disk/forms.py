from django import forms
import urllib.parse


class PublicKeyForm(forms.Form):
  CATEGORY_CHOICES = (
    ('all', 'Все'),
    ('archive', 'Архивы'),
    ('document', 'Документы'),
    ('image', 'Изображения'),
    ('media', 'Медиа файлы')
  )

  public_key = forms.CharField(
    label='Публичная ссылка',
    max_length=256,
    help_text='Введите публичную ссылку на ресурс.',
    required=True
  )
  filter = forms.ChoiceField(
    label='Фильтр',
    choices=CATEGORY_CHOICES,
    help_text='Выберите тип файла для отображения'
  )
  max_files = forms.IntegerField(
    label='Максимум файлов',
    min_value=1,
    required=False,
    help_text='Введите максимальное кол-во файлов для отображения. Оставьте пустым для отображения всех файлов'
  )

  def clean_public_key(self):
    pass