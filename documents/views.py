import requests
from rest_framework.views import APIView
from .models import Documents
from datetime import date
from django.http import HttpResponse, JsonResponse

SEARCH_TYPES = ['doc_type', 'date', 'number', 'doc_type_and_date']


class DocumentsView(APIView):
    @staticmethod
    def post(request):
        """
        UPDATE or CREATE documents from db.
        :param request: list of dicts with numbers(required), type and date(e.g."2020-06-01"). e.g.
            {
                "documents": [
                    {
                        "number": "1",
                        "type": "PDF",
                        "date": "2020-06-10"
                    },
                    {
                        "number": "2",
                        "type": "PDF",
                        "date": "2020-06-10"
                    }
                ]
            }
        :return:
        """
        documents = request.data.get('documents')
        for document in documents:
            if document.get('date'):
                document['date'] = date.fromisoformat(document.get('date'))
        try:
            Documents.put_batch(*documents)
        except Exception as e:
            return HttpResponse(status=400)
        return HttpResponse()

    @staticmethod
    def delete(request):
        """
        DELETE documents from db.
        :param request: list of dicts with numbers of documents to delete. e.g.
            {
                "documents": [
                    {
                        "number": "1"
                    },
                    {
                        "number": "2"
                    }
                ]
            }
        :return:
        """
        documents = request.data.get('documents')
        try:
            with Documents.Table.table.batch_writer() as writer:
                for doc in documents:
                    writer.delete_item(Key=doc)
        except Exception as e:
            return HttpResponse(status=400)

        return HttpResponse()

    def get(self, request):
        """
        GET documents filtered by number, date, doc_type, doc_type_and_date
        Possible number, date filters: eq, gte, lte, between, in.
        """
        search_type = request.data.get('search_type')
        search_data = request.data.get('search_data')
        search_data_fun = request.data.get('search_data_fun')
        search_data_type = request.data.get('search_data_type')
        documents_json = {}

        if search_type not in SEARCH_TYPES:
            return HttpResponse(f'{search_type} not in possible search types', status=400)

        if search_type == 'doc_type':
            if type(search_data) == list:
                documents = list(Documents.scan(type__is_in=search_data))
            else:
                documents = list(Documents.scan(type=search_data))
            if documents:
                documents_json = self.list_to_json(documents)

        elif search_type == 'date':
            search_data = request.data.get('search_data')
            documents_json = self.search_date(search_data_fun, search_data)

        elif search_type == 'number':
            search_data = request.data.get('search_data')
            documents_json = self.search_number(search_data_fun, search_data)

        elif search_type == 'doc_type_and_date':

            documents_json = self.search_date_and_type(search_data_fun, search_data_type, search_data)
        if type(documents_json) == HttpResponse:
            return documents_json
        return JsonResponse(documents_json)

    @staticmethod
    def list_to_json(data_list):
        if data_list:
            json_items = []
            for item in data_list:
                json_items.append(
                    dict(
                        number=item.number,
                        date=item.date.strftime("%Y-%m-%d") if item.date else "",
                        type=item.type if item.type else "",
                    )
                )
            return dict(documents=json_items)
        else:
            return {}

    def search_date(self, search_date, search):
         # search in db by date possible search_functions: eq, gte, lte, between, in
        documents = []
        if search_date == 'eq':
            documents = list(Documents.scan(date=search))
        elif search_date == 'gte':
            documents = list(Documents.scan(date__gt=search))
        elif search_date == 'lte':
            documents = list(Documents.scan(date__lt=search))
        elif search_date == 'between':
            if type(search) == list:
                documents = list(Documents.scan(date__between=search))
            else:
                return HttpResponse(content=f'No list for between provided', status=400)
        elif search_date == 'in':
            if type(search) == list:
                documents = list(Documents.scan(date__is_in=search))
            else:
                return HttpResponse(content=f'No list for in provided', status=400)
        if documents:
            return self.list_to_json(documents)
        return {}

    def search_number(self, search_data_fun, search_data):
        # search in db by number possible search_functions: eq, gte, lte, between, in
        documents = []
        if search_data_fun == 'eq':
            documents = list(Documents.scan(number=search_data))
        elif search_data_fun == 'gte':
            documents = list(Documents.scan(number__gt=search_data))
        elif search_data_fun == 'lte':
            documents = list(Documents.scan(number__lt=search_data))
        elif search_data_fun == 'between':
            if type(search_data) == list:
                documents = list(Documents.scan(number__between=search_data))
            else:
                return HttpResponse(content=f'No list for between provided', status=400)
        elif search_data_fun == 'in':
            if type(search_data) == list:
                documents = list(Documents.scan(number__is_in=search_data))
            else:
                return HttpResponse(content=f'No list for in provided', status=400)
        if documents:
            return self.list_to_json(documents)
        return {}

    def search_date_and_type(self, search_date_type, search_type_data, search_date_data):
        documents = []
        # search in db by date and type of documents. Possible search_functions: eq, gte, lte, between, in
        if search_date_type == 'eq':
            documents = list(Documents.scan(date=search_date_data, type=search_type_data))

        elif search_date_type == 'gte':
            documents = list(Documents.scan(date__gt=search_date_data, type=search_type_data))
        elif search_date_type == 'lte':
            documents = list(Documents.scan(date__lt=search_date_data, type=search_type_data))
        elif search_date_type == 'between':
            if type(search_date_data) == list:
                documents = list(Documents.scan(date__between=search_date_data, type=search_type_data))
            else:
                return HttpResponse(content=f'No list for between provided', status=400)
        elif search_date_type == 'in':
            if type(search_date_data) == list:
                documents = list(Documents.scan(date__is_in=search_date_data, type=search_type_data))
            else:
                return HttpResponse(content=f'No list for in provided', status=400)
        if documents:
            return self.list_to_json(documents)
        return {}

    @staticmethod
    def send_message(data):
        # change url and add secrets for messaging third party
        requests.post(
            "http://127.0.0.1:8000/api/documents/",
            data=data
        )