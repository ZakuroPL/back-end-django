from django.views.decorators.csrf import csrf_exempt
from rest_framework import  viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.http import JsonResponse

from .models import Product, Location, Transfer, HistoryOfTransfer, HistoryOfLoginToZakuro
from .serializers import ProductSerializer, LocationSerializer, TransferSerializer, UserSerializer, \
    HistoryOfTransferSerializer, HistoryOfLoginToZakuroSerializer
from django.core.mail import send_mail

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['POST'])
    def add_transfer(self, request, pk=None):
            locationFrom = request.data['locationFrom']
            locationFromId = Location.objects.get(id=locationFrom)
            locationTo = Location.objects.get(id=pk)
            product = request.data['product']
            thisProduct = Product.objects.get(id=product)
            pcs = request.data['pcs']
            user = request.user
            intPcs = int(pcs)
            if locationTo.id == 1 and locationFromId.id == 1:    # supply
                try:
                    transfer = Transfer.objects.get(location=locationTo, product=thisProduct)
                    transfer.pcs = intPcs + transfer.pcs
                    transfer.user = user
                    transfer.save()
                    HistoryOfTransfer.objects.create(product=thisProduct, locationFrom=locationFromId,
                                                     locationTo=locationTo, pcs=pcs, user=user)
                    response = {'message: ' 'transfer was updated'}
                    return Response(response, status=status.HTTP_200_OK)
                except:
                    Transfer.objects.create(product=thisProduct, location=locationTo, pcs=pcs, user=user)
                    HistoryOfTransfer.objects.create(product=thisProduct, locationFrom=locationFromId,
                                                     locationTo=locationTo, pcs=pcs, user=user)
                    response = {'message: ' 'transfer was created'}
                    return Response(response, status=status.HTTP_200_OK)
            elif locationTo.id == 2 and locationFromId.id == 2:    # packing
                    transfer = Transfer.objects.get(location=locationTo, product=thisProduct)
                    transfer.user = user
                    if transfer.pcs >= intPcs:
                        transfer.pcs = transfer.pcs - intPcs
                        transfer.save()
                        HistoryOfTransfer.objects.create(product=thisProduct, locationFrom=locationFromId,
                                                         locationTo=locationTo, pcs=pcs, user=user)
                        response = {'message: ' 'transfer was updated'}
                        return Response(response, status=status.HTTP_200_OK)
                    else:
                        response = {'message: ' 'You want to transfer more than you have'}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    transfer = Transfer.objects.get(location=locationTo, product=thisProduct)
                    transfer.pcs = intPcs + transfer.pcs
                    transfer.user = user
                    transfer.save()
                    HistoryOfTransfer.objects.create(product=thisProduct, locationFrom=locationFromId,
                                                     locationTo=locationTo, pcs=pcs, user=user)
                    transfer2 = Transfer.objects.get(location=locationFromId, product=thisProduct)
                    transfer2.pcs = transfer2.pcs - intPcs
                    transfer2.user = user
                    transfer2.save()
                    response = {'message: ' 'transfer was updated'}
                    return Response(response, status=status.HTTP_200_OK)
                except:
                    Transfer.objects.create(product=thisProduct, location=locationTo, pcs=pcs, user=user)
                    HistoryOfTransfer.objects.create(product=thisProduct, locationFrom=locationFromId,
                                                     locationTo=locationTo, pcs=pcs, user=user)
                    transfer2 = Transfer.objects.get(location=locationFromId, product=thisProduct)
                    transfer2.pcs = transfer2.pcs - intPcs
                    transfer2.user = user
                    transfer2.save()
                    response = {'message: ' 'transfer was created'}
                    return Response(response, status=status.HTTP_200_OK)


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        response = {'message: ' 'you cant update transfer like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message: ' 'you cant create transfer like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = HistoryOfTransfer.objects.all()
    serializer_class = HistoryOfTransferSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
# //////////////////FOR ZAKURO/////////////////////////////////////////////////////
class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(Login, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        try:
            HistoryOfLoginToZakuro.objects.create(user=user)
            send_mail(f'{user.username} zalogował się do Zakuro',
                      f'Użytkownik: {user.username}',
                      'zakuro.developer@gmail.com',
                      ['granatowski.d@gmail.com'],
                      fail_silently=False)
            return Response(token.key)
        except:
            response = {'message: ' 'History of login wasnt saved'}
            return Response(response)




class HistoryOfLoginToZakuroViewSet(viewsets.ModelViewSet):
    queryset = HistoryOfLoginToZakuro.objects.all()
    serializer_class = HistoryOfLoginToZakuroSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


@csrf_exempt
def send_email(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    try:
        send_mail(f'{name} wysłał wiadomość z Zakuro',
                  f'adres: {email}/// wiadomość: {message}',
                  'zakuro.developer@gmail.com',
                  ['granatowski.d@gmail.com'],
                  fail_silently=False)
        send_mail('Thanks for contact with Zakuro',
                  'Hi. I will response as soon as possible.',
                  'zakuro.developer@gmail.com',
                  [f'{email}'],
                  fail_silently=False)
        return JsonResponse({'message':'email sent'})
    except:
        return JsonResponse({'message':'email not sent'})
# //////////////////FOR DENTIST/////////////////////////////////////////////////////




