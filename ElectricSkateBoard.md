# Electric Skate Board esk8

- [Electric Skate Board esk8](#electric-skate-board-esk8)
  * [Design](#design)
    + [Power and Speed](#power-and-speed)
  * [Websites and Resources](#websites-and-resources)
  * [Design and Part Selection](#design-and-part-selection)
  * [Motors](#motors)
    + [[Hobby King 6374](https://hobbyking.com/en_us/catalogsearch/result/?q=6374)](#-hobby-king-6374--https---hobbykingcom-en-us-catalogsearch-result--q-6374-)
    + [[DIYElectricSkateboard 6374](https://diyelectricskateboard.com/products/electric-skateboard-motor-6374-190kv)](#-diyelectricskateboard-6374--https---diyelectricskateboardcom-products-electric-skateboard-motor-6374-190kv-)
  * [Wheels](#wheels)
    + [Haggyboard](#haggyboard)
    + [DIYelectricSakteboard](#diyelectricsakteboard)
    + [Evolve](#evolve)
    + [Drive Gears](#drive-gears)
    + [Motor Pulley](#motor-pulley)
  * [Drive systems](#drive-systems)
  * [Deck](#deck)
  * [Trucks](#trucks)
    + [HaggybBoard](#haggybboard)
    + [Evolve](#evolve-1)
    + [[eskatebuilder](https://eskatebuilder.com/product/double-kingpin-trucks/) same as Evolve trucks](#-eskatebuilder--https---eskatebuildercom-product-double-kingpin-trucks---same-as-evolve-trucks)
    + [SURFRODZ](#surfrodz)
  * [Bearings](#bearings)
  * [Electronics](#electronics)
    + [ESC](#esc)
    + [Main Switch and Charging Port](#main-switch-and-charging-port)
    + [Battery](#battery)
      - [Nickel Strip Current Capacity](#nickel-strip-current-capacity)
      - [Battery Holder](#battery-holder)
    + [Battery Management System](#battery-management-system)
    + [Battery Charger](#battery-charger)
    + [Remote Control](#remote-control)
  * [Deck](#deck-1)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Design
### Power and Speed
The Kv rating of a motor is the constant velocity of a motor without load. RPM = Kv x Voltage 

Example calculation:

Speed [km/hr] = 3.141 x 147 [wheel diameter in mm] x 1/1,000,000 [km/mm] x 15T/60T [pulley to gear ratio] x  170Kv * (10x*3.7-4.2) [V] x 60 [min/hr] = 50km/hr

Torque Calculation: Troque [Nm] = 3/2/(sqrt(3)*(1/60)*2*3.141) * MaxCurrent / Kv.

* Turnigy SK8: 8.3*100/192 = 4Nm
* Turnigy SK3: 8.3*80/192 = 3.4Nm

[VSEC calcuator](https://vesc-project.com/calculators)

Tire diameter 160  
Motor pulley 16  
Slave 62  
MotorKV sk3 c6374 192  
Serial Cells 12  
Parallel Cell 6  
Battery 35A 2600mAh  
Weigth 130kg  
100% throttle 0% climb 65Kmh 12minute drive  (40miles per hour)
100% throttle 10% climb 65Kmh 7minute drive  
40% throttle 0% climb 25Kmh 127minute drive  
40% throttle 10% climb 25Kmh 30minute drive  

## Websites and Resources
* Trampa Boards https://trampaboards.com/ many components, 406mm tilted end boards
* Build Kit Boards https://buildkitboards.com compact
* DIYEBoard http://www.diyeboard.com
* MBS https://www.mbs.com/parts 411mm trucks for tilted end board
* meepoboard https://www.meepoboard.com 245&265 (200mm) for flat board
* Evolve https://evolveskateboardsusa.com/ flat board, complete systems
* Baja Board https://www.bajaboard.com.au/, complete systems
* Propel https://www.ridepropel.com/, complete systems
* DIY electric skate board https://diyelectricskateboard.com flat boards
* Benchwheel https://benchwheel.com compact boards
* Build Kit https://buildkitboards.com compact

**Discussion Forums**  
https://forum.esk8.news/  
https://electric-skateboard.builders/  

---
## Design and Part Selection
---
The design should be 40A sustained and 100A for 5-10 sec per motor. For two motors that is 80A sustained and 200A max current.

**ESC**  
ODrive: 56V, 120A peak per motor. 40A will increase temperature of controller to 70-80C. The 6374 motors have max current of 70-100A. 

**Motors**  
192KV Turnigy SK8: 100A, 12cells, 4400W, 14 poles

**Trucks**  
Kingpin type from eskatebuilder, 370mm with motor mount 64mm, 

**Wheels**  
160mm all-terrain tire kit   
2 x 410mm hdt5 15mm belt  
2 x 62T HTD5 15mm drive wheel pulleys  
1 x ABEC7 bearing set  
Extra  
2 x 16T HTD5 15mm Motor Pulley  
slot key 3x3mm, 8mm bore

**BMS**  
Daligreen 80A, 250A over discharge, 13S

**Wiring**  
Battery to ODrive 8AWG  
Charging Connector to BMS 12AWG
Odrive to motor 12AWG
Break Resitor 12AWG

**Connectors**  
Using 8mm short bullet plugs for battery and 4mm bullet plug for motors

**Remote**  
Samsung gear BLE to Raspi, custom software

**Batteries**  
78 x 18650 Molicel P26A, 2600mAh 35A, 6Amp max charge
Nickel strips
13S6P = 210A, 41.6-54.5V, 48 nominal, 36A max charging

**Charger**  
WATE 13S 54.6V 7A Charger 48V, Aliexpress

**Deck**  
Aluminum Frame  

Bottom plate Aluminum  
Top plate Aluminum  
Cover plate Polycarbonate  
[onShape Design](https://cad.onshape.com/documents/780cf0791f6ea0020182cc37/w/52c93acc8a7040ecf66f8b0d/e/6630977b7a9cc9a77ba8d62b)
3/4 x 1/5 inch square tubing:
 - 29.75in x2 (side)
 - 6.5in x1 (battery separator)
 - 8.5in x2  (prependituclar front back)
 - 6.75in x4 (longitudinal front back)
 - 2.5in x8  (front back and fill ins)

---
## Motors
---
The number 6374 is the diameter and length of the motor in [mm].

### [Hobby King 6374](https://hobbyking.com/en_us/catalogsearch/result/?q=6374)
* 245KV Turnigy Aerodrive SK3, 70A, 2700W, 8mm shaft, M4 33mm bolt hole spacing, 12S, sensor less $90
* 192KV Turnigy Aerodrive SK3, 80A, 4032W, 8mm shaft, M4 44mm bolt hole spacing, 12S, sensor less $90
* 149KV Turnigy Aerodrive SK3, 70A, 2250W, 4mm shaft, M4 32mm bold hold spacing, 12S, sensor less $90
* 192KV Turnigy SK8,12S,      100A, 4400W, 8mm shaft, M4 44mm blot hole spacing, 12S, sensored $97
* 149KV Turnigy SK8,           80A, 3500W, 8mm shaft, M4 44mm blot hole spacing, 12S, sensored $97 89mm long plus 38mm shaft

**Hall Sensor Wire** 
- Red V++ (5V)
- Blu Temp
- Grn Hall1 - ODrive Hall A
- Wht Hall2 - ODrive Hall B
- Brw Hall3 - ODrive Hall Z
- Blk GND

Supply votlage 3.3 to 5V. VESEC has switch to select Vcc or 5V. ODrive eitehr 5V or VCC, examples use 5V.
Hall sensor pulls output to ground. It has built in voltag regulator. On ODrive board, Hall output is pulled high (3.3V) with 3.3k resitor (2k2 on VESEC).
Hall sensors need 22-47nF to GND to supress noise. Can turn off invalid Hall state in ODrive software (ignore_illegal_hall_state = True)

Thermistor is 10k Thermisotor
Pull high to VCC and place capcitor to ground. VESEC: 10k and 100nF, ODrive 3.3k and 2.2uF.

```
Turnigy SK8 6374-192KV Sensored Brushless Motor (14P)
14 Poles
100A, 4440W
Idle Current 1.8A
9-12S LiPo
24MΩ Resistance
44mm bolt hole spacing, M4, 8mm Shaft
Plug pin 4mm
Resistance 24mH
Max Voltage 45V
940gr
4.0 banana Gold plug
Length w/ hubs B w/o shaft: 80.7mm
Can Diameter C: 61.0mm
Can Length D: 67.0mm
Total Shaft Length E: 126.7mm
```

### [DIYElectricSkateboard 6374](https://diyelectricskateboard.com/products/electric-skateboard-motor-6374-190kv)
* 190KV 80A, 3150W, 8mm, 12S, sensored, $120
* 6380 170KV 80A, 4100W, 8mm, 12S, sensored, $135

---
## Wheels
---
### Haggyboard 
  * Haggyboard Bergmeister: 147mm diameter 45mm width 608 type bearings, 4 pneumatic wheels $196.84
  * Bergmeister tire $20

### DIYelectricSakteboard
  * 160mm all-terrain tire kit w/ 62T pulley, carbon enforced plastic $150 [Wheel kit](https://diyelectricskateboard.com/products/160mm-all-terrain-tire-kit)
    * Select 410mm hdt5 15mm belt optioin
    * Includes Tires, Tubes, Hub,  2x 62T HTD5 15mm Drive Wheel Pulleys, 2x 410mm HTD5 15mm Drive Belts, 1x ABEC7 Bearing Set
  * Needs 2 x 16T HTD5 15mm Motor Pulley, slot key 3x3mm, 8mm bore, 25.4mm
$16.75
  * Replacement Tire $19

### Evolve
  * Evolve wheel 152 or 178mm $34, Pulley 47T, Motor Gear 14T $15, Belt $30, 
  * Evolve tire $20

### Drive Gears
* Haggy board: 60T, 5mm pitch, 15mm Nylon with steel fibers belt, all terrain 88.41 

### Motor Pulley
* DIYesakteboard Motor Pulley 16T HTD5 15mm [Pulley](https://diyelectricskateboard.com/products/16t-htd5-15mm-motor-pulley?variant=7290917847063&currency=USD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gclid=Cj0KCQjwoPL2BRDxARIsAEMm9y_YFJFkJxs9a1j4Jel6Cp-UZeJ8B3uH65X2a9VpLfMqZ88Eika0ilIaAlr6EALw_wcB) $16.75

## Drive systems
[AVIO MK2 Drive](https://forum.esk8.news/t/in-stock-herringbone-gears-avio-mk2-gear-drive/3672)  

---
## Deck
* [eskatebuilder](  /product/flexible-deck/)
* https://www.volokno-esk8.ru/

Grip Tape: http://amzn.to/2ieljO9

---
## Trucks
---
### HaggybBoard
  * Kahua, 8mm axle, hanger width 210mm, 63m outside hanger, set of two  $145 
  * Kahua, with motor mount $160 
##3 Torqueboard DIYeboard
  * 8mm axle, hanger 218mm set of two $65
  * CNC truck 220mm set of two $260
  * 133mm motor mount 2 x $60, inward mount
  * 160mm / 63mm reverse motor mount 2 x $60, outward mount
### Evolve
  * 235mm hanger, 305mm total width GTR version L$45 
  * Evolve motor mount from DIYeboard $80 set of two [MotorMount](https://diyelectricskateboard.com/products/63mm-reverse-motor-mount-set)
  * https://www.evolveskateboards.co.uk/collections/carbon-gt-at/products/gt-truck-front-or-rear?variant=42152336784

### [eskatebuilder](https://eskatebuilder.com/product/double-kingpin-trucks/) same as Evolve trucks
  * 305 or 370mm $79 (wide version) **
  * Motor mount, 64mm distance $39 **

### SURFRODZ
   * hanger width  177mm, not wide enough, kit of two $120

## Bearings
6001 -> 12mm Trucks
16100-A-2Z 10mm Trucks

---
## Electronics
---

### ESC
An electronic speed control is needed for DC motors.

* [odrive](https://odriverobotics.com/) 56V, 2x120A peak, $149, $279
* [trampa](https://trampaboards.com/vesc--c-1434.html) vesc 6mk, 60V 100A, 75/300 and 100/250, $236 for single motor
* [maytech](https://maytech.cn/) MTVESC50A 50A 12S, $55, 100A 12S $165, 50A dual $177
* Unity [FocBox AliExpress](https://www.aliexpress.com/item/4000834490546.html?spm=a2g0o.detail.1000014.29.936639d8J5EdAo&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.14976.158757.0&scm_id=1007.14976.158757.0&scm-url=1007.14976.158757.0&pvid=1db38406-09ba-49c5-b953-4eab00dbb4d9&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.14976.158757.0,pvid:1db38406-09ba-49c5-b953-4eab00dbb4d9,tpp_buckets:668%230%23131923%2320_668%23808%234093%23864_668%23888%233325%2312_4976%230%23158757%230_4976%232711%237538%23261_668%232846%238111%23436_668%232717%237559%2337), 50V, 160A continous, 300A max, $250


### Main Switch and Charging Port

* [XLR socket](https://www.amazon.com/gp/product/B07VRYS4YD/ref=ox_sc_act_title_1?smid=A2VPI5RFYNE0AS&psc=1)
* [XLR socket plug](https://www.amazon.com/dp/B07M7LMSB7?psc=1&pf_rd_p=6ee60839-fe55-4da7-916f-6c976c852767&pf_rd_r=7BBKT5MFGM0D51AGFGMM&pd_rd_wg=Ms8XB&pd_rd_i=B07M7LMSB7&pd_rd_w=4jC8y&pd_rd_r=64f9c58c-0603-41f6-95de-063747505d8d&ref_=pd_luc_rh_ci_mcx_mr_huc_d_04_01_t_img_lh)

Switch
* https://www.volokno-esk8.ru/


### Battery
---

A good video to show the making of a battery pack is https://www.youtube.com/watch?v=f9fZZVfcBVQ  
The fully charged lithium ion battery is 4.2V and nominal voltage is 3.7V. To achieve higher voltage, batteries are connected in serial fashion.
A 10S LiPo is 10 batteries in series which creates 10x4.2 = 42V (37V nominal), with 12S 50V (44V) and with 13S 55V (48V). 

Dimensions of **18650** battery is **18mm** diameter and **65mm** length  and a 21700 is 21x70mm

The baja boards have 10S4P or 10S6P battery configuration which results in 550Wh/900Wh battery capacity.

For airline transportation, spare uninstalled rechargeable batteries are limited to 100Wh per battery. There is no limit for personal use of those battery packs. With airline approval, a passenger may also carry two separate batteries of 101-160Wh. The battery needs to be at less than 30% of maximum capacity when taken on the plane. A single LiPo battery 3.7V x 2.6Ah = 9.6Wh. With 13S that is 125Wh. One would need to use 10S configuration to stay below 100Wh or carry the battery cells individually.

A 6374 motor can take up to 70-100A at 12S. When designing with 18650 batteries one needs two to three battery packs as they can discharge up to 35-40A each.

For maximum performance one should design 13S battery pack with two to three battery packs per motor.

Round Batteries with flat top from [Battery Store 18650](https://www.18650batterystore.com)
* 21700 Molicel P42A, 4200mAh 45A $7, 21.6x70.5
* 18650 Molicel P26A, 2600mAh 35A $5, 18x65mm, 2.6A/6A(max) charge current
* 18650 Panasonic NCR18650Bm 3400mAh, 5A, $5
* 18650 Samsung 30Q cells 3000mAh, 15A $5

For 4 packs at 13S one needs 52 batteries 
For 5 packs at 13S one needs 65 batteries 
For 6 packs at 13S one needs 78 batteries

Battery Welding: https://i.imgur.com/PezhnYr.jpg  
Battery PCB https://www.volokno-esk8.ru/

#### Nickel Strip Current Capacity

| Size| Max Current | Resistance  | 80A Heat | V Drop|
|-----------|-------------|------|-----|--|
| [mm]|[A]|[mO/m]|I^2 x R | I x R
| 0.1x5  | 2.1 - 3   | 137 | 880W/m | 11 V/m
| 0.1x7  | 3   - 5   | 98  | 630W/m | 7.8 V/m
| 0.15x7 | 4.7 - 7   | 65  | 416W/m | 5.2 V/m
| 0.15x8 | 5.3 - 8   | 57  | 365W/m | 4.6 V/m
| 0.2x7  | 6.5 - 10.6| 49  | 315W/m | 3.9 V/m
| 0.3x7  | 10  - 15  | 33  | 210W/m | 2.4 V/m

**Heat Transfer** of single strip (one side):  
Surface area 1m length = 0.008 m2  
Convection coefficient α = 25 W/(K·m2)  
Ambient temperature  = 30°C  
Wire Temperature = 200°C (same as silicone wire)
Heat Transfer = α x (T_a - T_0) * A = 25 x 170 x 0.008 = 34W/m

Maximum current for equilibrium of heat genereated versus heat disipated:  
I x I x Resistance = 34 W/m, solve for I  
I = sqrt(34/R) = 24 A  

This means that if we want 80A continuous current we need to achieve a resitance of 34 / (80 x 80) = 0.005 which requires adding 10 0.15mm strips together.

A better solution might be to make a PCB board and solder the strips onto it.

#### Battery Holder 
* [vruzend](https://vruzend.com/product/hexagonal-18650-battery-holders-3-cell/) $8 for 30 cells
* [uxcell](https://www.amazon.com/uxcell-Lithium-Battery-Double-Bracket/dp/B011HFLFEG) $12
* [Hexagonal 13](https://www.aliexpress.com/item/4000435080395.html?spm=a2g0o.detail.1000014.5.673d236f65aNfb&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.13338.142407.0&scm_id=1007.13338.142407.0&scm-url=1007.13338.142407.0&pvid=12f37d55-1983-493b-b8ef-0b8fd51dcbfe&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.13338.142407.0,pvid:12f37d55-1983-493b-b8ef-0b8fd51dcbfe,tpp_buckets:668%230%23177981%2317_668%23808%237756%23238_668%23888%233325%234_3338%230%23142407%230_3338%233142%239890%2310_668%232846%238109%23272_668%232717%237567%23951_668%233164%239976%23665) $5  
* Battery holder http://amzn.to/2yChsR6

### Battery Management System
---
The BME is a battery protection circuit, lmiting under voltage, current overdraw and balancing of the individual cells.

* 10S  
  * [Amazon Walfront 40A](https://www.amazon.com/DC42-45V-Battery-Protection-Li-ion-Balance/dp/B074WZL5NF/ref=as_li_ss_tl?ie=UTF8&qid=1516403962&sr=8-1&keywords=10s+bms&linkCode=sl1&tag=just02b0-20&linkId=7f7b9e6774097882321903664d9a5a53) $18
  * [Deligreen Aliexpress 40A](https://www.aliexpress.com/item/33022056455.html?spm=a2g0o.productlist.0.0.132695a1PiPb1M&algo_pvid=999571a7-8b2b-4c6b-bc78-c4ae1202a862&algo_expid=999571a7-8b2b-4c6b-bc78-c4ae1202a862-25&btsid=0ab50f0815909718661574034eae7e&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_), 18.98
* 13S  
  * AliExpress
    * [Daligreen 80,100.150,250A](https://www.aliexpress.com/item/32850497316.html?spm=2114.12010612.8148356.2.193562bbnnZmjz) 80A for $44, 100A for 58 and 120A for $83
     * [Daligreen, 15,20,30,40,50,60A](https://www.aliexpress.com/item/32888880741.html?spm=a2g0o.productlist.0.0.33f72e54dlYqrq&algo_pvid=d7713592-8bfa-4c22-9836-9f33fe4bae42&algo_expid=d7713592-8bfa-4c22-9836-9f33fe4bae42-29&btsid=0ab6fb8315909672817281070eaf56&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $22 for 40A
    * [Aliexpress](https://www.aliexpress.com/item/4000918063364.html?spm=a2g0o.productlist.0.0.33f72e54dlYqrq&ad_pvid=202005311612357180131457934610005919249_1&s=p) 35A (125) $8, 52x69
    * [Aliexpress](https://www.aliexpress.com/item/4001065824185.html?spm=a2g0o.productlist.0.0.33f72e54dlYqrq&algo_pvid=d7713592-8bfa-4c22-9836-9f33fe4bae42&algo_expid=d7713592-8bfa-4c22-9836-9f33fe4bae42-7&btsid=0ab6fb8315909672817281070eaf56&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_), 35A, $14 for two
    * [Broodio](https://www.aliexpress.com/item/4000372642579.html?spm=a2g0o.productlist.0.0.33f72e54dlYqrq&algo_pvid=33c23fff-1ef1-409d-a319-7faf8f32d6bf&algo_expid=33c23fff-1ef1-409d-a319-7faf8f32d6bf-0&btsid=0ab6d69f15909659598455140e5742&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) 60A $23, 40A (125) $17
    * [NonName](https://www.aliexpress.com/item/4000245584923.html?spm=a2g0o.productlist.0.0.2bdde4c5TzbfVk&algo_pvid=430ab711-b32a-4532-87ec-ce7bb45a691f&algo_expid=430ab711-b32a-4532-87ec-ce7bb45a691f-12&btsid=0ab6d69515918458467542780e8a4b&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $24 for (80A) 50A continous, $45 (150A) 110A
    * [QCCC](https://www.aliexpress.com/item/10000214354490.html?spm=a2g0o.productlist.0.0.1c5de4c5WQgfuS&algo_pvid=b734fbb0-5dcd-492d-9485-0da5c70510b1&algo_expid=b734fbb0-5dcd-492d-9485-0da5c70510b1-7&btsid=0ab6f83a15918464959321806e184f&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) 80A $40, 120A $48 150mmx105mm

  * Amazon
    * [Causin 35A](https://www.amazon.com/Rechargeable-Lithium-Liion-Battery-13S30A-Upgrade/dp/B082SCPL9N/ref=pd_sbs_147_2/135-0325508-0159315?_encoding=UTF8&pd_rd_i=B082SCRWS4&pd_rd_r=1fa0928a-7c27-476a-94b5-405942232f00&pd_rd_w=I1XQs&pd_rd_wg=mtQ9m&pf_rd_p=12b8d3e2-e203-4b23-a8bc-68a7d2806477&pf_rd_r=633WK7CTD7K2AV99KT47&refRID=633WK7CTD7K2AV99KT47&th=1) $23, 50x80mm
    * [KKmoon 35A](https://www.amazon.com/KKmoon-Battery-Protection-Integrated-Circuits/dp/B07X8M83QG/ref=pd_sbs_147_3/135-0325508-0159315?_encoding=UTF8&pd_rd_i=B07X8M83QG&pd_rd_r=1fa0928a-7c27-476a-94b5-405942232f00&pd_rd_w=I1XQs&pd_rd_wg=mtQ9m&pf_rd_p=12b8d3e2-e203-4b23-a8bc-68a7d2806477&pf_rd_r=633WK7CTD7K2AV99KT47&psc=1&refRID=633WK7CTD7K2AV99KT47) $17, 51x69mm
    * [Causin 30A](https://www.amazon.com/Rechargeable-Lithium-Liion-Battery-13S30A-Upgrade/dp/B082SCRWS4/ref=pd_sbs_23_3/135-0325508-0159315?_encoding=UTF8&pd_rd_i=B082SCRWS4&pd_rd_r=d352e308-f195-452c-a16e-cd4334971997&pd_rd_w=HW0ac&pd_rd_wg=MaLC8&pf_rd_p=12b8d3e2-e203-4b23-a8bc-68a7d2806477&pf_rd_r=GJJQ9H2G32AF5XH62A0Q&psc=1&refRID=GJJQ9H2G32AF5XH62A0Q) $18, 50x80mm
    * [Paialu 45A](https://www.amazon.com/Li-ion-Lipolymer-Battery-Protection-Balance/dp/B07PG2Z9RB/ref=sr_1_3?dchild=1&keywords=13s+bms&qid=1590955382&s=industrial&sr=1-3) $29 60x120mm
    * [DALY 100A, same as Daligreen](https://www.amazon.com/Current-Tricycle-Motorcycle-Inverter-Balance/dp/B087JF517P/ref=pd_sbs_23_4/135-0325508-0159315?_encoding=UTF8&pd_rd_i=B087JF517P&pd_rd_r=45191d64-6d30-426a-a086-afb56bfb9886&pd_rd_w=SWqn6&pd_rd_wg=j734x&pf_rd_p=12b8d3e2-e203-4b23-a8bc-68a7d2806477&pf_rd_r=QN1CTVYB33FDQGNJY5R8&psc=1&refRID=QN1CTVYB33FDQGNJY5R8) $68, 66x150mm
    * [DALY 50A](https://www.amazon.com/DALY-Battery-managment-Discharge-Electric/dp/B0876PW4MX/ref=sr_1_2?dchild=1&keywords=DALY+BMS+13S&qid=1590964740&sr=8-2) $28, 61x80mm
    * DALY 60A $34, 40A, $25, 25A $32
    * [AYMARIO 20A](https://www.amazon.com/Lithium-Battery-Protection-Function-Batteries/dp/B07NHHL3DY/ref=olp_product_details?ie=UTF8&me=&qid=1590965687&sr=1-1) $24, 49x66mm

  * [ebay](https://www.ebay.com/itm/US-35A-BMS-PCB-PCM-Protection-Board-With-Balance-For-E-bike-Li-ion-Battery-13S/133417323146?hash=item1f104aca8a:g:wQQAAOSwPuFex6gT) 35A (100) $16
  
### Battery Charger
---

For 13S you need a 54.6V charger. 
* [Amazon 54.6V 13S 6A](https://www.amazon.com/Battery-Charger-Lithium-90-230V-54-6V6A/dp/B07VSNBJR2) $78
* [Amazon 54.6 13S 4A](https://www.amazon.com/Charger-Electric-Battery-Scooter-Motorcycle/dp/B07P7GHY3L/ref=pd_di_sccai_4/144-1181655-6631115?_encoding=UTF8&pd_rd_i=B07PBVTZ67&pd_rd_r=5f27bd13-b8a6-4afa-abbd-3448ef7fb9a9&pd_rd_w=sPP9w&pd_rd_wg=ZrcAL&pf_rd_p=61ce50cf-2379-4458-9044-fa8b402c702d&pf_rd_r=C4FE2TY6P226K0SBY244&refRID=C4FE2TY6P226K0SBY244&th=1), $58
* [Aliexpress 13S 7A](https://www.aliexpress.com/item/32979899647.html?spm=a2g0o.productlist.0.0.3f8227049ZdB3B&algo_pvid=8450172b-cddf-46e0-a378-59c820ba1ac2&algo_expid=8450172b-cddf-46e0-a378-59c820ba1ac2-6&btsid=0ab6d67915909767797998084e7fea&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $47
* [Aliexpress 13S 4A](https://www.aliexpress.com/item/32870181959.html?spm=a2g0o.productlist.0.0.3f8227049ZdB3B&algo_pvid=8450172b-cddf-46e0-a378-59c820ba1ac2&algo_expid=8450172b-cddf-46e0-a378-59c820ba1ac2-17&btsid=0ab6d67915909767797998084e7fea&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $38
* [Aliexpress 12A](https://www.aliexpress.com/item/4000193014157.html?spm=a2g0o.productlist.0.0.3f8227049ZdB3B&algo_pvid=8450172b-cddf-46e0-a378-59c820ba1ac2&algo_expid=8450172b-cddf-46e0-a378-59c820ba1ac2-35&btsid=0ab6d67915909767797998084e7fea&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $206
* [Aliexpress T500 Ant Charger 8A](https://www.aliexpress.com/item/4000394843267.html?spm=a2g0o.productlist.0.0.3f8227049ZdB3B&algo_pvid=413d0752-30c6-491e-ae1d-11a9a16fa37b&algo_expid=413d0752-30c6-491e-ae1d-11a9a16fa37b-10&btsid=0ab6f83a15909774883345344e3191&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) $65 **
* [Aliexpress 10A](https://www.aliexpress.com/item/32986399986.html?spm=a2g0o.detail.1000014.1.936639d8NgGimi&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.14976.158757.0&scm_id=1007.14976.158757.0&scm-url=1007.14976.158757.0&pvid=e15aeea8-2e4e-4509-924a-1278e487b3e6&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.14976.158757.0,pvid:e15aeea8-2e4e-4509-924a-1278e487b3e6,tpp_buckets:668%230%23131923%234_668%23808%234093%23864_668%23888%233325%2312_4976%230%23158757%230_4976%232711%237538%23261_668%232846%238111%23436_668%232717%237559%2337) $85

### Remote Control
---
* http://www.diyeboard.com/ RC7 2.4Ghz $20
* http://www.diyeboard.com/ RC with receiver $39
* Enertion Nano-X, http://www.enertionboards.com/
* Miami Electric Boards Remote 278 (Benchwheel)
* Benchwheel.com Remote & Receiver 2.4 GHz $54
* [DIYeboard](https://diyelectricskateboard.com/collections/remote-controller) $46
* Same boards are available at [AliExress 1](https://www.aliexpress.com/item/4000241274377.html?spm=a2g0o.cart.0.0.5aeb3c00myg8ZA&mp=1), [AliExpress 2](https://www.aliexpress.com/item/32678995218.html?spm=a2g0o.cart.0.0.153c3c00tRosU8&mp=1)

## Deck
https://www.roarockit.com/skateboard-building/
Bamboo 10.5x46 1/16 best elasticity, fragile until laminated
Mable 12x47 1/16 denser and strong
Birch 12x47 1/16 light and flexible
7-9 layers

https://www.woodcraft.com/products/rock-hard-maple-skatebaord-veneers-longboard-style-12-x-48-7-mmply7.7inches
Maple 12x48

Canadian Hard Maple

10mill = 1/100inch

Polycarb
1/16 24x48
1/8 24x48 $24
1/8 12x24
Temp Melt 280-320, Form 30-80

Foamboard 3mm
12x12 Expanded PVC
170-190 30-60

Polypropylene 
200-280 30-80

Polystyrene Foam (white packaging block)
170-280 30-60

PVD Shring Tubing  
length 3x65mm = 195mm 7.7inches pluse side 20+20= 240mm  

Battery  
length 3x65mm = 195mm 7.7" pluse side 20+20= 240mm  
width 6x18mm = 108mm 4.25 inches plus side 20 = 130mm  
height total = 9"  
length total 4x108 + 65 + BMS + Odrive 2"  = 26"  
  
150mm shrink tubing clear PVC  

Neoperene Rubber Sheets  
1/16 1'x12'
