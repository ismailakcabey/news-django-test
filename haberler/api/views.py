import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from haberler.models import Makale, Gazeteci
from haberler.api.serializers import (
    MakaleSerializer,
    GazeteciSerializer,
    MakaleSerializerGet,
)
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


class GazeteciView(APIView):
    def get(self, request):
        gazeteciler = Gazeteci.objects.filter()
        serializer = GazeteciSerializer(
            gazeteciler, many=True, context={"request": request}
        )
        return Response({"message": "başarılı", "data": serializer.data})

    def post(self, request):
        gazeteci = GazeteciSerializer(data=request.data)
        if gazeteci.is_valid():
            gazeteci.save()
            return Response(
                {"message": "başarılı", "data": gazeteci.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "failed", "error": gazeteci.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GazeteciDetailView(APIView):

    def get_object(self, pk):
        gazeteci_instance = get_object_or_404(Gazeteci, pk=pk)
        return gazeteci_instance

    def merged_object(self, model, request_data):
        makale_dict = model.__dict__
        concet = {**makale_dict, **request_data}
        return concet

    def get(self, request, pk):
        gazeteci = self.get_object(pk=pk)
        serializer = GazeteciSerializer(gazeteci)
        return Response(
            {"message": "başarılı", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        gazeteci = self.get_object(pk=pk)
        gazeteci.delete()
        return Response(
            {"message": "başarılı", "data": "silindi"}, status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        gazeteci = self.get_object(pk=pk)
        concet = self.merged_object(gazeteci, request_data=request.data)
        serializer = GazeteciSerializer(instance=gazeteci, data=concet)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "başarılı", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "failed", "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MakaleView(APIView):
    def get(self, request):
        makaleler = Makale.objects.filter(aktif=True)
        serializer = MakaleSerializerGet(
            makaleler, many=True, context={"request": request}
        )
        return Response({"message": "başarılı", "data": serializer.data})

    def post(self, request):
        makale = MakaleSerializer(data=request.data)
        if makale.is_valid():
            makale.save()
            return Response(
                {"message": "başarılı", "data": makale.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "failed", "error": makale.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MakaleDetailView(APIView):

    def get_object(self, pk):
        makale_instance = get_object_or_404(Makale, pk=pk)
        return makale_instance

    def merged_object(self, model, request_data):
        makale_dict = model.__dict__
        concet = {**makale_dict, **request_data}
        return concet

    def get(self, request, pk):
        makale = self.get_object(pk=pk)
        serializer = MakaleSerializer(makale)
        return Response(
            {"message": "başarılı", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        makale = self.get_object(pk=pk)
        makale.delete()
        return Response(
            {"message": "başarılı", "data": "silindi"}, status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        makale = self.get_object(pk=pk)
        concet = self.merged_object(makale, request_data=request.data)
        serializer = MakaleSerializer(instance=makale, data=concet)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "başarılı", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "failed", "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


## __ FUNCTIONS METHOD __ ##

# @api_view(["GET"])
# def makale_list_api_view(request):
#     makaleler = Makale.objects.filter(aktif=True)
#     serializer = MakaleSerializer(makaleler, many=True)
#     print(serializer.data)
#     return Response({"message": "başarılı", "data": serializer.data})


# @api_view(["POST"])
# def makale_create_api_view(request):
#     makale = MakaleSerializer(data=request.data)
#     if makale.is_valid():
#         makale.save()
#         return Response(
#             {"message": "başarılı", "data": makale.data}, status=status.HTTP_201_CREATED
#         )
#     else:
#         return Response({"message": "hata alindi"}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def makale_get_by_id_api_view(request, id):
#     try:
#         makale = Makale.objects.get(pk=id)
#         serializer = MakaleSerializer(makale)
#         return Response(
#             {"message": "başarılı", "data": serializer.data}, status=status.HTTP_200_OK
#         )
#     except Makale.DoesNotExist:
#         return Response(
#             status=status.HTTP_404_NOT_FOUND, data={"data": f"not found data {id}"}
#         )


# @api_view(["DELETE"])
# def makale_delete_by_id_api_view(request, id):
#     try:
#         makale = Makale.objects.get(pk=id)
#         makale.delete()
#         return Response(
#             {"message": "başarılı", "data": "silindi"}, status=status.HTTP_200_OK
#         )
#     except Makale.DoesNotExist:
#         return Response(
#             status=status.HTTP_404_NOT_FOUND, data={"data": f"not found data {id}"}
#         )


# @api_view(["PATCH"])
# def makale_update_api_view(request, id):
#     try:
#         makale = Makale.objects.get(pk=id)
#         makale_dict = makale.__dict__
#         concet = {**makale_dict, **request.data}
#         serializer = MakaleSerializer(instance=makale, data=concet)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "başarılı", "data": serializer.data},
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response({"message": "failed"}, status=status.HTTP_400_BAD_REQUEST)
#     except Makale.DoesNotExist:
#         return Response(
#             status=status.HTTP_404_NOT_FOUND, data={"data": f"not found data {id}"}
#         )
