# Budget Manager

## Setup

- `urls.py`:
  ```Python
  urlpatterns = [
    path('budgetmanager/', include('budgetmanager.urls')),
  ]
  ```

- `settings.py`:
  ```Python
  INSTALLED_APPS = [
    'budgetmanager',
    'rest_framework',
    'knox',
  ]
  ```
  - To disable the browsable API:
    ```Python
    REST_FRAMEWORK = {
      'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
      )
    }
    ```
