# Electric Skate Board esk8

The Kv rating of a motor is the constant velocity of a motor without load. RPM = Kv x Voltage 

Example calculation:

Speed [km/hr] = 3.141 x 147 [wheel diameter in mm] x 1/1,000,000 [km/mm] x 15T/60T [pulley to gear ratio] x  170Kv * (10x*3.7-4.2) [V] x 60 [min/hr] = 50km/hr

## ESC 
* odrive https://odriverobotics.com/ 56V, 2x120A peak, $149, 40A with passive cooling goes to 70-80C in 5 mins
* trampa vesc 6mk >$200
* https://maytech.cn/ 
* [FocBox Aliexpress](https://www.aliexpress.com/item/4000834490546.html?spm=a2g0o.detail.1000014.29.936639d8J5EdAo&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.14976.158757.0&scm_id=1007.14976.158757.0&scm-url=1007.14976.158757.0&pvid=1db38406-09ba-49c5-b953-4eab00dbb4d9&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.14976.158757.0,pvid:1db38406-09ba-49c5-b953-4eab00dbb4d9,tpp_buckets:668%230%23131923%2320_668%23808%234093%23864_668%23888%233325%2312_4976%230%23158757%230_4976%232711%237538%23261_668%232846%238111%23436_668%232717%237559%2337)

## Motors
6374 is diameter and length of the motor in [mm].

### Hobby King
* 6374 245KV Turnigy Aerodrive SK3, 70A, 2700W, 8mm shaft, M4 33mm bolt hole spacing, 12S, sensor less $90
* 6374 192KV Turnigy Aerodrive SK3, 80A, 4032W, 8mm shaft, M4 44mm bolt hole spacing, 12S, sensor less $90
* 6374 149KV Turnigy Aerodrive SK3, 70A, 2250W, 4mm shaft, M4 32mm bold hold spacing, 12S, sensor less $90
* 6374 192KV Turnigy SK8,12S,      100A, 4400W, 8mm shaft, M4 44mm blot hole spacing, 12S, sensored $97
* 6374 149KV Turnigy SK8,           80A, 3500W, 8mm shaft, M4 44mm blot hole spacing, 12S, sensored $97

SK8 is 89mm long plus 38mm shaft

Torque Calculation: Troque [Nm] = 3/2/(sqrt(3)*(1/60)*2*3.141) * MaxCurrent / Kv.

* Turnigy SK8: 8.3*100/192 = 4Nm
* Turnigy SK3: 8.3*80/192 = 3.4Nm

If the motor is run at reduced voltage the current is likely decreasing by the same amount.

### [DIYElectricSkateboard](https://diyelectricskateboard.com/products/electric-skateboard-motor-6374-190kv)
* 6374 190KV 80A, 3150W, 8mm, 12S, sensored, $120
* 6380 170KV 80A, 4100W, 8mm, 12S, sensored, $135

## Wheels
### All Terrain
* Haggyboard 
  * Haggyboard Bergmeister: 147mm diameter 45mm width 608 type bearings, 4 pneumatic wheels $196.84
  * Bergmeister tire $20
* DIYelectric
  * DYIElectric 160mm all-terrain tire kit w/ 62T pulley, carbon enforced plastic $150 [Wheel kit] (https://diyelectricskateboard.com/products/160mm-all-terrain-tire-kit)
  * DYIElectric tire $19
* Evolve
  * Evolve wheel 152 or 178mm $34, Pulley 47T, Motor Gear 14T $15, Belt $30, 
  * Evolve tire $20

## Trucks
* HaggybBoard
  * Kahua, 8mm axle, hanger width 210mm, 63m outside hanger, set of two  $145 
  * Kahua, with motor mount $160 
* Torqueboard DIYeboard
  * 8mm axle, hanger 218mm set of two $65
  * CNC truck 220mm set of two $260
  * 133mm motor mount 2 x $60, inward mount
  * 160mm reverse motor mount 2 x $60, outward mount
* Evolve Trucks
  * 235mm hanger, 305mm total width GTR version L$45 
  * Evolve motor mount from DIYeboard $80 set of two [MotorMount](https://diyelectricskateboard.com/products/63mm-reverse-motor-mount-set)
  * https://www.evolveskateboards.co.uk/collections/carbon-gt-at/products/gt-truck-front-or-rear?variant=42152336784


* SURFRODZ, hanger width  177mm, not wide enough, kit of two $120

## Drive Gears
* Haggy board: 60T, 5mm pitch, 15mm Nylon with steel fibers belt, all terrain 88.41 
* DIYesakteboard Motor Pulley 16T HTD5 15mm [Pulley](https://diyelectricskateboard.com/products/16t-htd5-15mm-motor-pulley?variant=7290917847063&currency=USD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gclid=Cj0KCQjwoPL2BRDxARIsAEMm9y_YFJFkJxs9a1j4Jel6Cp-UZeJ8B3uH65X2a9VpLfMqZ88Eika0ilIaAlr6EALw_wcB) $16.75

## Bearings
6001 -> 12mm Trucks
16100-A-2Z 10mm Trucks

## Electronics

ODrive ESC has 120A peak per motor and 40A will increase temperature of controller to 70-80C. The 6374 motors have max current of 70-100A. The design should be 40A sustainedand 100A for 5-10 sec per motor. For two motors that is 80A sustained and 200A max.

BMS should be 80A with 250A over discharge trip
Wire into BME 8AWG from battery
Wire into odrive 8AWG with EC5 Connector
Wire into 6374 10-12AWG for 4mm bullet plug 

## Battery
The fully charged lithium ion battery is 4.2V and nominal voltage is 3.7V. To achieve higher voltage batteries are connected in serial fashion.
A 10S LiPo is 10 batteries in series which creates 10x4.2 = 42V (37V nominal at 3.7V), with 12S 50V (44V) and with 13S 55V (48V). The maximum voltage on the odrive controller is 56V or 13S. 

The baja boards have 10S4P or 10S6P battery configuration which results in 550Wh/900Wh battery capacity.

For airline transportation, spare uninstalled rechargeable batteries are limited to 100Wh per battery. There is no limit for personal use of those battery packs. With airline approval, a passenger may also carry two separate batteries of 101-160Wh. The battery needs to be at less than 30% of maximum capacity when taken on the plane. A single LiPo battery 3.7V x 2.6Ah = 9.6Wh. With 13S that is 125Wh. One would need to use 10S configuration to stay below 100Wh or carry the battery cells individually.

A 6374 motor can take up to 70-100A at 12S. When designing with 18650 batteries one needs two to three battery packs as they can discharge up to 35-40A each.

For maximum performance one should design 13S battery pack with two to three battery packs per motor.

When one uses multiple battery packs they are connected in parallel but each batter pack needs its own battery management board (charging and discharge protection as well as balancing). 

### Round Batteries with flat top
[Battery Store 18650](https://www.18650batterystore.com)
* 21700 Molicel P42A, 4200mAh 45A $7, 21.6x70.5
* 18650 Molicel P26A, 2600mAh 35A $5, 18x65mm, 2.6A/6A(max) charge current
* 18650 Panasonic NCR18650Bm 3400mAh, 5A, $5

For 4 packs and each at 13S one needs 52 batteries and for 6 packs 78.

### Battery Holder 
* https://vruzend.com/product/hexagonal-18650-battery-holders-3-cell/
* [uxcell](https://www.amazon.com/uxcell-Lithium-Battery-Double-Bracket/dp/B011HFLFEG) $12
 
### Battery Management System
Battery Protection Circuit
* 10S
  * [Amazon 40A](https://www.amazon.com/DC42-45V-Battery-Protection-Li-ion-Balance/dp/B074WZL5NF/ref=as_li_ss_tl?ie=UTF8&qid=1516403962&sr=8-1&keywords=10s+bms&linkCode=sl1&tag=just02b0-20&linkId=7f7b9e6774097882321903664d9a5a53) $ 18
  * [Deligreen Aliexpress 40A](https://www.aliexpress.com/item/33022056455.html?spm=a2g0o.productlist.0.0.132695a1PiPb1M&algo_pvid=999571a7-8b2b-4c6b-bc78-c4ae1202a862&algo_expid=999571a7-8b2b-4c6b-bc78-c4ae1202a862-25&btsid=0ab50f0815909718661574034eae7e&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_), 18.98
* 13S 
  * [Amazon Causin 35A Upgrade](https://www.amazon.com/Rechargeable-Lithium-Liion-Battery-13S30A-Upgrade/dp/B082SCPL9N/ref=pd_sbs_147_2/135-0325508-0159315?_encoding=UTF8&pd_rd_i=B082SCRWS4&pd_rd_r=1fa0928a-7c27-476a-94b5-405942232f00&pd_rd_w=I1XQs&pd_rd_wg=mtQ9m&pf_rd_p=12b8d3e2-e203-4b23-a8bc-68a7d2806477&pf_rd_r=633WK7CTD7K2AV99KT47&refRID=633WK7CTD7K2AV99KT47&th=1) $23, 50x80mm
  * [Amazon KKmoon 35A](https://www.amazon.com/KKmoon-Battery-Protection-Integrated-Circuits/dp/B07X8M83QG/ref=pd_sbs_147_3/135-0325508-0159315?_encoding=UTF8&pd_rd_i=B07X8M83QG&pd_rd_r=1fa0928a-7c27-476a-94b5-405942232f00&pd_rd_w=I1XQs&pd_rd_wg=mtQ9m&pf_rd_p=12b8d3e2-e203-4b23-a8bc-68a7d2806477&pf_rd_r=633WK7CTD7K2AV99KT47&psc=1&refRID=633WK7CTD7K2AV99KT47) $17, 51x69mm
  * [Amazon Causin 30A](https://www.amazon.com/Rechargeable-Lithium-Liion-Battery-13S30A-Upgrade/dp/B082SCRWS4/ref=pd_sbs_23_3/135-0325508-0159315?_encoding=UTF8&pd_rd_i=B082SCRWS4&pd_rd_r=d352e308-f195-452c-a16e-cd4334971997&pd_rd_w=HW0ac&pd_rd_wg=MaLC8&pf_rd_p=12b8d3e2-e203-4b23-a8bc-68a7d2806477&pf_rd_r=GJJQ9H2G32AF5XH62A0Q&psc=1&refRID=GJJQ9H2G32AF5XH62A0Q) $18, 50x80mm
  * [Amazon Paialu 45A](https://www.amazon.com/Li-ion-Lipolymer-Battery-Protection-Balance/dp/B07PG2Z9RB/ref=sr_1_3?dchild=1&keywords=13s+bms&qid=1590955382&s=industrial&sr=1-3) $29 60x120mm
  * [Amazon DALY BMS 100A](https://www.amazon.com/Current-Tricycle-Motorcycle-Inverter-Balance/dp/B087JF517P/ref=pd_sbs_23_4/135-0325508-0159315?_encoding=UTF8&pd_rd_i=B087JF517P&pd_rd_r=45191d64-6d30-426a-a086-afb56bfb9886&pd_rd_w=SWqn6&pd_rd_wg=j734x&pf_rd_p=12b8d3e2-e203-4b23-a8bc-68a7d2806477&pf_rd_r=QN1CTVYB33FDQGNJY5R8&psc=1&refRID=QN1CTVYB33FDQGNJY5R8) $68, 66x150mm
  * [Amazon DALY BMS 60A] $34
  * [Amazon DALY BMS 50A](https://www.amazon.com/DALY-Battery-managment-Discharge-Electric/dp/B0876PW4MX/ref=sr_1_2?dchild=1&keywords=DALY+BMS+13S&qid=1590964740&sr=8-2) $28, 61x80mm
  * [Amazon DALY BMS 40A] $25
  * [Amazon DALY BMS 25A] $32
  * [Amazon AYMARIO 20A](https://www.amazon.com/Lithium-Battery-Protection-Function-Batteries/dp/B07NHHL3DY/ref=olp_product_details?ie=UTF8&me=&qid=1590965687&sr=1-1) $24, 49x66mm

  * [Aliexpress](https://www.aliexpress.com/item/4000918063364.html?spm=a2g0o.productlist.0.0.33f72e54dlYqrq&ad_pvid=202005311612357180131457934610005919249_1&s=p) 35A (125) $8, 52x69
  * [Aliexpress](https://www.aliexpress.com/item/4001065824185.html?spm=a2g0o.productlist.0.0.33f72e54dlYqrq&algo_pvid=d7713592-8bfa-4c22-9836-9f33fe4bae42&algo_expid=d7713592-8bfa-4c22-9836-9f33fe4bae42-7&btsid=0ab6fb8315909672817281070eaf56&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_), 35A, $14 for two
  * [Aliexpress Broodio]() 40A (125) $17
  * [Aliexpress Broodio](https://www.aliexpress.com/item/4000372642579.html?spm=a2g0o.productlist.0.0.33f72e54dlYqrq&algo_pvid=33c23fff-1ef1-409d-a319-7faf8f32d6bf&algo_expid=33c23fff-1ef1-409d-a319-7faf8f32d6bf-0&btsid=0ab6d69f15909659598455140e5742&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) 60A $23
  * [ebay](https://www.ebay.com/itm/US-35A-BMS-PCB-PCM-Protection-Board-With-Balance-For-E-bike-Li-ion-Battery-13S/133417323146?hash=item1f104aca8a:g:wQQAAOSwPuFex6gT) 35A (100) $16
  * [Deligreen, Aliexpress, Separate, 15,20,30,40,50,60](https://www.aliexpress.com/item/32888880741.html?spm=a2g0o.productlist.0.0.33f72e54dlYqrq&algo_pvid=d7713592-8bfa-4c22-9836-9f33fe4bae42&algo_expid=d7713592-8bfa-4c22-9836-9f33fe4bae42-29&btsid=0ab6fb8315909672817281070eaf56&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $22 for 40A (165)

  https://www.aliexpress.com/item/4000245584923.html?spm=a2g0o.productlist.0.0.2bdde4c5TzbfVk&algo_pvid=430ab711-b32a-4532-87ec-ce7bb45a691f&algo_expid=430ab711-b32a-4532-87ec-ce7bb45a691f-12&btsid=0ab6d69515918458467542780e8a4b&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_ 24 for 80A 50A continous

  https://www.aliexpress.com/item/33017110340.html?spm=a2g0o.productlist.0.0.1c5de4c5WQgfuS&algo_pvid=b734fbb0-5dcd-492d-9485-0da5c70510b1&algo_expid=b734fbb0-5dcd-492d-9485-0da5c70510b1-20&btsid=0ab6f83a15918464959321806e184f&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_ 80A for $26

  https://www.aliexpress.com/item/10000214354490.html?spm=a2g0o.productlist.0.0.1c5de4c5WQgfuS&algo_pvid=b734fbb0-5dcd-492d-9485-0da5c70510b1&algo_expid=b734fbb0-5dcd-492d-9485-0da5c70510b1-7&btsid=0ab6f83a15918464959321806e184f&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_ 80A $40

https://www.aliexpress.com/item/32850497316.html?spm=2114.12010612.8148356.2.193562bbnnZmjz Daligreen 80A for $44, 100A for 58 and 120A for $83

### Connectors 
* JST 5A (10A)
* XT90 90A, 8AWG
* XT60 60A (180A), 12AWG
* EC5 120A, 5mm 8-10AWG, 4.77mm solder cup
* EC3 60A, 3.5mm
* 4mm bullet plug 70A
* 6mm bullet plug 120A
* 8mm bullet plug 200A

## Wire
Silicone insulated wire with 200C temperature rating.

[1] https://sparks.gogo.co.nz/silicone-wire-current-capacity.html
[2] https://www.4-max.co.uk/silicone-wire.htm
[3] https://www.multicable.com/resources/reference-data/current-carrying-capacity-of-copper-conductors/

*  8AWG 3.26mm, 8.37mm2 209A 180A 100A  
* 10AWG 2.59mm, 5.26mm2 130A 120A  75A  burst 250A
* 12AWG 2.05mm, 3.31mm2  75A  70A  55A  burst 160A

Approximation for current A[mm2]*25
Approximation for current (D[mm]*39)^2 / 80

Single core to multicore up to 1/3 factor

### Battery Charger
For 13S you need  54.6V charger. 
* [Amazon 54.6V 13S 6A](https://www.amazon.com/Battery-Charger-Lithium-90-230V-54-6V6A/dp/B07VSNBJR2) $78
* [Amazon 54.6 13S 4A](https://www.amazon.com/Charger-Electric-Battery-Scooter-Motorcycle/dp/B07P7GHY3L/ref=pd_di_sccai_4/144-1181655-6631115?_encoding=UTF8&pd_rd_i=B07PBVTZ67&pd_rd_r=5f27bd13-b8a6-4afa-abbd-3448ef7fb9a9&pd_rd_w=sPP9w&pd_rd_wg=ZrcAL&pf_rd_p=61ce50cf-2379-4458-9044-fa8b402c702d&pf_rd_r=C4FE2TY6P226K0SBY244&refRID=C4FE2TY6P226K0SBY244&th=1), $58
* [Aliexpress 13S 7A](https://www.aliexpress.com/item/32979899647.html?spm=a2g0o.productlist.0.0.3f8227049ZdB3B&algo_pvid=8450172b-cddf-46e0-a378-59c820ba1ac2&algo_expid=8450172b-cddf-46e0-a378-59c820ba1ac2-6&btsid=0ab6d67915909767797998084e7fea&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $47
* [Aliexpress 13S 4A](https://www.aliexpress.com/item/32870181959.html?spm=a2g0o.productlist.0.0.3f8227049ZdB3B&algo_pvid=8450172b-cddf-46e0-a378-59c820ba1ac2&algo_expid=8450172b-cddf-46e0-a378-59c820ba1ac2-17&btsid=0ab6d67915909767797998084e7fea&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $38
* [Aliexpress 12A](https://www.aliexpress.com/item/4000193014157.html?spm=a2g0o.productlist.0.0.3f8227049ZdB3B&algo_pvid=8450172b-cddf-46e0-a378-59c820ba1ac2&algo_expid=8450172b-cddf-46e0-a378-59c820ba1ac2-35&btsid=0ab6d67915909767797998084e7fea&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $206
* [Aliexpress T500 Ant Charger 8A](https://www.aliexpress.com/item/4000394843267.html?spm=a2g0o.productlist.0.0.3f8227049ZdB3B&algo_pvid=413d0752-30c6-491e-ae1d-11a9a16fa37b&algo_expid=413d0752-30c6-491e-ae1d-11a9a16fa37b-10&btsid=0ab6f83a15909774883345344e3191&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $65 **
* [Aliexpress 10A](https://www.aliexpress.com/item/32986399986.html?spm=a2g0o.detail.1000014.1.936639d8NgGimi&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.14976.158757.0&scm_id=1007.14976.158757.0&scm-url=1007.14976.158757.0&pvid=e15aeea8-2e4e-4509-924a-1278e487b3e6&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.14976.158757.0,pvid:e15aeea8-2e4e-4509-924a-1278e487b3e6,tpp_buckets:668%230%23131923%234_668%23808%234093%23864_668%23888%233325%2312_4976%230%23158757%230_4976%232711%237538%23261_668%232846%238111%23436_668%232717%237559%2337) $85

## Remote Control
* dyeboard RC6 2.4Ghz $20
* dyeboard RC5 2.4Ghz $20
* dyeboard RC7 2.4Ghz $20
* Enertion Nano-X, http://www.enertionboards.com/
* DIYElectric Torqueboard Control&Receiver $46
* Miami Electric Boards Remote 278 (Benchwheel)
* Benchwheel.com Remote & Receiver 2.4 GHz $54


## Decks
* 
# Resources
AVIO MK2 Drive

https://haggyboard.com 340mm(210mm) total for flat board
https://trampaboards.com 406mm total for tilted end board
https://buildkitboards.com compact
https://www.mbs.com/parts 411mm total for tilted end board
https://www.meepoboard.com 245&265 (200mm) for flat board
https://evolveskateboardsusa.com/ flat board, complete systems
https://diyelectricskateboard.com flat boards
https://benchwheel.com compact boards

https://forum.esk8.news/
https://electric-skateboard.builder
http://www.diyeboard.com/
https://forum.esk8.news/t/project-bluebeam/19337





Deck: https://www.ebay.com/sch/i.html?_from...
Wheel Motor Hubs: https://www.ebay.com/itm/90mm-dual-63...
Controller with remote: https://www.ebay.com/itm/Dual-motors-...
Vesc housing: https://www.ebay.com/itm/Plastic-dual...
HG2 Batteries: https://www.ebay.com/itm/10x-LG-HG2-1...
BMS X2: https://www.ebay.com/itm/5S-15A-Prote...
Charger: https://www.ebay.com/itm/42V-2A-charg...
Charger Plug: https://www.ebay.com/itm/Panel-Chassi...
Battery Holders: http://amzn.to/2yChsR6
Grip Tape: http://amzn.to/2ieljO9
