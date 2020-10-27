from medstore.models import Company, CompanyBank, Medicine, MedicalDetails
from medstore.serializers import CompanySerializer, CompanyBankSerializer
from medstore.serializers import MedicineSerializer, MedicalDetailsSerializerSimple, MedicalDetailsSerializer
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class CompanyViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company,
                                       many=True, context={"request": request})
        response_dict = {"error": False,
                         "message": "All Company List Data",
                         "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CompanySerializer(data=request.data,
                                           context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response_dict = {"error": False,
                             "message":
                             "All Company Data Has Been Saved Successfully"}
        except:
            response_dict = {"error": True, "message":
                             "Error During saving of Company Data"}
        return Response(response_dict)


def update(self, request, pk=None):
    try:
        queryset = Company.objects.all()
        company = get_object_or_404(queryset, pk=pk)
        serializer = CompanySerializer(company, data=request.data,
                                       context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_dict = {"error": False, "message":
                         "Company Data Updated Successfully!"}
    except:
        response_dict = {"error": True, "message":
                         "Error Updating Company Data"}
    return Response(response_dict)


class CompanyBankViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = CompanyBankSerializer(data=request.data,
                                               context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_dict = {"error": False,
                             "message":
                             "All Company Bank Data Has Been Saved Successfully"}
        except:
            response_dict = {"error": True, "message":
                             "Error During saving of Company Bank Data"}
        return Response(response_dict)

    def list(self, request):
        companybank = CompanyBank.objects.all()
        serializer = CompanyBankSerializer(companybank,
                                           many=True, context={"request": request})
        response_dict = {"error": False,
                         "message": "All Company Bank List Data",
                         "data": serializer.data}
        return Response(response_dict)

    def retrieve(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset, pk=pk)
        serializer = CompanyBankSerializer(companybank, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})

    def update(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset, pk=pk)
        serializer = CompanyBankSerializer(
            companybank, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"error": False, "message": "Data Has Been Updated!"})


class CompanyNameViewset(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name=name)


class MedicineViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = MedicineSerializer(data=request.data,
                                            context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            medicine_id = serializer.data['id']
            # Access medicine serializer id
            # print(medicine_id)

            # adding and saving id from medicin
            medicaldetails_list = []

            for medicaldetail in request.data['medicaldetails']:
                # print(medicaldetail)
                medicaldetail["medicine_id"] = medicine_id
                medicaldetails_list.append(medicaldetail)
                # print(medicaldetail)

                serializer2 = MedicalDetailsSerializer(
                    data=medicaldetails_list, many=True, context={"request": request})
                serializer2.is_valid()
                serializer2.save()

            response_dict = {"error": False,
                             "message":
                             "All Medicine Data Has Been Saved Successfully"}
        except:
            response_dict = {"error": True, "message":
                             "Error During saving of  Medicine Data"}
        return Response(response_dict)

    def list(self, request):
        medicine = Medicine.objects.all()
        serializer = MedicineSerializer(medicine,
                                        many=True, context={"request": request})
        medicine_data = serializer.data
        new_medicine_list = []

        for medicine in medicine_data:
            medicaldetails = MedicalDetails.objects.filter(medicine_id=medicine["id"])
            medical_details_serializer = MedicalDetailsSerializerSimple(medicaldetails, many=True)
            medicine["medicaldetails"] = medical_details_serializer.data
            new_medicine_list.append(medicine)
        response_dict = {"error": False,
                         "message": "All Medicine  List Data",
                         "data": serializer.data}
        return Response(response_dict)

    def retrieve(self, request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk=pk)
        serializer = MedicineSerializer(medicine, context={"request": request})

        serializer_data = serializer.data
        medicaldetails = MedicalDetails.objects.filter(medicine_id=serializer_data["id"])
        medical_details_serializer = MedicalDetailsSerializerSimple(medicaldetails, many=True)
        serializer_data["medicaldetails"] = medical_details_serializer.data

        return Response({"error": False, "message": "Single Medicine Data Fetch", "data": serializer.data})

    def update(self, request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk=pk)
        serializer = MedicineSerializer(
            medicine, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"error": False, "message": "Medicine Data Has Been Updated!"})


company_list = CompanyViewset.as_view({"get": "list"})
company_create = CompanyViewset.as_view({"post": "create"})
company_update = CompanyViewset.as_view({"put": "update"})
