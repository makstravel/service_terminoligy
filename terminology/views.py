from datetime import date, datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models import RefBook, Version, Element
from .serializers import RefbookSerializer, ElementSerializer


class RefbookService:
    """
    сервис для работы со справочниками.
    """

    @staticmethod
    def get_active_refbooks(filter_date: date):
        """
        получает список справочников, актуальных на указанную дату.
        """
        return RefBook.objects.prefetch_related('versions').filter(
            versions__start_date__lte=filter_date  # фильтруем справочники по дате начала действия версии
        ).distinct()


class ElementService:
    """
    сервис для работы с элементами справочника.
    """

    @staticmethod
    def get_version(refbook: RefBook, version: str = None):
        """
        получение версии справочника.
        """
        if version:
            return refbook.versions.filter(version=version).first()  # ищем указанную версию
        return refbook.versions.filter(start_date__lte=date.today()).order_by('-start_date').first()  # берем актуальную

    @staticmethod
    def get_elements(refbook: RefBook, version: str = None):
        """
        получение элементов справочника по версии.
        """
        version_obj = ElementService.get_version(refbook, version)  # получаем объект версии
        return Element.objects.filter(version=version_obj) if version_obj else None  # фильтруем элементы по версии

    @staticmethod
    def validate_element(refbook: RefBook, code: str, value: str, version: str = None) -> bool:
        """
        проверяет наличие элемента в справочнике.
        """
        version_obj = ElementService.get_version(refbook, version)  # получаем объект версии
        return Element.objects.filter(version=version_obj, code=code, value=value).exists() if version_obj else False  # проверяем существование элемента


class RefbookListView(APIView):
    """
    представление для получения списка справочников.
    """

    @swagger_auto_schema(operation_description="получить все справочники")
    def get(self, request):
        """
        обрабатывает get-запрос для получения актуальных справочников на указанную дату.
        """
        date_str = request.query_params.get('date')  # получаем параметр даты из запроса
        if not date_str:
            return Response({"detail": "параметр 'date' обязателен."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()  # преобразуем строку в объект даты
        except ValueError:
            return Response({"detail": "Неправильный формат даты, используйте YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        refbooks = RefbookService.get_active_refbooks(filter_date)  # получаем актуальные справочники
        if not refbooks.exists():
            return Response({"detail": "Нет справочников, актуальных на указанную дату."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = RefbookSerializer(refbooks, many=True)
        return Response({"refbooks": serializer.data}, status=status.HTTP_200_OK)


class ElementListView(APIView):
    """
    получение элементов заданного справочника по версии.
    """

    @swagger_auto_schema(operation_description="Получение элементов по версии")
    def get(self, request, id):
        """
        обрабатывает get-запрос для получения элементов указанного справочника.
        """
        version = request.query_params.get("version")  # получаем версию из запроса

        try:
            refbook = RefBook.objects.get(id=id)  # ищем справочник по id
        except RefBook.DoesNotExist:
            return Response({'error': 'Справочник не найден'}, status=status.HTTP_404_NOT_FOUND)

        elements = ElementService.get_elements(refbook, version)  # получаем элементы
        if elements is None:
            return Response({'error': 'Элемент справочника не найдена'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ElementSerializer(elements, many=True)
        return Response({'elements': serializer.data}, status=status.HTTP_200_OK)


class ValidateElementView(APIView):
    """
    валидация элемента справочника.
    """

    @swagger_auto_schema(operation_description="Проверка наличия элемента в справочнике")
    def get(self, request, id):
        """
        обрабатывает get-запрос для проверки наличия элемента в справочнике.
        """
        code = request.query_params.get('code')  # получаем код элемента
        value = request.query_params.get('value')  # получаем значение элемента
        version = request.query_params.get('version')  # получаем версию

        if not code or not value:
            return Response({'error': "Оба параметра 'code' и 'value' обязательны"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            refbook = RefBook.objects.get(id=id)  # ищем справочник по id
        except RefBook.DoesNotExist:
            return Response({'error': 'Справочник не найден'}, status=status.HTTP_404_NOT_FOUND)

        is_valid = ElementService.validate_element(refbook, code, value, version)  # проверяем существование элемента
        return Response({'is_valid': is_valid}, status=status.HTTP_200_OK)
