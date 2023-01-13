# ЕИС номенклатура

Работа со информационной базой номенклатуры: добавление, хранение, изменение, поиск
<br />
<br />
<br />
## Перед началом

- Создать виртуальное окружение **poetry env use python**. Все команды python выполнять в созданной виртуальной среде (**poetry shell**).
- Установить необходимые пакеты **poetry install**, **yarn**.
- __(необязательно)__ Создать и применить миграции **python manage.py makemigrations**, **python manage.py migrate**.
- __(необязательно)__ Создать пользователя панели администратора **python manage.py createsuperuser**.

## Изменить настройки для своего проекта

- Заменить **dev.mkvityaz.ru** на своё значение host в файлах __settings.py__ и __vite.config.js__.
- Поменять значение константы **ALLOWED_HOSTS** в __settings.py__.
- В __Header.vue__ прописать своё наименование и версию веб-приложения.

## Запуск в development

Запустить в отдельных процессах в указанном порядке:

- yarn dev
- python manage.py runserver --insecure

## Подготовка в production:

- yarn build
- python manage.py collectstatic

<br />
<br />

## Скриншоты

![Страница создания заявки](/readme/Screenshot_01.png)