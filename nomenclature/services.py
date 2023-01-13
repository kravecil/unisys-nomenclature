# from nomenclature.models import Request
from django.conf import settings
import requests

def get_stats(objs):
    return {
        'products': objs.filter(approved_at__isnull=False).count(),
        'requests': objs.filter(approved_at__isnull=True).count()
    }

def get_user_by_auth_id(id):
    if id is None: return None
    try:
        response =  requests.get(
            settings.HOST_AUTH + '/api-local/user/%d' % id,
            headers={
                # 'Authorization': token,
                'Accept': 'application/json',
            }
        )

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print('Person: ошибка при получении сведений о пользователе')
        print(e)

    return None