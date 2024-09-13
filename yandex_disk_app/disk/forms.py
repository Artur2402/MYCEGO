from django import forms
import urllib.parse


class PublicKeyForm(forms.Form):
  CATEGORY_CHOICES = (
    ('all', 'Все'),
    ('archive', 'Архивы'),
    ('document', 'Документы'),
    ('image', 'Изображения'),
    ('media', 'Медиа файлы'),
    ('executable', "Исполняемые файлы")
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

# Функция извлечения public_key из ссылки.
  def clean_public_key(self):
    public_key = self.cleaned_data.get('public_key')
    try:
      parsed_url = urllib.parse.urlparse(public_key)
      query_params = urllib.parse.parse_qs(parsed_url.query)

      # Извлечение значения public_key
      if 'public_key' in query_params:
        return query_params['public_key'][0]
      else:
        raise forms.ValidationError('Ссылка не содержит public_key')
    except Exception as e:
      raise forms.ValidationError(f'Ошибка обработки ссылки: {e}')