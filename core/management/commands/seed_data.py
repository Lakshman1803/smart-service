"""
SMART REPAIR — Complete Seed: 99 AP centers, repair issues, service types, workers, holidays
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from datetime import date, time, timedelta


class Command(BaseCommand):
    help = 'Seed all SMART REPAIR data for Andhra Pradesh'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Seeding SMART REPAIR...'))
        self.create_service_centers()
        self.create_service_types()
        self.create_repair_issues()
        self.create_holidays()
        self.create_admin()
        self.create_employees_and_workers()
        self.create_time_slots()
        self.stdout.write(self.style.SUCCESS('✅ All done!'))

    # ─────────────────────────────────────────────────────────────────────────
    # SERVICE CENTERS — 99 across AP
    # ─────────────────────────────────────────────────────────────────────────
    def create_service_centers(self):
        from core.models import ServiceCenter
        centers = [
            # KRISHNA (8)
            {'name':'SMART REPAIR - Vijayawada MG Road','address':'42 MG Road Governorpet','city':'Vijayawada','district':'Krishna','pincode':'520002','phone':'8885410010','email':'vjw.mg@smartrepair.in','latitude':16.5062,'longitude':80.6480,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Ravi Kumar','total_bays':15,'established_year':2015},
            {'name':'SMART REPAIR - Vijayawada Benz Circle','address':'Shop 12 Benz Circle Junction','city':'Vijayawada','district':'Krishna','pincode':'520010','phone':'8885410011','email':'vjw.benz@smartrepair.in','latitude':16.5193,'longitude':80.6281,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Suresh Babu','total_bays':12,'established_year':2017},
            {'name':'SMART REPAIR - Vijayawada Auto Nagar','address':'78 Auto Nagar Industrial Area','city':'Vijayawada','district':'Krishna','pincode':'520007','phone':'8885410012','email':'vjw.auto@smartrepair.in','latitude':16.5480,'longitude':80.6750,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Naresh Reddy','total_bays':20,'established_year':2015},
            {'name':'SMART REPAIR - Vijayawada Gandhinagar','address':'15 Gandhinagar Main Road','city':'Vijayawada','district':'Krishna','pincode':'520003','phone':'8885410013','email':'vjw.gandhi@smartrepair.in','latitude':16.4974,'longitude':80.6600,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Prasad Varma','total_bays':10,'established_year':2018},
            {'name':'SMART REPAIR - Vijayawada Patamata','address':'22 Patamata Main Road','city':'Vijayawada','district':'Krishna','pincode':'520010','phone':'8885410014','email':'vjw.patamata@smartrepair.in','latitude':16.5120,'longitude':80.6200,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Srinivas Rao','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Vijayawada Kanuru','address':'14 Kanuru Road','city':'Vijayawada','district':'Krishna','pincode':'520007','phone':'8885410015','email':'vjw.kanuru@smartrepair.in','latitude':16.5300,'longitude':80.6900,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Venkata Rao','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Machilipatnam','address':'34 Bandar Road Near Bus Stand','city':'Machilipatnam','district':'Krishna','pincode':'521001','phone':'8885410016','email':'machilipatnam@smartrepair.in','latitude':16.1875,'longitude':81.1345,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Chandrasekhar','total_bays':10,'established_year':2018},
            {'name':'SMART REPAIR - Gudivada','address':'12 NH-9 Gudivada Town','city':'Gudivada','district':'Krishna','pincode':'521301','phone':'8885410017','email':'gudivada@smartrepair.in','latitude':16.4335,'longitude':80.9919,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Satish Kumar','total_bays':8,'established_year':2019},
            # GUNTUR (6)
            {'name':'SMART REPAIR - Guntur Brodipet','address':'88 Brodipet Main Road','city':'Guntur','district':'Guntur','pincode':'522002','phone':'8885420010','email':'guntur.brodi@smartrepair.in','latitude':16.3067,'longitude':80.4365,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Ramachandra Rao','total_bays':12,'established_year':2016},
            {'name':'SMART REPAIR - Guntur Arundelpet','address':'12 Arundelpet Circle','city':'Guntur','district':'Guntur','pincode':'522002','phone':'8885420011','email':'guntur.arundel@smartrepair.in','latitude':16.3100,'longitude':80.4400,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Kishore Babu','total_bays':10,'established_year':2017},
            {'name':'SMART REPAIR - Amaravati Capital','address':'1 Capital Region Boulevard','city':'Amaravati','district':'Guntur','pincode':'522503','phone':'8885420012','email':'amaravati@smartrepair.in','latitude':16.5150,'longitude':80.5160,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Madhava Rao','total_bays':18,'established_year':2019},
            {'name':'SMART REPAIR - Tenali','address':'45 Old Bus Stand Road','city':'Tenali','district':'Guntur','pincode':'522201','phone':'8885420013','email':'tenali@smartrepair.in','latitude':16.2426,'longitude':80.6389,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Bhaskara Rao','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Narasaraopet','address':'23 Market Street','city':'Narasaraopet','district':'Guntur','pincode':'522601','phone':'8885420014','email':'narasaraopet@smartrepair.in','latitude':16.2345,'longitude':80.0534,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Naga Raju','total_bays':8,'established_year':2021},
            {'name':'SMART REPAIR - Piduguralla','address':'7 NH-65 Piduguralla','city':'Piduguralla','district':'Guntur','pincode':'522413','phone':'8885420015','email':'piduguralla@smartrepair.in','latitude':16.4774,'longitude':79.8888,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Siva Prasad','total_bays':6,'established_year':2022},
            # VISAKHAPATNAM (6)
            {'name':'SMART REPAIR - Visakhapatnam Dwaraka Nagar','address':'34 Dwaraka Nagar Main Road','city':'Visakhapatnam','district':'Visakhapatnam','pincode':'530016','phone':'8885430010','email':'vizag.dwaraka@smartrepair.in','latitude':17.7384,'longitude':83.3377,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Anand Krishna','total_bays':14,'established_year':2016},
            {'name':'SMART REPAIR - Visakhapatnam MVP Colony','address':'56 MVP Colony Sector 6','city':'Visakhapatnam','district':'Visakhapatnam','pincode':'530017','phone':'8885430011','email':'vizag.mvp@smartrepair.in','latitude':17.7500,'longitude':83.3200,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Phani Kumar','total_bays':12,'established_year':2017},
            {'name':'SMART REPAIR - Visakhapatnam Gajuwaka','address':'23 Main Road Gajuwaka','city':'Visakhapatnam','district':'Visakhapatnam','pincode':'530026','phone':'8885430012','email':'vizag.gajuwaka@smartrepair.in','latitude':17.6800,'longitude':83.2100,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Murali Krishna','total_bays':10,'established_year':2018},
            {'name':'SMART REPAIR - Visakhapatnam Steel Plant Road','address':'9 Steel Plant Road Ukkunagaram','city':'Visakhapatnam','district':'Visakhapatnam','pincode':'530032','phone':'8885430013','email':'vizag.steel@smartrepair.in','latitude':17.6868,'longitude':83.2185,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Satyanarayana','total_bays':16,'established_year':2016},
            {'name':'SMART REPAIR - Visakhapatnam Madhurawada','address':'67 Madhurawada Junction NH-16','city':'Visakhapatnam','district':'Visakhapatnam','pincode':'530041','phone':'8885430014','email':'vizag.madhu@smartrepair.in','latitude':17.7840,'longitude':83.3750,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Venkata Rao','total_bays':12,'established_year':2019},
            {'name':'SMART REPAIR - Bheemunipatnam','address':'14 Beach Road Bheemunipatnam','city':'Bheemunipatnam','district':'Visakhapatnam','pincode':'531163','phone':'8885430015','email':'bheemunipatnam@smartrepair.in','latitude':17.8904,'longitude':83.4502,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Kiran Babu','total_bays':8,'established_year':2021},
            # EAST GODAVARI (6)
            {'name':'SMART REPAIR - Kakinada Main','address':'23 Main Road Near Collectorate','city':'Kakinada','district':'East Godavari','pincode':'533001','phone':'8885440010','email':'kakinada@smartrepair.in','latitude':16.9891,'longitude':82.2475,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Sekhar Babu','total_bays':10,'established_year':2017},
            {'name':'SMART REPAIR - Kakinada Port Road','address':'45 Port Road','city':'Kakinada','district':'East Godavari','pincode':'533003','phone':'8885440011','email':'kakinada.port@smartrepair.in','latitude':17.0200,'longitude':82.2900,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Rajesh Kumar','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Rajahmundry Main','address':'78 In Road Near RTC Bus Stand','city':'Rajahmundry','district':'East Godavari','pincode':'533101','phone':'8885440012','email':'rajahmundry@smartrepair.in','latitude':17.0005,'longitude':81.7799,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Hari Prasad','total_bays':12,'established_year':2016},
            {'name':'SMART REPAIR - Rajahmundry Morampudi','address':'12 Morampudi Junction NH-16','city':'Rajahmundry','district':'East Godavari','pincode':'533101','phone':'8885440013','email':'rajahmundry.mora@smartrepair.in','latitude':17.0250,'longitude':81.7600,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Ramu Naidu','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Amalapuram','address':'34 Konaseema Road','city':'Amalapuram','district':'East Godavari','pincode':'533201','phone':'8885440014','email':'amalapuram@smartrepair.in','latitude':16.5785,'longitude':82.0050,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Govinda Rao','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Tuni','address':'15 NH-16 Tuni Town','city':'Tuni','district':'East Godavari','pincode':'533401','phone':'8885440015','email':'tuni@smartrepair.in','latitude':17.3582,'longitude':82.5472,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Ravi Shankar','total_bays':6,'established_year':2021},
            # WEST GODAVARI (5)
            {'name':'SMART REPAIR - Eluru Main','address':'12 NH-16 Near Old Bus Stand','city':'Eluru','district':'West Godavari','pincode':'534001','phone':'8885450010','email':'eluru@smartrepair.in','latitude':16.7107,'longitude':81.0952,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Chandra Sekhar','total_bays':10,'established_year':2018},
            {'name':'SMART REPAIR - Bhimavaram','address':'34 Tanuku Road','city':'Bhimavaram','district':'West Godavari','pincode':'534201','phone':'8885450011','email':'bhimavaram@smartrepair.in','latitude':16.5443,'longitude':81.5215,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Subba Rao','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Tanuku','address':'56 Main Road Tanuku Town','city':'Tanuku','district':'West Godavari','pincode':'534211','phone':'8885450012','email':'tanuku@smartrepair.in','latitude':16.7536,'longitude':81.6828,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Veera Babu','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Tadepalligudem','address':'23 Bhimavaram Road','city':'Tadepalligudem','district':'West Godavari','pincode':'534101','phone':'8885450013','email':'tadepalligudem@smartrepair.in','latitude':16.8137,'longitude':81.5258,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Prabhakar Rao','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Narsapur','address':'23 Konaseema Highway','city':'Narsapur','district':'West Godavari','pincode':'534275','phone':'8885450014','email':'narsapur@smartrepair.in','latitude':16.4330,'longitude':81.6940,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Sarada Prasad','total_bays':6,'established_year':2021},
            # TIRUPATI (5)
            {'name':'SMART REPAIR - Tirupati Main','address':'67 TP Area Leela Mahal Circle','city':'Tirupati','district':'Tirupati','pincode':'517501','phone':'8885460010','email':'tirupati.main@smartrepair.in','latitude':13.6288,'longitude':79.4192,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Balaji Reddy','total_bays':14,'established_year':2016},
            {'name':'SMART REPAIR - Tirupati Renigunta Road','address':'89 Renigunta Road','city':'Tirupati','district':'Tirupati','pincode':'517520','phone':'8885460011','email':'tirupati.reni@smartrepair.in','latitude':13.6500,'longitude':79.4050,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Venkateswara Reddy','total_bays':10,'established_year':2018},
            {'name':'SMART REPAIR - Tirupati Alipiri','address':'14 Alipiri Road Near TTD','city':'Tirupati','district':'Tirupati','pincode':'517502','phone':'8885460012','email':'tirupati.alipiri@smartrepair.in','latitude':13.6420,'longitude':79.3980,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Lakshmaiah','total_bays':12,'established_year':2019},
            {'name':'SMART REPAIR - Srikalahasti','address':'45 Temple Road','city':'Srikalahasti','district':'Tirupati','pincode':'517644','phone':'8885460013','email':'srikalahasti@smartrepair.in','latitude':13.7490,'longitude':79.6980,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Prasanna Kumar','total_bays':8,'established_year':2021},
            {'name':'SMART REPAIR - Chandragiri','address':'7 Tirupati Road','city':'Chandragiri','district':'Tirupati','pincode':'517101','phone':'8885460014','email':'chandragiri@smartrepair.in','latitude':13.5847,'longitude':79.3133,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Narasimha Reddy','total_bays':6,'established_year':2021},
            # KURNOOL (5)
            {'name':'SMART REPAIR - Kurnool Main','address':'34 Station Road Near APSRTC','city':'Kurnool','district':'Kurnool','pincode':'518001','phone':'8885470010','email':'kurnool.main@smartrepair.in','latitude':15.8281,'longitude':78.0373,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Siva Kumar','total_bays':10,'established_year':2017},
            {'name':'SMART REPAIR - Kurnool Bypass','address':'78 NH-44 Bypass','city':'Kurnool','district':'Kurnool','pincode':'518003','phone':'8885470011','email':'kurnool.bypass@smartrepair.in','latitude':15.8500,'longitude':78.0600,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Ranga Swamy','total_bays':12,'established_year':2019},
            {'name':'SMART REPAIR - Adoni','address':'12 Bellary Road','city':'Adoni','district':'Kurnool','pincode':'518301','phone':'8885470012','email':'adoni@smartrepair.in','latitude':15.6247,'longitude':77.2745,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Basavaiah','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Nandyal Kurnool','address':'56 Guntakal Road','city':'Nandyal','district':'Kurnool','pincode':'518501','phone':'8885470013','email':'nandyal.kurnool@smartrepair.in','latitude':15.4787,'longitude':78.4839,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Reddappa','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Dhone','address':'4 NH-44 Dhone','city':'Dhone','district':'Kurnool','pincode':'518222','phone':'8885470014','email':'dhone@smartrepair.in','latitude':15.3955,'longitude':77.8686,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Suresh Naidu','total_bays':6,'established_year':2022},
            # NELLORE (5)
            {'name':'SMART REPAIR - Nellore Main','address':'56 Grand Trunk Road Near Town Hall','city':'Nellore','district':'SPSR Nellore','pincode':'524001','phone':'8885480010','email':'nellore.main@smartrepair.in','latitude':14.4426,'longitude':79.9865,'working_hours':'8:00 AM - 7:00 PM','manager_name':'Praveen Kumar','total_bays':10,'established_year':2017},
            {'name':'SMART REPAIR - Nellore Pogathota','address':'23 Pogathota Road','city':'Nellore','district':'SPSR Nellore','pincode':'524002','phone':'8885480011','email':'nellore.poga@smartrepair.in','latitude':14.4560,'longitude':79.9950,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Manohar Rao','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Kavali','address':'14 NH-16 Kavali Town','city':'Kavali','district':'SPSR Nellore','pincode':'524201','phone':'8885480012','email':'kavali@smartrepair.in','latitude':14.9162,'longitude':79.9947,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Soma Shekar','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Sullurpeta','address':'8 Sri City Road','city':'Sullurpeta','district':'SPSR Nellore','pincode':'524121','phone':'8885480013','email':'sullurpeta@smartrepair.in','latitude':13.8670,'longitude':80.0202,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Rajan Kumar','total_bays':8,'established_year':2021},
            {'name':'SMART REPAIR - Gudur','address':'23 NH-16 Gudur','city':'Gudur','district':'SPSR Nellore','pincode':'524101','phone':'8885480014','email':'gudur@smartrepair.in','latitude':14.1479,'longitude':79.8539,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Anantha Rao','total_bays':6,'established_year':2021},
            # CHITTOOR (5)
            {'name':'SMART REPAIR - Chittoor Main','address':'67 Tirupati Road Near Bus Station','city':'Chittoor','district':'Chittoor','pincode':'517001','phone':'8885490010','email':'chittoor.main@smartrepair.in','latitude':13.2172,'longitude':79.1003,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Ramesh Babu','total_bays':10,'established_year':2018},
            {'name':'SMART REPAIR - Madanapalle','address':'34 Bangalore Road','city':'Madanapalle','district':'Chittoor','pincode':'517325','phone':'8885490011','email':'madanapalle@smartrepair.in','latitude':13.5504,'longitude':78.5016,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Govind Reddy','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Puttur','address':'12 NH-71 Puttur','city':'Puttur','district':'Chittoor','pincode':'517583','phone':'8885490012','email':'puttur@smartrepair.in','latitude':13.4425,'longitude':79.5511,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Murthy Naidu','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Nagari','address':'5 Chennai Highway Nagari','city':'Nagari','district':'Chittoor','pincode':'517590','phone':'8885490013','email':'nagari@smartrepair.in','latitude':13.3232,'longitude':79.5826,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Chenna Reddy','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Palamaner','address':'18 Kolar Road Palamaner','city':'Palamaner','district':'Chittoor','pincode':'517408','phone':'8885490014','email':'palamaner@smartrepair.in','latitude':13.2027,'longitude':78.7451,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Thippeswamy','total_bays':6,'established_year':2022},
            # YSR KADAPA (4)
            {'name':'SMART REPAIR - Kadapa Main','address':'34 Cuddapah Main Road','city':'Kadapa','district':'YSR Kadapa','pincode':'516001','phone':'8885500010','email':'kadapa.main@smartrepair.in','latitude':14.4674,'longitude':78.8241,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Krishna Murthy','total_bays':10,'established_year':2018},
            {'name':'SMART REPAIR - Proddatur','address':'56 NH-40 Proddatur','city':'Proddatur','district':'YSR Kadapa','pincode':'516360','phone':'8885500011','email':'proddatur@smartrepair.in','latitude':14.7502,'longitude':78.5481,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Obul Reddy','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Rajampet','address':'12 Kadapa Road Rajampet','city':'Rajampet','district':'YSR Kadapa','pincode':'516115','phone':'8885500012','email':'rajampet@smartrepair.in','latitude':14.1929,'longitude':79.1603,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Jagan Mohan Reddy','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Jammalamadugu','address':'5 Mydukur Road','city':'Jammalamadugu','district':'YSR Kadapa','pincode':'516434','phone':'8885500013','email':'jammalamadugu@smartrepair.in','latitude':14.8455,'longitude':78.3832,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Yellaiah','total_bays':6,'established_year':2021},
            # PRAKASAM (4)
            {'name':'SMART REPAIR - Ongole Main','address':'45 Kurnool Road Near APSRTC','city':'Ongole','district':'Prakasam','pincode':'523001','phone':'8885510010','email':'ongole.main@smartrepair.in','latitude':15.5057,'longitude':80.0499,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Jagan Mohan','total_bays':8,'established_year':2018},
            {'name':'SMART REPAIR - Ongole Bypass','address':'89 NH-16 Ongole Bypass','city':'Ongole','district':'Prakasam','pincode':'523002','phone':'8885510011','email':'ongole.bypass@smartrepair.in','latitude':15.5200,'longitude':80.0650,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Dharma Rao','total_bays':10,'established_year':2020},
            {'name':'SMART REPAIR - Markapur','address':'23 Giddalur Road Markapur','city':'Markapur','district':'Prakasam','pincode':'523316','phone':'8885510012','email':'markapur@smartrepair.in','latitude':15.7385,'longitude':79.2729,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Pulla Reddy','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Kandukur','address':'7 NH-16 Kandukur','city':'Kandukur','district':'Prakasam','pincode':'523105','phone':'8885510013','email':'kandukur@smartrepair.in','latitude':15.2120,'longitude':79.9014,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Suryanarayana','total_bays':6,'established_year':2022},
            # SRIKAKULAM (4)
            {'name':'SMART REPAIR - Srikakulam Main','address':'12 Main Road Near District Court','city':'Srikakulam','district':'Srikakulam','pincode':'532001','phone':'8885520010','email':'srikakulam@smartrepair.in','latitude':18.2949,'longitude':83.8938,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Narayana Swamy','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Palasa','address':'34 NH-16 Palasa','city':'Palasa','district':'Srikakulam','pincode':'532221','phone':'8885520011','email':'palasa@smartrepair.in','latitude':18.7699,'longitude':84.4169,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Appala Raju','total_bays':6,'established_year':2020},
            {'name':'SMART REPAIR - Narasannapeta','address':'8 Srikakulam Road','city':'Narasannapeta','district':'Srikakulam','pincode':'532421','phone':'8885520012','email':'narasannapeta@smartrepair.in','latitude':18.4161,'longitude':83.9967,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Bhaskar Rao','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Amadalavalasa','address':'5 NH-16 Amadalavalasa','city':'Amadalavalasa','district':'Srikakulam','pincode':'532185','phone':'8885520013','email':'amadalavalasa@smartrepair.in','latitude':18.4165,'longitude':83.8966,'working_hours':'8:00 AM - 5:30 PM','manager_name':'Satya Babu','total_bays':4,'established_year':2022},
            # VIZIANAGARAM (4)
            {'name':'SMART REPAIR - Vizianagaram Main','address':'56 Station Road Near Fort','city':'Vizianagaram','district':'Vizianagaram','pincode':'535001','phone':'8885530010','email':'vizianagaram@smartrepair.in','latitude':18.1066,'longitude':83.3956,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Vasu Deva Rao','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Bobbili','address':'23 Parvathipuram Road','city':'Bobbili','district':'Vizianagaram','pincode':'535558','phone':'8885530011','email':'bobbili@smartrepair.in','latitude':18.5739,'longitude':83.3567,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Durgaiah','total_bays':6,'established_year':2020},
            {'name':'SMART REPAIR - Parvathipuram','address':'7 Visakhapatnam Road','city':'Parvathipuram','district':'Vizianagaram','pincode':'535501','phone':'8885530012','email':'parvathipuram@smartrepair.in','latitude':18.7785,'longitude':83.4271,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Srinu Naidu','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Salur','address':'3 Vizianagaram Road Salur','city':'Salur','district':'Vizianagaram','pincode':'535591','phone':'8885530013','email':'salur@smartrepair.in','latitude':18.5245,'longitude':83.2025,'working_hours':'8:00 AM - 5:30 PM','manager_name':'Harish Babu','total_bays':4,'established_year':2022},
            # ANANTAPUR (5)
            {'name':'SMART REPAIR - Anantapur Main','address':'45 Bangalore Road Near Hospital','city':'Anantapur','district':'Anantapur','pincode':'515001','phone':'8885540010','email':'anantapur.main@smartrepair.in','latitude':14.6819,'longitude':77.6006,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Venkat Reddy','total_bays':10,'established_year':2018},
            {'name':'SMART REPAIR - Guntakal','address':'34 Railway Station Road','city':'Guntakal','district':'Anantapur','pincode':'515801','phone':'8885540011','email':'guntakal@smartrepair.in','latitude':15.1691,'longitude':77.3722,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Ramaiah','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Hindupur','address':'12 Bangalore Highway','city':'Hindupur','district':'Anantapur','pincode':'515201','phone':'8885540012','email':'hindupur@smartrepair.in','latitude':13.8286,'longitude':77.4919,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Sidda Reddy','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Tadipatri','address':'9 NH-40 Tadipatri','city':'Tadipatri','district':'Anantapur','pincode':'515411','phone':'8885540013','email':'tadipatri@smartrepair.in','latitude':14.9040,'longitude':78.0090,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Gopal Krishna','total_bays':6,'established_year':2022},
            {'name':'SMART REPAIR - Dharmavaram','address':'12 Anantapur Road','city':'Dharmavaram','district':'Anantapur','pincode':'515671','phone':'8885540014','email':'dharmavaram@smartrepair.in','latitude':14.4147,'longitude':77.7183,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Lakshmi Narayana','total_bays':6,'established_year':2022},
            # ALLURI SITARAMA RAJU (3)
            {'name':'SMART REPAIR - Rajam','address':'12 NH-516 Rajam','city':'Rajam','district':'Alluri Sitarama Raju','pincode':'532127','phone':'8885550010','email':'rajam@smartrepair.in','latitude':18.4655,'longitude':83.6464,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Subrahmanyam','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Narsipatnam','address':'8 Visakhapatnam Road','city':'Narsipatnam','district':'Alluri Sitarama Raju','pincode':'531116','phone':'8885550011','email':'narsipatnam@smartrepair.in','latitude':17.6674,'longitude':82.6136,'working_hours':'8:00 AM - 5:30 PM','manager_name':'Appala Swamy','total_bays':4,'established_year':2022},
            {'name':'SMART REPAIR - Paderu','address':'5 Araku Road Paderu','city':'Paderu','district':'Alluri Sitarama Raju','pincode':'531024','phone':'8885550012','email':'paderu@smartrepair.in','latitude':18.0648,'longitude':82.6624,'working_hours':'8:00 AM - 5:30 PM','manager_name':'Linga Raju','total_bays':4,'established_year':2022},
            # ANAKAPALLI (3)
            {'name':'SMART REPAIR - Anakapalli','address':'34 NH-16 Anakapalli Town','city':'Anakapalli','district':'Anakapalli','pincode':'531001','phone':'8885560010','email':'anakapalli@smartrepair.in','latitude':17.6910,'longitude':83.0053,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Satya Narayana','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Yelamanchili','address':'12 NH-16 Yelamanchili','city':'Yelamanchili','district':'Anakapalli','pincode':'531055','phone':'8885560011','email':'yelamanchili@smartrepair.in','latitude':17.5390,'longitude':82.8603,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Srinivasa Rao','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Chodavaram','address':'5 Anakapalli Road','city':'Chodavaram','district':'Anakapalli','pincode':'531036','phone':'8885560012','email':'chodavaram@smartrepair.in','latitude':17.8090,'longitude':82.9357,'working_hours':'8:00 AM - 5:30 PM','manager_name':'Siva Nageswara Rao','total_bays':4,'established_year':2022},
            # BAPATLA (3)
            {'name':'SMART REPAIR - Bapatla','address':'45 Chennai Road Bapatla','city':'Bapatla','district':'Bapatla','pincode':'522101','phone':'8885580010','email':'bapatla@smartrepair.in','latitude':15.9064,'longitude':80.4672,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Nageswara Rao','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Chirala','address':'23 Ongole Road Chirala','city':'Chirala','district':'Bapatla','pincode':'523157','phone':'8885580011','email':'chirala@smartrepair.in','latitude':15.8278,'longitude':80.3552,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Apparao','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Addanki','address':'8 NH-16 Addanki','city':'Addanki','district':'Bapatla','pincode':'523201','phone':'8885580012','email':'addanki@smartrepair.in','latitude':15.8085,'longitude':79.9756,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Venu Gopal','total_bays':4,'established_year':2022},
            # PALNADU (3)
            {'name':'SMART REPAIR - Macherla','address':'12 Narasaraopet Road Macherla','city':'Macherla','district':'Palnadu','pincode':'522426','phone':'8885590010','email':'macherla@smartrepair.in','latitude':16.4741,'longitude':79.4333,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Nageswara Raju','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Sattenapalle','address':'5 Guntur Road Sattenapalle','city':'Sattenapalle','district':'Palnadu','pincode':'522403','phone':'8885590011','email':'sattenapalle@smartrepair.in','latitude':16.3958,'longitude':80.1519,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Hanumantha Rao','total_bays':6,'established_year':2022},
            {'name':'SMART REPAIR - Vinukonda','address':'3 Guntur Road Vinukonda','city':'Vinukonda','district':'Palnadu','pincode':'522647','phone':'8885590012','email':'vinukonda@smartrepair.in','latitude':16.0557,'longitude':79.7424,'working_hours':'8:00 AM - 5:30 PM','manager_name':'Venkata Subbaiah','total_bays':4,'established_year':2023},
            # NTR (3)
            {'name':'SMART REPAIR - Nandigama','address':'14 Vijayawada Road Nandigama','city':'Nandigama','district':'NTR','pincode':'521185','phone':'8885600010','email':'nandigama@smartrepair.in','latitude':16.7741,'longitude':80.2869,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Venkaiah','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Jaggayyapeta','address':'8 Krishna Road','city':'Jaggayyapeta','district':'NTR','pincode':'521175','phone':'8885600011','email':'jaggayyapeta@smartrepair.in','latitude':16.8951,'longitude':80.0976,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Subrahmanya Sarma','total_bays':6,'established_year':2022},
            {'name':'SMART REPAIR - Tiruvuru','address':'3 NH-65 Tiruvuru','city':'Tiruvuru','district':'NTR','pincode':'521235','phone':'8885600012','email':'tiruvuru@smartrepair.in','latitude':16.9717,'longitude':80.6098,'working_hours':'8:00 AM - 5:30 PM','manager_name':'Raghu Ram','total_bays':4,'established_year':2023},
            # ELURU (3)
            {'name':'SMART REPAIR - Eluru Powerpet','address':'45 Powerpet Road Eluru','city':'Eluru','district':'Eluru','pincode':'534002','phone':'8885610010','email':'eluru.power@smartrepair.in','latitude':16.7200,'longitude':81.1050,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Appala Raju','total_bays':8,'established_year':2019},
            {'name':'SMART REPAIR - Kovvur','address':'5 Godavari Bridge Road','city':'Kovvur','district':'Eluru','pincode':'534350','phone':'8885610011','email':'kovvur@smartrepair.in','latitude':17.0154,'longitude':81.7245,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Sitarama Rao','total_bays':4,'established_year':2021},
            {'name':'SMART REPAIR - Jangareddigudem','address':'7 Eluru Road','city':'Jangareddigudem','district':'Eluru','pincode':'534447','phone':'8885610012','email':'jangareddigudem@smartrepair.in','latitude':17.0971,'longitude':81.2974,'working_hours':'8:00 AM - 5:30 PM','manager_name':'Durga Prasad','total_bays':4,'established_year':2022},
            # KONASEEMA (3)
            {'name':'SMART REPAIR - Amalapuram Konaseema','address':'34 Godavari Road Amalapuram','city':'Amalapuram','district':'Konaseema','pincode':'533201','phone':'8885620010','email':'konaseema.amalapuram@smartrepair.in','latitude':16.5790,'longitude':82.0060,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Govinda Rao','total_bays':8,'established_year':2021},
            {'name':'SMART REPAIR - Razole','address':'8 Amalapuram Road Razole','city':'Razole','district':'Konaseema','pincode':'533242','phone':'8885620011','email':'razole@smartrepair.in','latitude':16.4780,'longitude':81.8376,'working_hours':'8:00 AM - 5:30 PM','manager_name':'Kotaiah','total_bays':4,'established_year':2022},
            {'name':'SMART REPAIR - Mandapeta','address':'4 Rajahmundry Road Mandapeta','city':'Mandapeta','district':'Konaseema','pincode':'533308','phone':'8885620012','email':'mandapeta@smartrepair.in','latitude':16.8687,'longitude':81.9266,'working_hours':'8:00 AM - 5:30 PM','manager_name':'Narsing Rao','total_bays':4,'established_year':2022},
            # SRI SATHYA SAI (2)
            {'name':'SMART REPAIR - Puttaparthi','address':'5 Prasanthi Nilayam Road','city':'Puttaparthi','district':'Sri Sathya Sai','pincode':'515134','phone':'8885630010','email':'puttaparthi@smartrepair.in','latitude':14.1649,'longitude':77.8282,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Mohan Kumar','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Penukonda','address':'9 NH-44 Penukonda','city':'Penukonda','district':'Sri Sathya Sai','pincode':'515110','phone':'8885630011','email':'penukonda@smartrepair.in','latitude':14.0853,'longitude':77.5937,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Hanumappa','total_bays':4,'established_year':2022},
            # NANDYAL (2)
            {'name':'SMART REPAIR - Nandyal Main','address':'34 Station Road Nandyal','city':'Nandyal','district':'Nandyal','pincode':'518501','phone':'8885640010','email':'nandyal.main@smartrepair.in','latitude':15.4787,'longitude':78.4839,'working_hours':'8:00 AM - 6:30 PM','manager_name':'Venkata Krishna','total_bays':8,'established_year':2020},
            {'name':'SMART REPAIR - Allagadda','address':'6 Kurnool Road Allagadda','city':'Allagadda','district':'Nandyal','pincode':'518543','phone':'8885640011','email':'allagadda@smartrepair.in','latitude':15.1307,'longitude':78.5211,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Obanna','total_bays':4,'established_year':2022},
            # KAKINADA (2)
            {'name':'SMART REPAIR - Peddapuram','address':'23 Rajahmundry Road Peddapuram','city':'Peddapuram','district':'Kakinada','pincode':'533437','phone':'8885570010','email':'peddapuram@smartrepair.in','latitude':17.0775,'longitude':82.1380,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Rama Murthy','total_bays':6,'established_year':2021},
            {'name':'SMART REPAIR - Samalkota','address':'5 NH-16 Samalkota','city':'Samalkota','district':'Kakinada','pincode':'533440','phone':'8885570011','email':'samalkota@smartrepair.in','latitude':17.0566,'longitude':82.1751,'working_hours':'8:00 AM - 6:00 PM','manager_name':'Trinadha Rao','total_bays':6,'established_year':2021},
        ]
        count = 0
        for c in centers:
            defaults = {k: v for k, v in c.items() if k != 'name'}
            defaults.update({'state': 'AP', 'working_days': 'Monday to Saturday', 'is_active': True})
            _, created = ServiceCenter.objects.get_or_create(name=c['name'], defaults=defaults)
            if created:
                count += 1
        total = ServiceCenter.objects.filter(is_active=True).count()
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} new centers added | {total} total across AP'))

    # ─────────────────────────────────────────────────────────────────────────
    # REPAIR ISSUES — all vehicle types, all categories
    # ─────────────────────────────────────────────────────────────────────────
    def create_repair_issues(self):
        from bookings.models import RepairIssue
        issues = [
            # ── TWO WHEELER ────────────────────────────────────────────
            ('Engine Not Starting', 'engine', '2w', 300, 800, 'Bike/scooter engine fails to crank or start'),
            ('Engine Overheating', 'engine', '2w', 400, 1200, 'Engine temperature rises abnormally'),
            ('Low Pickup / Misfiring', 'engine', '2w', 250, 700, 'Loss of acceleration, engine misfire'),
            ('Oil Leakage', 'engine', '2w', 300, 900, 'Engine oil leaking from gasket or seals'),
            ('Chain Problem / Noise', 'engine', '2w', 150, 500, 'Chain loose, worn, or making noise'),
            ('Brake Not Working Properly', 'brakes', '2w', 200, 600, 'Brakes feel soft, squealing, or weak'),
            ('Brake Pads Worn Out', 'brakes', '2w', 150, 400, 'Brake pads need replacement'),
            ('Front Fork Leaking', 'brakes', '2w', 500, 1500, 'Front suspension fork oil seal leak'),
            ('Tyre Puncture', 'tyres', '2w', 100, 250, 'Flat tyre, nail, or tube damage'),
            ('Tyre Worn / Bald', 'tyres', '2w', 500, 2000, 'Tyre tread worn out, needs replacement'),
            ('Battery Dead / Weak', 'electrical', '2w', 200, 800, 'Battery drains fast or does not charge'),
            ('Headlight Not Working', 'electrical', '2w', 150, 500, 'Headlight bulb, wire or relay fault'),
            ('Self Start Not Working', 'electrical', '2w', 300, 800, 'Electric starter motor not working'),
            ('Indicator / Horn Fault', 'electrical', '2w', 100, 400, 'Turn signals or horn not functioning'),
            ('Fuel Leakage / Carb Issue', 'fuel', '2w', 200, 700, 'Carburetor or fuel line leaking'),
            ('Poor Mileage', 'fuel', '2w', 200, 600, 'Fuel efficiency has reduced significantly'),
            ('Clutch Slipping / Hard', 'transmission', '2w', 200, 700, 'Clutch plates worn or clutch cable issue'),
            ('Gear Shifting Problem', 'transmission', '2w', 250, 800, 'Gears not shifting smoothly'),
            ('Periodic Service (2W)', 'service', '2w', 499, 999, 'Full scheduled service: oil, filter, check-up'),

            # ── THREE WHEELER ──────────────────────────────────────────
            ('Auto Engine Overheating', 'engine', '3w', 500, 1500, 'Auto engine overheats on long runs'),
            ('CNG Kit Problem', 'fuel', '3w', 300, 1000, 'CNG kit not switching or leaking'),
            ('Auto Brake Failure', 'brakes', '3w', 400, 1200, 'Brakes weak or not responding'),
            ('Auto Electrical Fault', 'electrical', '3w', 300, 900, 'Electrical wiring, lights or horn issue'),
            ('Auto Tyre Wear / Puncture', 'tyres', '3w', 200, 700, 'Tyre puncture or worn out'),
            ('Auto Transmission Problem', 'transmission', '3w', 500, 2000, 'Gearbox or clutch issue in auto'),
            ('Auto Periodic Service', 'service', '3w', 799, 1299, 'Full auto rickshaw service'),

            # ── FOUR WHEELER ───────────────────────────────────────────
            ('Car Engine Not Starting', 'engine', '4w', 500, 2000, 'Car does not start, starter or battery issue'),
            ('Engine Knocking Sound', 'engine', '4w', 1000, 5000, 'Metallic knocking from engine internals'),
            ('Engine Overheating', 'engine', '4w', 800, 3000, 'Coolant leak or radiator issue'),
            ('Car Vibration / Shaking', 'engine', '4w', 500, 2500, 'Car shakes while driving or idling'),
            ('Oil Leakage (Car)', 'engine', '4w', 500, 2000, 'Engine oil leaking from gasket or sump'),
            ('Check Engine Light On', 'engine', '4w', 500, 3000, 'MIL / CEL on dashboard illuminated'),
            ('Brake Failure / Spongy', 'brakes', '4w', 800, 3000, 'Brakes feel spongy, weak, or pulling'),
            ('Brake Pads / Disc Worn', 'brakes', '4w', 600, 2500, 'Brake pads or rotors need replacement'),
            ('Car Pulling to One Side', 'brakes', '4w', 500, 1500, 'Steering pulls left/right while braking'),
            ('Shock Absorber Leaking', 'brakes', '4w', 1500, 5000, 'Suspension oil leaked, bouncy ride'),
            ('Steering Heavy / Play', 'brakes', '4w', 800, 3000, 'Power steering hard or loose steering'),
            ('Car Tyre Puncture', 'tyres', '4w', 200, 500, 'Flat tyre needs repair or replacement'),
            ('Tyre Uneven Wear', 'tyres', '4w', 300, 800, 'Tyres wearing unevenly, alignment needed'),
            ('AC Not Cooling', 'ac', '4w', 500, 2500, 'AC blowing warm air, gas leak or compressor'),
            ('AC Gas Leakage', 'ac', '4w', 800, 2000, 'Refrigerant gas leak from AC system'),
            ('Compressor Not Working', 'ac', '4w', 2000, 8000, 'AC compressor clutch or motor failure'),
            ('Battery Draining Fast', 'electrical', '4w', 500, 2000, 'Car battery drains overnight or quickly'),
            ('Car Not Charging Battery', 'electrical', '4w', 800, 2500, 'Alternator or charging circuit fault'),
            ('Lights Not Working', 'electrical', '4w', 300, 1000, 'Headlights, taillights or interior lights'),
            ('Car Central Locking Fault', 'electrical', '4w', 500, 1500, 'Central lock not working or key fob issue'),
            ('Gear Shifting Hard', 'transmission', '4w', 1000, 4000, 'Manual gearbox stiff or not engaging'),
            ('Automatic Transmission Jerk', 'transmission', '4w', 2000, 8000, 'AT slipping, jerking or delayed shifts'),
            ('Clutch Plate Worn', 'transmission', '4w', 3000, 8000, 'Clutch slipping or juddering on take-off'),
            ('Denting / Scratches', 'body', '4w', 500, 5000, 'Panel dents, deep scratches or rust'),
            ('Windshield Crack / Chip', 'body', '4w', 500, 5000, 'Windscreen damaged or chipped'),
            ('Car Full Painting', 'body', '4w', 8000, 25000, 'Full vehicle respray or partial paint job'),
            ('Fuel Pump Issue', 'fuel', '4w', 1500, 5000, 'Fuel pump weak or not pressurising'),
            ('Diesel Injector Problem', 'fuel', '4w', 2000, 8000, 'Injector clogged, noisy or misfiring'),
            ('Car Full Service', 'service', '4w', 1299, 2999, 'Complete scheduled service with all checks'),

            # ── HEAVY VEHICLE ──────────────────────────────────────────
            ('Truck Engine Failure', 'engine', 'heavy', 5000, 25000, 'Major engine fault in truck or bus'),
            ('Truck Overheating', 'engine', 'heavy', 2000, 8000, 'Cooling system or head gasket issue'),
            ('Truck Brake Failure', 'brakes', 'heavy', 3000, 12000, 'Air brake or hydraulic brake fault'),
            ('Heavy Vehicle Tyre Issue', 'tyres', 'heavy', 1500, 8000, 'Commercial tyre puncture or replacement'),
            ('Truck Electrical Fault', 'electrical', 'heavy', 1500, 6000, 'Wiring, alternator, battery issue'),
            ('Gearbox Failure', 'transmission', 'heavy', 8000, 40000, 'Truck gearbox grinding or not engaging'),
            ('Truck Suspension Failure', 'brakes', 'heavy', 5000, 20000, 'Leaf spring, shock absorber broken'),
            ('Bus AC Not Cooling', 'ac', 'heavy', 3000, 12000, 'Bus AC system underperforming'),
            ('Heavy Vehicle Full Service', 'service', 'heavy', 4999, 9999, 'Complete truck/bus maintenance service'),
        ]

        count = 0
        for i, (name, cat, vtype, min_cost, max_cost, desc) in enumerate(issues):
            _, created = RepairIssue.objects.get_or_create(
                name=name, vehicle_type=vtype,
                defaults={
                    'category': cat, 'estimated_cost_min': min_cost,
                    'estimated_cost_max': max_cost, 'description': desc,
                    'is_active': True, 'display_order': i,
                }
            )
            if created:
                count += 1
        total = RepairIssue.objects.filter(is_active=True).count()
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} repair issues created | {total} total'))

    # ─────────────────────────────────────────────────────────────────────────
    # SERVICE TYPES
    # ─────────────────────────────────────────────────────────────────────────
    def create_service_types(self):
        from core.models import ServiceType
        services = [
            ('Basic Service', '2w', 'Oil change, filter, cleaning, inspection', 499, 2, 'fa-oil-can'),
            ('Full Service', '2w', 'Comprehensive: engine, brakes, tyres, electricals', 999, 4, 'fa-wrench'),
            ('Tyre Puncture Repair', '2w', 'Puncture repair, tyre change, balancing', 149, 1, 'fa-circle'),
            ('Battery Replacement', '2w', 'Battery check, charging, replacement', 299, 1, 'fa-car-battery'),
            ('Brake Service', '2w', 'Brake pad/shoe inspection and replacement', 399, 1, 'fa-compact-disc'),
            ('Chain Lubrication', '2w', 'Chain cleaning, lubrication, tension', 149, 0, 'fa-link'),
            ('Auto Rickshaw Service', '3w', 'Complete service for auto rickshaws', 799, 3, 'fa-taxi'),
            ('CNG Kit Service', '3w', 'CNG kit inspection, tuning, leak check', 599, 2, 'fa-fire'),
            ('Auto Tyre & Brake', '3w', 'Tyre change, brake lining, alignment', 499, 2, 'fa-circle'),
            ('Basic Car Service', '4w', 'Engine oil, filters, basic inspection', 1299, 3, 'fa-oil-can'),
            ('Comprehensive Car Service', '4w', 'Full: engine, brakes, AC, tyres, electricals', 2999, 5, 'fa-car'),
            ('AC Service & Gas Refill', '4w', 'AC gas refill, compressor check, cooling test', 999, 2, 'fa-snowflake'),
            ('Denting & Painting', '4w', 'Panel denting, putty, primer, paint', 2499, 8, 'fa-paint-roller'),
            ('Wheel Alignment & Balancing', '4w', 'Computer alignment, balancing, rotation', 599, 1, 'fa-circle-notch'),
            ('Car Battery Service', '4w', 'Battery check, terminals, replacement', 599, 1, 'fa-car-battery'),
            ('Windshield Repair', '4w', 'Chip repair, crack fill, replacement', 799, 2, 'fa-window-maximize'),
            ('Engine Diagnostics OBD', '4w', 'OBD scan, fault codes, health check', 799, 2, 'fa-microchip'),
            ('Suspension Service', '4w', 'Shock absorber, spring, bush repair', 1499, 3, 'fa-arrows-alt-v'),
            ('Truck Full Service', 'heavy', 'Complete commercial vehicle service', 4999, 8, 'fa-truck'),
            ('Bus Service', 'heavy', 'Complete passenger bus maintenance', 5999, 10, 'fa-bus'),
            ('Heavy Vehicle Tyre Service', 'heavy', 'Commercial tyre change, alignment', 1499, 3, 'fa-circle'),
            ('Engine Overhaul', 'heavy', 'Complete engine reconditioning', 19999, 48, 'fa-cogs'),
            ('Air Brake Overhaul', 'heavy', 'Brake system inspection and overhaul', 2999, 4, 'fa-stop-circle'),
            ('General Car Wash', 'all', 'Exterior wash, vacuum, dashboard wipe', 199, 1, 'fa-tint'),
            ('Interior Detailing', 'all', 'Deep interior clean, shampooing', 799, 3, 'fa-star'),
            ('Electrical Repair', 'all', 'Wiring, fuse, relay, sensor repair', 499, 2, 'fa-bolt'),
            ('Emergency Repair', 'all', 'Priority emergency vehicle repair', 999, 2, 'fa-exclamation-triangle'),
        ]
        count = 0
        for i, (name, vtype, desc, price, dur, icon) in enumerate(services):
            _, created = ServiceType.objects.get_or_create(
                name=name, vehicle_type=vtype,
                defaults={'description': desc, 'base_price': price, 'estimated_duration': dur,
                          'icon': icon, 'is_active': True, 'display_order': i}
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} service types created'))

    # ─────────────────────────────────────────────────────────────────────────
    # HOLIDAYS
    # ─────────────────────────────────────────────────────────────────────────
    def create_holidays(self):
        from core.models import Holiday
        holidays = [
            ("New Year's Day", date(2025, 1, 1), True, 'New Year celebration'),
            ('Pongal / Sankranti', date(2025, 1, 14), False, 'Harvest festival of AP'),
            ('Kanuma', date(2025, 1, 15), False, 'Second day of Sankranti'),
            ('Republic Day', date(2025, 1, 26), True, 'National holiday'),
            ('Maha Shivaratri', date(2025, 2, 26), False, 'Hindu festival'),
            ('Holi', date(2025, 3, 14), True, 'Festival of colors'),
            ('Eid al-Fitr', date(2025, 3, 31), True, 'Islamic festival'),
            ('Ugadi (Telugu New Year)', date(2025, 3, 30), False, 'Telugu New Year'),
            ('Ram Navami', date(2025, 4, 6), False, 'Hindu festival'),
            ('Dr. Ambedkar Jayanti', date(2025, 4, 14), True, 'National holiday'),
            ('Good Friday', date(2025, 4, 18), True, 'Christian holiday'),
            ('Labour Day', date(2025, 5, 1), True, "Workers' Day"),
            ('Buddha Purnima', date(2025, 5, 12), True, 'Buddhist festival'),
            ('Eid al-Adha', date(2025, 6, 7), True, 'Islamic festival'),
            ('Independence Day', date(2025, 8, 15), True, 'National holiday'),
            ('Janmashtami', date(2025, 8, 16), False, 'Hindu festival'),
            ('Ganesh Chaturthi', date(2025, 8, 27), False, 'Major AP festival'),
            ('Gandhi Jayanti / Dussehra', date(2025, 10, 2), True, 'National + Hindu festival'),
            ('Diwali', date(2025, 10, 20), True, 'Festival of lights'),
            ('Diwali Bali Padyami', date(2025, 10, 21), False, 'Day after Diwali'),
            ('AP Formation Day', date(2025, 11, 1), False, 'Andhra Pradesh State Day'),
            ('Kartika Pournami', date(2025, 11, 5), False, 'Telugu festival'),
            ('Christmas', date(2025, 12, 25), True, 'Christian festival'),
        ]
        count = 0
        for name, hdate, nat, desc in holidays:
            _, created = Holiday.objects.get_or_create(
                name=name, date=hdate, defaults={'description': desc, 'is_national': nat}
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} holidays created'))

    # ─────────────────────────────────────────────────────────────────────────
    # ADMIN
    # ─────────────────────────────────────────────────────────────────────────
    def create_admin(self):
        from accounts.models import User
        if not User.objects.filter(mobile_number='9999999999').exists():
            User.objects.create_superuser(
                mobile_number='9999999999', password='admin@123',
                first_name='Admin', last_name='Smart Repair',
                role='admin', is_verified=True, email='admin@smartrepair.in'
            )
            self.stdout.write(self.style.SUCCESS('  ✅ Admin: 9999999999 / admin@123'))

    # ─────────────────────────────────────────────────────────────────────────
    # EMPLOYEES + WORKERS at every service center
    # ─────────────────────────────────────────────────────────────────────────
    def create_employees_and_workers(self):
        from accounts.models import User, Employee
        from core.models import ServiceCenter

        # Named managers & employees from earlier
        named = [
            ('EMP001', '8001000001', 'Ravi', 'Kumar', 'manager', 'Vijayawada MG Road'),
            ('EMP002', '8001000002', 'Suresh', 'Reddy', 'mechanic', 'Vijayawada MG Road'),
            ('EMP003', '8001000003', 'Priya', 'Sharma', 'receptionist', 'Vijayawada MG Road'),
            ('EMP004', '8001000004', 'Anand', 'Krishna', 'manager', 'Visakhapatnam Dwaraka Nagar'),
            ('EMP005', '8001000005', 'Mohan', 'Das', 'mechanic', 'Visakhapatnam Dwaraka Nagar'),
            ('EMP006', '8001000006', 'Lakshmi', 'Devi', 'receptionist', 'Guntur Brodipet'),
            ('EMP007', '8001000007', 'Venkat', 'Rao', 'manager', 'Guntur Brodipet'),
            ('EMP008', '8001000008', 'Balaji', 'Naidu', 'electrician', 'Tirupati Main'),
            ('EMP009', '8001000009', 'Srinu', 'Babu', 'painter', 'Vijayawada Auto Nagar'),
            ('EMP010', '8001000010', 'Kiran', 'Kumar', 'worker', 'Vijayawada Auto Nagar'),
            ('EMP011', '8001000011', 'Rama', 'Rao', 'manager', 'Kurnool Main'),
            ('EMP012', '8001000012', 'Durga', 'Prasad', 'mechanic', 'Nellore Main'),
            ('EMP013', '8001000013', 'Siva', 'Kumar', 'mechanic', 'Tirupati Main'),
            ('EMP014', '8001000014', 'Narasimha', 'Reddy', 'manager', 'Kadapa Main'),
            ('EMP015', '8001000015', 'Pavan', 'Kalyan', 'supervisor', 'Rajahmundry Main'),
        ]

        count = 0
        for emp_id, mobile, fname, lname, designation, center_partial in named:
            user, ucreated = User.objects.get_or_create(
                mobile_number=mobile,
                defaults={'first_name': fname, 'last_name': lname,
                          'role': 'employee', 'is_verified': True,
                          'is_staff': designation == 'manager'}
            )
            if ucreated:
                user.set_password('emp@123')
                user.save()
            center = ServiceCenter.objects.filter(name__icontains=center_partial.split()[-1], is_active=True).first()
            if not center:
                center = ServiceCenter.objects.filter(is_active=True).first()
            emp, ecreated = Employee.objects.get_or_create(
                employee_id=emp_id,
                defaults={'user': user, 'designation': designation, 'service_center': center,
                          'joining_date': date(2023, 1, 1),
                          'salary': 28000 if designation == 'manager' else 18000,
                          'is_active': True}
            )
            if ecreated:
                count += 1

        # Now add 3 workers to EVERY service center that doesn't already have 3+ workers
        centers = ServiceCenter.objects.filter(is_active=True)
        worker_designations = ['mechanic', 'mechanic', 'electrician', 'painter', 'worker', 'worker']
        first_names = ['Ramu', 'Babu', 'Sekhar', 'Naidu', 'Swamy', 'Reddy', 'Kumar', 'Rao',
                       'Prasad', 'Varma', 'Chandra', 'Murali', 'Satish', 'Ganesh', 'Suresh',
                       'Naresh', 'Ramesh', 'Mahesh', 'Dinesh', 'Umesh']
        last_names = ['Reddy', 'Naidu', 'Rao', 'Kumar', 'Babu', 'Varma', 'Swamy',
                      'Sharma', 'Das', 'Raju', 'Prasad', 'Krishna', 'Murthy', 'Nair']

        import random
        random.seed(42)
        mobile_counter = 8002000001

        for center in centers:
            existing_count = Employee.objects.filter(service_center=center, is_active=True).count()
            needed = max(0, 4 - existing_count)  # ensure at least 4 staff per center
            for j in range(needed):
                mobile_str = str(mobile_counter)
                mobile_counter += 1
                emp_id_str = f'W{mobile_counter % 100000:05d}'
                fname = random.choice(first_names)
                lname = random.choice(last_names)
                designation = worker_designations[j % len(worker_designations)]
                salary = 16000 if designation == 'worker' else 18000

                user, ucreated = User.objects.get_or_create(
                    mobile_number=mobile_str,
                    defaults={'first_name': fname, 'last_name': lname,
                              'role': 'employee', 'is_verified': True}
                )
                if ucreated:
                    user.set_password('worker@123')
                    user.save()

                emp, ecreated = Employee.objects.get_or_create(
                    employee_id=emp_id_str,
                    defaults={'user': user, 'designation': designation,
                              'service_center': center,
                              'joining_date': date(2024, 1, 1),
                              'salary': salary, 'is_active': True}
                )
                if ecreated:
                    count += 1

        total_emp = Employee.objects.filter(is_active=True).count()
        self.stdout.write(self.style.SUCCESS(
            f'  ✅ {count} employees/workers created | {total_emp} total staff across all centers'
        ))
        self.stdout.write(self.style.WARNING(
            '  📋 Named employees: EMP001-EMP015 | mobile 800100000X | password emp@123\n'
            '  📋 Workers: mobile 800200XXXX | password worker@123'
        ))

    # ─────────────────────────────────────────────────────────────────────────
    # TIME SLOTS — 21 days for top 20 centers
    # ─────────────────────────────────────────────────────────────────────────
    def create_time_slots(self):
        from bookings.models import TimeSlot
        from core.models import ServiceCenter
        centers = ServiceCenter.objects.filter(is_active=True)[:20]
        today = date.today()
        slot_times = [
            (time(8, 0), time(9, 0)), (time(9, 0), time(10, 0)),
            (time(10, 0), time(11, 0)), (time(11, 0), time(12, 0)),
            (time(13, 0), time(14, 0)), (time(14, 0), time(15, 0)),
            (time(15, 0), time(16, 0)), (time(16, 0), time(17, 0)),
            (time(17, 0), time(18, 0)),
        ]
        count = 0
        for center in centers:
            for day_offset in range(0, 21):
                slot_date = today + timedelta(days=day_offset)
                if slot_date.weekday() == 6:
                    continue
                for start_t, end_t in slot_times:
                    _, created = TimeSlot.objects.get_or_create(
                        service_center=center, date=slot_date, start_time=start_t,
                        defaults={'end_time': end_t, 'max_bookings': 5, 'is_available': True}
                    )
                    if created:
                        count += 1
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} time slots (21 days × 20 centers)'))


    def create_repair_issues(self):
        from bookings.models import RepairIssue
        issues = [
            # ENGINE
            ('Engine not starting', 'engine', '2w', 300, 2000, 'Bike/scooter not cranking or turning over'),
            ('Engine overheating', 'engine', '2w', 500, 3000, 'Engine temperature rising abnormally'),
            ('Engine oil leaking', 'engine', '2w', 200, 1500, 'Oil dripping from engine'),
            ('Unusual engine noise / knocking', 'engine', '2w', 500, 4000, 'Tapping, knocking or rattling sounds'),
            ('Engine not starting', 'engine', '4w', 500, 3000, 'Car cranks but won\'t start or no crank'),
            ('Engine overheating / coolant issue', 'engine', '4w', 800, 5000, 'Temperature warning, steam, coolant loss'),
            ('Engine oil leaking', 'engine', '4w', 300, 3000, 'Oil spots under car, burning smell'),
            ('Engine knocking / rough idle', 'engine', '4w', 1000, 8000, 'Irregular idle, misfires, power loss'),
            ('Check engine light on', 'engine', 'all', 500, 2000, 'OBD warning light illuminated'),
            # BRAKES
            ('Brakes not working / hard pedal', 'brakes', '4w', 500, 3000, 'Pedal goes to floor or very stiff'),
            ('Brake noise / squealing', 'brakes', 'all', 300, 2500, 'Squealing, grinding when braking'),
            ('Car pulling to one side when braking', 'brakes', '4w', 500, 2000, 'Vehicle drifts left or right during braking'),
            ('Handbrake not holding', 'brakes', 'all', 300, 1500, 'Parking brake loose or ineffective'),
            ('Brake pads worn', 'brakes', '4w', 800, 3000, 'Pad wear indicator noise'),
            ('Brake vibration / judder', 'brakes', '4w', 500, 3000, 'Steering wheel shaking when braking'),
            # TYRES
            ('Flat tyre / puncture', 'tyres', 'all', 100, 500, 'Flat or losing air rapidly'),
            ('Tyre bulge or cracking', 'tyres', 'all', 500, 3000, 'Visible bulge or sidewall cracks'),
            ('Abnormal tyre wear', 'tyres', 'all', 300, 2000, 'Uneven wear pattern'),
            ('Wheel alignment off', 'tyres', '4w', 400, 800, 'Car drifts when driving straight'),
            ('Wheel balancing needed', 'tyres', 'all', 200, 500, 'Vibration in steering at high speed'),
            # ELECTRICAL
            ('Battery dead / not charging', 'electrical', 'all', 300, 5000, 'Car won\'t start, battery warning'),
            ('Headlights not working', 'electrical', 'all', 200, 2000, 'One or both headlights out'),
            ('Electrical short / fuse blown', 'electrical', 'all', 200, 2000, 'Repeated fuse failures, dead circuits'),
            ('Starter motor issue', 'electrical', 'all', 500, 4000, 'Clicking sound when starting'),
            ('Alternator issue', 'electrical', '4w', 1000, 6000, 'Battery not charging, warning light'),
            # AC
            ('AC not cooling', 'ac', '4w', 500, 4000, 'Air not cold enough or warm air'),
            ('AC gas leaking / refill needed', 'ac', '4w', 800, 2500, 'Refrigerant low, AC blows warm'),
            ('AC compressor noise', 'ac', '4w', 1000, 8000, 'Rattling or clunking from AC compressor'),
            ('AC not working at all', 'ac', '4w', 500, 5000, 'Blower works but no cooling'),
            # BODY
            ('Body denting repair', 'body', 'all', 500, 10000, 'Door dings, dents from minor accidents'),
            ('Paint scratches / chips', 'body', 'all', 300, 5000, 'Surface scratches, paint peeling'),
            ('Rust spots / corrosion', 'body', 'all', 500, 8000, 'Rust on body panels'),
            ('Windshield crack / chip', 'body', '4w', 500, 5000, 'Cracked or chipped windshield'),
            # TRANSMISSION
            ('Gear shifting difficult', 'transmission', 'all', 300, 5000, 'Hard to shift gears or slips out'),
            ('Clutch slipping / heavy', 'transmission', 'all', 800, 6000, 'Clutch not engaging fully, high clutch point'),
            ('Transmission fluid leak', 'transmission', '4w', 500, 3000, 'Red fluid dripping, burning smell'),
            ('Gear box noise', 'transmission', 'all', 500, 8000, 'Grinding or whining in gear'),
            # FUEL
            ('Poor fuel economy', 'fuel', 'all', 300, 2000, 'Noticeably more fuel consumption'),
            ('Fuel leaking / smell', 'fuel', 'all', 500, 3000, 'Strong petrol/diesel smell, visible leak'),
            ('Engine sputtering on acceleration', 'fuel', 'all', 300, 3000, 'Hesitation, stumbling when accelerating'),
            # SERVICE
            ('Periodic service due', 'service', 'all', 499, 2999, 'Routine oil change and service by KM'),
            ('Full vehicle check-up', 'service', 'all', 499, 1999, 'Complete 50-point vehicle inspection'),
            ('Pre-trip inspection', 'service', 'all', 299, 599, 'Safety check before long trip'),
            # HEAVY VEHICLE
            ('Air brake failure', 'brakes', 'heavy', 2000, 10000, 'Truck/bus air brake not working'),
            ('Engine overhaul needed', 'engine', 'heavy', 15000, 50000, 'Major engine reconditioning'),
            ('Leaf spring broken', 'brakes', 'heavy', 2000, 8000, 'Suspension leaf spring damaged'),
        ]
        count = 0
        for i, (name, cat, vtype, cmin, cmax, desc) in enumerate(issues):
            _, created = RepairIssue.objects.get_or_create(
                name=name, vehicle_type=vtype,
                defaults={'category': cat, 'estimated_cost_min': cmin,
                          'estimated_cost_max': cmax, 'description': desc,
                          'is_active': True, 'display_order': i}
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {count} repair issues'))

    def create_workers_for_all_centers(self):
        from accounts.models import User, Employee
        from core.models import ServiceCenter
        centers = ServiceCenter.objects.filter(is_active=True)
        designations = ['mechanic', 'mechanic', 'electrician', 'painter', 'worker', 'worker']
        first_names  = ['Rajesh','Suresh','Ramesh','Naresh','Mahesh','Ganesh','Venkat','Srinivas','Murali','Kiran',
                        'Ravi','Pavan','Anil','Sunil','Tarun','Varun','Arun','Jagan','Srinu','Balu',
                        'Chandu','Madhu','Ramu','Shiva','Gopi','Nani','Bunny','Babu','Raju','Hari']
        last_names   = ['Rao','Reddy','Kumar','Naidu','Sharma','Babu','Varma','Swamy','Das','Raju']
        count = 0
        mobile_base  = 8100000000
        emp_id_base  = 5000

        for ci, center in enumerate(centers):
            # Check if center already has workers
            existing = Employee.objects.filter(service_center=center).count()
            if existing >= 4:
                continue
            needed = max(0, 4 - existing)
            for wi in range(needed):
                mobile = str(mobile_base + ci * 10 + wi)
                emp_id = f'WRK{emp_id_base + ci * 10 + wi}'
                if User.objects.filter(mobile_number=mobile).exists():
                    continue
                fname = first_names[(ci * 6 + wi) % len(first_names)]
                lname = last_names[(ci + wi) % len(last_names)]
                desig = designations[wi % len(designations)]

                user = User.objects.create(
                    mobile_number=mobile, first_name=fname, last_name=lname,
                    role='employee', is_verified=True,
                )
                user.set_password('worker@123')
                user.save()

                Employee.objects.create(
                    user=user, employee_id=emp_id,
                    designation=desig, service_center=center,
                    joining_date=__import__('datetime').date(2024, 1, 1),
                    salary=16000, is_active=True,
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✅ Added {count} workers across all service centers'))
