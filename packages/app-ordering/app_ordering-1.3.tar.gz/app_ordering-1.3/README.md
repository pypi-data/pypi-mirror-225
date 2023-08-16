# Django admin app ordering

**Django admin app ordering** is a Django app to able ordering apps and models in the Django admin site, it also support to toggle visiblity app or model.

Summary this are features:
- Sorting admin app, models.
- Toggle visibility admin app, models.
- Configure sorting/visibility app(model) for certain users or groups.

![screenshot](https://raw.githubusercontent.com/kajalagroup/django-admin-app-ordering/develop/screenshot.png)


## Install

```
pip install app_ordering
```

Add "app_ordering" and "adminsortable2" to app list:

```
INSTALLED_APPS = [
    ....
    "app_ordering",
    "adminsortable2"
]
````

**adminsortable2** is third party to help you to manipulate sorting easier.

Add get_package_template_dir("app_ordering") to TEMPLATES.DIR
Remember to import get_package_template_dir in the settings.py

```
from app_ordering.helpers import get_package_template_dir
```

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [
            get_package_template_dir("app_ordering"),
        ],
        ...
    },
]
```


## Profile:
- Default profile will be used as default if you don't set any specific profile for logged in user.


## Extend template:

If you want to custom app_list.html, better you should take a look at *app_ordering/templates/admin/app_list.html* and custom based on that