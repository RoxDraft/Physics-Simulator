#!/usr/bin/env python3
"""Generate the Sources page (src/<sim>/Sources.dc.html) for every simulator.

Each source is listed in one of three groups:
  open        openly available, free to read and reuse
  restricted  exists, but needs registration, payment, or is limited to some organisations
  none        not published anywhere we could use, so the simulator uses an estimate
Every entry says which part of the simulator uses it.

Usage: python3 tools/gen_sources.py   (tools/build.sh runs it)
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def S(title, used, access, url=""):
    return {"title": title, "used": used, "access": access, "url": url}


SIMS = {
    "ocean-waves": {
        "eyebrow": "OCEAN WAVE SIMULATOR · แหล่งข้อมูล",
        "back": ("Main.dc.html", "← กลับไปที่ตัวจำลองคลื่น"),
        "intro": "ตัวจำลองคลื่นใช้ทฤษฎีคลื่นเชิงเส้นที่เป็นมาตรฐานทางวิศวกรรมชายฝั่ง ส่วนตัวอย่างการใช้ประโยชน์อ้างอิงจากหน่วยงานและโครงการจริง ภาพเคลื่อนไหวเป็นการจำลองหลักการ ไม่ใช่ข้อมูลจากอุปกรณ์จริง",
        "open": [
            S("Coastal Engineering Manual (EM 1110-2-1100), US Army Corps of Engineers", "สมการ dispersion ความเร็วคลื่น คาบ ความเร็วกลุ่ม กำลังคลื่น และเกณฑ์คลื่นแตก", "เอกสารรัฐบาลสหรัฐฯ เป็นสาธารณสมบัติ ดาวน์โหลดได้ฟรี", "https://www.publications.usace.army.mil/"),
            S("OpenStax University Physics Volume 1 บทที่ 16 คลื่น", "พื้นฐานคลื่น ความยาวคลื่น คาบ และพลังงาน", "ตำราเปิด สัญญาอนุญาต CC BY 4.0", "https://openstax.org/books/university-physics-volume-1/pages/16-introduction"),
            S("NOAA National Data Buoy Center และ DART", "การทำงานของทุ่นเตือนภัยสึนามิ และข้อมูลคลื่นจริงจากทุ่น", "ข้อมูลเปิด ใช้ได้ฟรี", "https://www.ndbc.noaa.gov/"),
            S("European Marine Energy Centre (EMEC)", "หลักการของเครื่องแปลงพลังงานคลื่นทั้ง 4 แบบ", "ข้อมูลทั่วไปเปิดให้อ่านบนเว็บไซต์", "https://www.emec.org.uk/"),
            S("Ocean Energy Systems (IEA Technology Collaboration Programme)", "สถานะเทคโนโลยีพลังงานคลื่นและโครงการต้นแบบ", "รายงานส่วนใหญ่ดาวน์โหลดได้ฟรี", "https://www.ocean-energy-systems.org/"),
            S("กรมอุทกศาสตร์ กองทัพเรือ", "ลักษณะน้ำขึ้นน้ำลงในอ่าวไทย", "ตารางน้ำขึ้นน้ำลงเผยแพร่ต่อสาธารณะ", "https://www.hydro.navy.mi.th/"),
            S("กรมป้องกันและบรรเทาสาธารณภัย", "ระบบเตือนภัยสึนามิและหอเตือนภัยตามแนวชายฝั่งอันดามัน", "ข้อมูลเปิดบนเว็บไซต์หน่วยงาน", "https://www.disaster.go.th/"),
            S("Polynesian Voyaging Society", "การอ่านสเวลล์เพื่อนำทางแบบโพลินีเซีย", "ข้อมูลเปิดบนเว็บไซต์", "https://www.hokulea.com/"),
        ],
        "restricted": [
            S("Gunn, K. & Stock-Williams, C. (2012). Quantifying the global wave power resource. Renewable Energy 44", "ตัวเลขศักยภาพพลังงานคลื่นทั่วโลกราว 2 เทราวัตต์", "บทความวารสาร ต้องสมัครสมาชิกหรือซื้อบทความ"),
            S("Dean, R. G. & Dalrymple, R. A. Water Wave Mechanics for Engineers and Scientists", "ตำราอ้างอิงทฤษฎีคลื่นเชิงเส้นและคลื่นแตก", "หนังสือ ต้องซื้อหรือยืมจากห้องสมุด"),
            S("ข้อมูลการทดสอบในทะเลของเครื่องแปลงพลังงานคลื่นแต่ละบริษัท", "ประสิทธิภาพจริงของอุปกรณ์", "ส่วนใหญ่เป็นข้อมูลภายในบริษัท เปิดเผยเพียงบางส่วนในรายงานโครงการ"),
        ],
        "none": [
            S("การเคลื่อนไหวในภาพตัวอย่างการใช้ประโยชน์ 8 แบบ และเครื่องแปลงพลังงาน 4 แบบ", "ความเร็ว ระยะ จังหวะ และการหน่วงเวลาในภาพ", "ใช้ค่าและสัดส่วนสมมติเพื่อแสดงหลักการ ไม่ตามสเกลจริง"),
            S("ค่าเริ่มต้นของคลื่นแต่ละชนิด", "ความสูง ความยาว และความลึกเริ่มต้นของคลื่นลม สเวลล์ คลื่นเข้าฝั่ง สึนามิ และน้ำขึ้นน้ำลง", "เป็นค่าตัวอย่างทั่วไป ไม่ใช่การวัดจากเหตุการณ์ใดเหตุการณ์หนึ่ง"),
            S("ภาพหน้าตัดคลื่นในตัวจำลอง", "ความสูงคลื่นที่วาด และความเร็วของภาพเคลื่อนไหว", "ขยายความสูง 4 เท่าและปรับความเร็วให้มองเห็นง่าย ตัวเลขในช่องผลลัพธ์คำนวณจากค่าจริง"),
            S("สูตรกำลังคลื่นแบบคร่าว ๆ P ≈ 0.5 H² T", "ช่องคำนวณพลังงานคลื่น", "สูตรจริงใช้ความสูงคลื่นนัยสำคัญ (Hs) และคาบพลังงาน (Te) ของทะเลจริงที่มีคลื่นหลายขนาด หน้านี้ใช้คลื่นลูกเดียวเพื่อความง่าย"),
        ],
    },
    "camera-lab": {
        "eyebrow": "CAMERA LAB · แหล่งข้อมูล",
        "back": ("Main.dc.html", "← กลับไปที่ห้องแล็บกล้อง"),
        "intro": "ห้องแล็บกล้องใช้หลักทัศนศาสตร์และฟิสิกส์ของเซนเซอร์ที่เปิดเผยในตำราและมาตรฐาน แต่รายละเอียดของอุปกรณ์จริง เช่น อัลกอริทึมของแต่ละแบรนด์ ส่วนใหญ่ไม่เปิดเผย หน้านี้บอกว่าตัวเลขใดมาจากแหล่งใด และตัวเลขใดเป็นค่าประมาณของเรา",
        "open": [
            S("OpenStax University Physics Volume 3 บทที่ 2 ทัศนศาสตร์เชิงเรขาคณิต", "สมการเลนส์บาง กำลังขยาย กล้องจุลทรรศน์ และกล้องโทรทรรศน์", "ตำราเปิด สัญญาอนุญาต CC BY 4.0", "https://openstax.org/books/university-physics-volume-3/pages/2-introduction"),
            S("EMVA 1288 มาตรฐานการวัดคุณภาพกล้องและเซนเซอร์", "แบบจำลองนอยส์โฟตอน SNR ความจุพิกเซล และกระแสมืด", "มาตรฐานเปิด ดาวน์โหลดได้ฟรี", "https://www.emva.org/standards-technology/emva-1288/"),
            S("สิทธิบัตรสหรัฐฯ 3,971,065 (Bayer, 1976)", "ฟิลเตอร์สีแบบ Bayer ในขั้นตอน ISP", "สิทธิบัตรเผยแพร่ต่อสาธารณะ", "https://patents.google.com/patent/US3971065A"),
            S("ITU-T H.265 (HEVC) รวมส่วนขยายหลายมุมมอง MV-HEVC", "การเก็บวิดีโอ Spatial สองมุมในไฟล์เดียว", "ดาวน์โหลดเอกสารมาตรฐานได้ฟรีจาก ITU", "https://www.itu.int/rec/T-REC-H.265"),
            S("Apple Developer Documentation", "หลักการบันทึกภาพและวิดีโอ Spatial ด้วยกล้องสองตัว", "เอกสารสำหรับนักพัฒนาเปิดให้อ่าน แต่ไม่รวมรายละเอียดภายในของ ISP", "https://developer.apple.com/documentation/"),
            S("OpenCV Documentation: camera calibration และ stereo", "การจัดแนวภาพ (rectification) และการหาความลึกจาก disparity", "ซอฟต์แวร์และเอกสารเปิด สัญญาอนุญาต Apache 2.0", "https://docs.opencv.org/"),
            S("NASA Mars 2020 Perseverance", "กล้องนำทางและกล้องหลบอันตรายแบบคู่ของยานสำรวจ", "ข้อมูลเปิด", "https://science.nasa.gov/mission/mars-2020-perseverance/"),
            S("Alduchov, O. A. & Eskridge, R. E. (1996). Journal of Applied Meteorology", "สูตร Magnus สำหรับคำนวณจุดน้ำค้างและการเกิดฝ้าบนเลนส์", "บทความเปิดให้อ่านบนเว็บไซต์ของ American Meteorological Society", "https://journals.ametsoc.org/"),
            S("NASA Electronic Parts and Packaging Program (NEPP)", "ผลของรังสีต่อเซนเซอร์และอุปกรณ์อิเล็กทรอนิกส์ในอวกาศ", "รายงานส่วนใหญ่เปิดให้อ่าน", "https://nepp.nasa.gov/"),
            S("Image sensor format (Wikipedia)", "ขนาดเซนเซอร์มาตรฐาน เช่น 1/1.3″, 1 นิ้ว, APS-C, ฟูลเฟรม", "สารานุกรมเปิด CC BY-SA ควรตรวจกับแหล่งต้นทางที่อ้างในบทความ", "https://en.wikipedia.org/wiki/Image_sensor_format"),
        ],
        "restricted": [
            S("ISO 2720 และ ISO 12232", "ค่าคงที่ของเครื่องวัดแสง (K = 12.5) และนิยามความไวแสง ISO", "มาตรฐาน ISO ต้องซื้อเอกสาร", "https://www.iso.org/"),
            S("Hecht, E. Optics และ Hartley, R. & Zisserman, A. Multiple View Geometry", "ตำราอ้างอิงทัศนศาสตร์และการมองเห็นสามมิติ", "หนังสือ ต้องซื้อหรือยืมจากห้องสมุด"),
            S("เอกสารข้อมูลจำเพาะ (datasheet) ของเซนเซอร์จากผู้ผลิต", "ขนาดพิกเซล ความจุพิกเซล นอยส์จากวงจรอ่าน", "มักให้เฉพาะลูกค้าที่ลงนามสัญญารักษาความลับ (NDA)"),
            S("แก้วทนรังสีผสมซีเรียมของผู้ผลิตแก้ว เช่น SCHOTT", "การที่แก้วธรรมดาเป็นสีน้ำตาลเมื่อโดนรังสี", "มีข้อมูลทั่วไปบนเว็บไซต์ ค่าทดสอบละเอียดต้องขอจากผู้ผลิต", "https://www.schott.com/"),
        ],
        "none": [
            S("อัลกอริทึม ISP ของแต่ละแบรนด์ (ลดนอยส์ HDR การใช้ AI)", "ขั้นตอน ISP 7 ขั้นในการทดลอง 03", "ไม่เปิดเผย หน้านี้ใช้ขั้นตอนทั่วไปแบบง่าย"),
            S("สเปกเลนส์และเซนเซอร์ของโทรศัพท์แต่ละรุ่น", "ทางยาวโฟกัสจริง 6.9 มม. เส้นทแยงเซนเซอร์ 12.4 มม. ความละเอียด 48/12 ล้านพิกเซล", "ผู้ผลิตเปิดเผยไม่ครบ ใช้ค่าตัวอย่างที่ใกล้เคียงของจริง ไม่ใช่สเปกรุ่นใด"),
            S("ลูปควบคุมกันสั่นของผู้ผลิต", "OIS ชดเชย 92% ขยับได้สูงสุด 18 px และ EIS ครอป 10% ต่อด้าน", "ไม่เปิดเผย ใช้แบบจำลองสมมติ"),
            S("ระยะห่างเลนส์คู่ของมือถือ รถยนต์ และยานสำรวจ", "ค่า B ในการทดลอง 04", "ใช้ค่าประมาณเพื่อเปรียบเทียบ ไม่ใช่สเปกรุ่นใด"),
            S("อัตราความเสียหายจากรังสีและการลดลงของแสงผ่านเลนส์", "พิกเซลเสียสะสมและเปอร์เซ็นต์แสงผ่านในการทดลอง 06", "เป็นตัวเลขสมมติเพื่อแสดงแนวโน้ม ของจริงขึ้นกับวงโคจรและกิจกรรมของดวงอาทิตย์"),
            S("ค่าสัมประสิทธิ์โฟกัสเลื่อนตามอุณหภูมิ", "โฟกัสเลื่อนของเลนส์พลาสติก แก้ว และแบบ athermal", "ใช้ค่าตัวแทนแบบง่าย เลนส์จริงแต่ละรุ่นต่างกัน"),
        ],
    },
    "plate-tectonics": {
        "eyebrow": "PLATE TECTONICS LAB · แหล่งข้อมูล",
        "back": ("Main.dc.html", "← กลับไปที่แผนที่และสถิติ"),
        "intro": "แผนที่และกราฟคำนวณจากข้อมูลเปิดของ USGS, Smithsonian และ Natural Earth ด้วยสคริปต์ในโฟลเดอร์ data/plate-tectonics ของ repo ข้อมูลความสูญเสียบางชุดจำกัดการเข้าถึง และบางค่าในตัวจำลองเป็นค่าประมาณเพื่อการเรียนรู้",
        "open": [
            S("USGS ANSS Comprehensive Earthquake Catalog (ComCat)", "แผ่นดินไหว M 5.5 ขึ้นไป ปี 1965–2016 จำนวน 23,412 เหตุการณ์ บนแผนที่และในกราฟรายประเทศ (ใช้สำเนา earthquakes-23k.csv จาก github.com/plotly/datasets)", "ข้อมูลรัฐบาลสหรัฐฯ เป็นสาธารณสมบัติ", "https://earthquake.usgs.gov/earthquakes/search/"),
            S("Smithsonian Institution Global Volcanism Program", "ภูเขาไฟยุคโฮโลซีน 1,571 ลูก และภูเขาไฟที่ปะทุตั้งแต่ปี 1964 (ใช้สำเนา volcano_db.csv จาก github.com/plotly/datasets ซึ่งเป็นรายชื่อรุ่นเก่า ฐานข้อมูลปัจจุบันมีรายละเอียดมากกว่า)", "ใช้ได้ฟรีโดยอ้างอิงแหล่งที่มา", "https://volcano.si.edu/"),
            S("Bird, P. (2003). An updated digital model of plate boundaries (PB2002)", "เส้นรอยต่อแผ่นเปลือกโลกและเขตมุดตัวบนแผนที่ (GeoJSON โดย Hugo Ahlenius)", "สัญญาอนุญาต Open Data Commons Attribution", "https://github.com/fraxen/tectonicplates"),
            S("Natural Earth", "รูปร่างแผ่นดินและพรมแดนประเทศ ใช้ผ่านแพ็กเกจ world-atlas", "สาธารณสมบัติ", "https://www.naturalearthdata.com/"),
            S("USGS Earthquake Hazards Program: Lists, Maps, and Statistics", "จำนวนแผ่นดินไหวเฉลี่ยต่อปี และตารางเปรียบเทียบขนาดกับความรุนแรงเมอร์คัลลี", "สาธารณสมบัติ", "https://www.usgs.gov/programs/earthquake-hazards/lists-maps-and-statistics"),
            S("NOAA NCEI Natural Hazards Data", "จำนวนผู้เสียชีวิตโดยประมาณของเหตุการณ์ในอดีต", "ข้อมูลเปิด", "https://www.ncei.noaa.gov/products/natural-hazards"),
            S("ราชกิจจานุเบกษา", "กฎกระทรวงว่าด้วยการต้านทานแรงสั่นสะเทือนของแผ่นดินไหว พ.ศ. 2564", "เปิดให้อ่านฟรี", "https://ratchakitcha.soc.go.th/"),
            S("กรมโยธาธิการและผังเมือง", "มาตรฐาน มยผ. 1301/1302-61 การออกแบบอาคารต้านทานการสั่นสะเทือนของแผ่นดินไหว", "ดาวน์โหลดได้จากหน่วยงาน", "https://www.dpt.go.th/"),
            S("กรมอุตุนิยมวิทยา ศูนย์เฝ้าระวังแผ่นดินไหว", "แผ่นดินไหวในไทย เช่น แม่ลาว เชียงราย 2557", "ข้อมูลเปิดบนเว็บไซต์", "https://earthquake.tmd.go.th/"),
            S("Earthquake Country Alliance และ Ready.gov", "หลัก “หมอบ ป้อง เกาะ” และการเตรียมตัวก่อนเกิดแผ่นดินไหว", "ข้อมูลเปิด", "https://www.earthquakecountry.org/dropcoverholdon/"),
            S("ShakeAlert (USGS) และหน่วยงานอุตุนิยมวิทยาญี่ปุ่น (JMA)", "หลักการเตือนภัยแผ่นดินไหวล่วงหน้า", "ข้อมูลเปิด", "https://www.shakealert.org/"),
            S("EarthScope Consortium (เดิม IRIS และ UNAVCO)", "เครือข่ายเครื่องวัดแผ่นดินไหวและสถานี GNSS", "ข้อมูลส่วนใหญ่เปิดให้ดาวน์โหลด", "https://www.earthscope.org/"),
            S("Copernicus Data Space (Sentinel-1, Sentinel-2, Sentinel-5P)", "ภาพเรดาร์ InSAR ภาพถ่ายเชิงแสง และข้อมูลก๊าซภูเขาไฟ", "ข้อมูลเปิด ใช้ได้ฟรี", "https://dataspace.copernicus.eu/"),
            S("NISAR (NASA–ISRO) และ GRACE-FO", "เรดาร์ติดตามการเคลื่อนตัวของพื้นผิว และการเปลี่ยนแปลงแรงโน้มถ่วง", "นโยบายเปิดข้อมูล", "https://nisar.jpl.nasa.gov/"),
            S("Eos (AGU): Magnitude 8.8 earthquake strikes western Pacific", "แผ่นดินไหวคัมชัตคา กรกฎาคม 2568", "บทความข่าววิทยาศาสตร์ อ่านได้ฟรี", "https://eos.org/research-and-developments/magnitude-8-8-earthquake-strikes-western-pacific"),
            S("Yeni Şafak และ Izvestia (รายงานข่าว)", "ผู้เสียชีวิตในเมียนมามากกว่า 3,700 คน และอย่างน้อย 86 คนที่ตึกถล่มในกรุงเทพฯ (รายงาน พ.ค. 2568)", "ข่าวเปิดให้อ่าน ตัวเลขอาจปรับภายหลัง ควรตรวจกับรายงานทางการล่าสุด", "https://iz.ru/en/1881049/2025-05-04/bangkok-death-toll-collapse-building-due-earthquake-has-increased-86"),
        ],
        "restricted": [
            S("EM-DAT ฐานข้อมูลภัยพิบัติระหว่างประเทศ (CRED, UCLouvain)", "สถิติผู้เสียชีวิตและความเสียหายรายประเทศ ซึ่งเป็นแหล่งที่ใช้กันมากที่สุด", "ต้องลงทะเบียน ใช้ฟรีเฉพาะงานไม่แสวงกำไร ห้ามเผยแพร่ข้อมูลดิบต่อ งานเชิงพาณิชย์ต้องซื้อสิทธิ์ เราจึงไม่ได้ใส่ข้อมูลชุดนี้ในหน้า", "https://doc.emdat.be/docs/legal/terms-of-use/"),
            S("ข้อมูลสถานีตรวจวัดของ CTBTO (International Monitoring System)", "คลื่นไหวสะเทือนและคลื่นเสียงความถี่ต่ำจากทั่วโลก", "เฉพาะรัฐภาคีและนักวิจัยที่ได้รับอนุญาต", "https://www.ctbto.org/"),
            S("มาตรฐานอาคารต่างประเทศ: ASCE 7, Eurocode 8, NZS 1170.5, NCh433 และอื่น ๆ", "ตารางมาตรฐานอาคารในหน้าการรับมือ", "ส่วนใหญ่ต้องซื้อเอกสารมาตรฐาน เราสรุปเฉพาะข้อมูลทั่วไปที่เผยแพร่"),
            S("NIED ญี่ปุ่น: K-NET, KiK-net, S-net", "ข้อมูลความเร่งแรงสั่นและเครือข่ายเคเบิลใต้ทะเล", "ต้องลงทะเบียนก่อนดาวน์โหลด", "https://www.bosai.go.jp/e/"),
            S("ภาพถ่ายดาวเทียมความละเอียดสูงเชิงพาณิชย์", "การประเมินความเสียหายรายอาคารหลังภัยพิบัติ", "ต้องซื้อจากบริษัทผู้ให้บริการ หน่วยงานภัยพิบัติขอใช้ผ่าน International Charter ได้", "https://disasterscharter.org/"),
            S("แบบจำลองความเสี่ยงภัยพิบัติเชิงพาณิชย์ของบริษัทประกันภัย", "การประเมินความเสียหายทางเศรษฐกิจล่วงหน้า", "เป็นทรัพย์สินทางปัญญาของบริษัท ไม่เปิดเผย"),
            S("Wells, D. L. & Coppersmith, K. J. (1994). Bulletin of the Seismological Society of America", "สูตรความยาวรอยแตกโดยประมาณจากขนาดแผ่นดินไหว", "บทความวารสาร อาจต้องสมัครสมาชิก"),
        ],
        "none": [
            S("การนับแผ่นดินไหวรายประเทศ", "กราฟสถิติรายประเทศ", "วิธีของเราเอง: นับตามประเทศที่จุดศูนย์กลางอยู่ภายใน หรือมีแผ่นดินห่างไม่เกิน 300 กม. ไม่ใช่สถิติทางการของประเทศใด"),
            S("แผ่นดินไหวหลังปี 2016 บนแผนที่", "จุดแผ่นดินไหวบนแผนที่", "ชุดข้อมูลที่ใช้สิ้นสุดปี 2016 เหตุการณ์หลังจากนั้นเพิ่มเฉพาะเหตุการณ์สำคัญด้วยมือ"),
            S("จำนวนผู้เสียชีวิตบางเหตุการณ์", "การ์ดเหตุการณ์สำคัญ", "ยังไม่มีตัวเลขที่ตรงกัน เช่น เฮติ 2010 วัลดิเวีย 1960 และตัมโบรา 1815 เราจึงแสดงเป็นช่วงหรือค่าประมาณ"),
            S("คาบการสั่นของดินและอาคาร", "ตัวจำลองการสั่นพ้อง: ดิน 0.3 / 0.7 / 1.5 วินาที และกฎ 0.1 วินาทีต่อชั้น", "เป็นค่าตัวอย่างเพื่อการเรียนรู้ ข้อมูลโครงสร้างและผลตรวจสอบของอาคารรายหลังโดยทั่วไปไม่เปิดเผยต่อสาธารณะ"),
            S("เวลาประมวลผลของระบบเตือนภัย", "ตัวจำลองเวลาเตือนภัยล่วงหน้า: สถานีห่าง 10 กม. ประมวลผล 4 วินาที", "เป็นค่าสมมติ ระบบจริงแต่ละประเทศต่างกันและไม่เปิดเผยรายละเอียดทั้งหมด"),
            S("ความเร็วคลื่น P และ S", "การหาจุดศูนย์กลาง: 6.0 และ 3.5 กม./วินาที", "เป็นค่าเฉลี่ยในเปลือกโลก ความเร็วจริงเปลี่ยนตามชนิดหินและความลึก"),
            S("ข้อมูลดิบจากเซนเซอร์ในโทรศัพท์มือถือ", "การ์ดเซนเซอร์ในหน้าการรับมือ", "ไม่เปิดเผย ผู้ให้บริการเก็บเป็นข้อมูลภายใน"),
            S("ความเร็วแผ่นเปลือกโลกและสเกลเวลาในภาพเคลื่อนไหว", "หน้าฟิสิกส์ของแผ่นดินไหว", "ใช้ช่วงค่าทั่วไป 1–15 ซม./ปี ไม่ใช่การวัดของรอยต่อใดรอยต่อหนึ่ง"),
        ],
    },
    "mechanics-lab": {
        "eyebrow": "MECHANICS LAB · แหล่งข้อมูล",
        "back": ("Main.dc.html", "← กลับไปที่แล็บกลศาสตร์"),
        "intro": "แล็บกลศาสตร์ใช้หลักโมเมนต์ แรงสู่ศูนย์กลาง และหลักอาร์คิมิดีสจากตำราฟิสิกส์ 1 เกณฑ์ความปลอดภัยมาจากมาตรฐานจริง แต่ขนาดและน้ำหนักของรถแบ็คโฮและเรือเป็นค่าตัวอย่างที่ทำให้ง่ายขึ้น",
        "open": [
            S("OpenStax University Physics Volume 1 บทที่ 10 และ 12: การหมุนและสมดุลสถิต", "โมเมนต์ของแรง จุดพลิกคว่ำ และแรงสู่ศูนย์กลาง F = mω²r", "ตำราเปิด สัญญาอนุญาต CC BY 4.0", "https://openstax.org/books/university-physics-volume-1/pages/10-introduction"),
            S("OpenStax University Physics Volume 1 บทที่ 14: กลศาสตร์ของไหล", "แรงลอยตัว ปริมาตรน้ำที่ถูกแทนที่ และความหนาแน่นน้ำทะเลกับน้ำจืด", "ตำราเปิด สัญญาอนุญาต CC BY 4.0", "https://openstax.org/books/university-physics-volume-1/pages/14-introduction"),
            S("PhET Interactive Simulations: Buoyancy และ Balancing Act", "แนวคิดการทดลองซ้ำแบบปรับค่าได้ ซึ่งเป็นต้นแบบของแล็บนี้", "ใช้ได้ฟรี สัญญาอนุญาต CC BY 4.0", "https://phet.colorado.edu/"),
            S("OSHA Cranes and Derricks in Construction (29 CFR 1926 Subpart CC)", "หลักการไม่ยกเกินพิกัดและการใช้ตารางพิกัดยก", "เอกสารรัฐบาลสหรัฐฯ อ่านได้ฟรี", "https://www.osha.gov/cranes-derricks"),
        ],
        "restricted": [
            S("ISO 10567 Earth-moving machinery: Hydraulic excavators, lift capacity", "พิกัดยก = 75% ของน้ำหนักที่ทำให้รถพลิก (หรือ 87% ของแรงไฮดรอลิก)", "มาตรฐาน ISO ต้องซื้อ เราใช้เฉพาะหลักการที่ผู้ผลิตอ้างถึงในคู่มือ"),
            S("IMO International Code on Intact Stability (2008 IS Code)", "เกณฑ์ GM ขั้นต่ำ 0.15 ม. สำหรับเรือ", "เอกสาร IMO ต้องซื้อ เกณฑ์นี้ถูกอ้างถึงในตำราสถาปัตยกรรมเรือทั่วไป"),
            S("ตารางพิกัดยกและสเปกจริงของผู้ผลิตรถขุด", "เปรียบเทียบค่าที่คำนวณกับเครื่องจริงขนาด 20 ตัน", "เผยแพร่บางส่วนในโบรชัวร์ ตารางเต็มอยู่ในคู่มือผู้ใช้ของแต่ละรุ่น"),
            S("แผนการบรรทุกและข้อมูลเสถียรภาพของเรือแต่ละลำ (stability booklet)", "การจัดตู้สินค้าและน้ำอับเฉาจริง", "เป็นเอกสารของเจ้าของเรือ ไม่เผยแพร่ต่อสาธารณะ"),
        ],
        "none": [
            S("มวลและตำแหน่งชิ้นส่วนของรถแบ็คโฮ", "ตัวรถ 16.5 ตัน บูม 1.7 ตัน แขน 0.9 ตัน บุ้งกี๋ 0.7 ตัน ความยาวบูม 5.7 ม. แขน 2.9 ม.", "เป็นค่าประมาณของรถขุดขนาด 20 ตันทั่วไป ไม่ใช่รุ่นใดรุ่นหนึ่ง"),
            S("กระบอกไฮดรอลิก", "เส้นผ่านศูนย์กลาง 14 ซม. แขนโมเมนต์ 0.9 ม. และเกณฑ์เตือน 35 MPa", "ค่าสมมติเพื่อแสดงความสัมพันธ์ระหว่างโมเมนต์กับแรงดัน"),
            S("รูปทรงเรือเป็นกล่องสี่เหลี่ยม", "เรือยาว 250 ม. กว้าง 40 ม. ลึก 22 ม. น้ำหนักเรือเปล่า 30,000 ตัน", "ตัวเรือจริงมีรูปทรงโค้ง สูตร KB และ BM จึงต่างจากค่าจริง ใช้เพื่อเห็นหลักการเท่านั้น"),
            S("แรงลมบนตู้สินค้า", "มุมเอียงจากลม", "ใช้สัมประสิทธิ์แรงต้านและพื้นที่รับลมแบบง่าย ไม่รวมคลื่นและการเคลื่อนที่ของเรือ"),
        ],
    },
    "beam-fea": {
        "eyebrow": "BEAM FEA · แหล่งข้อมูล",
        "back": ("Main.dc.html", "← กลับไปที่ FEA คาน"),
        "intro": "หน้า FEA ใช้วิธีไฟไนต์เอลิเมนต์แบบคานออยเลอร์-แบร์นูลลี ซึ่งเป็นเนื้อหามาตรฐานของวิชากลศาสตร์วัสดุและการวิเคราะห์โครงสร้าง ผลตรวจสอบเทียบกับสูตรในตำราแล้ว แต่ไม่ใช่การออกแบบตามมาตรฐานจริง ซึ่งต้องทำโดยวิศวกรโยธาที่มีใบอนุญาต",
        "open": [
            S("MIT OpenCourseWare 2.001 Mechanics & Materials I", "ความเค้นดัด σ = My/I แรงเฉือน และการโก่งตัวของคาน", "เนื้อหาเปิด สัญญาอนุญาต CC BY-NC-SA", "https://ocw.mit.edu/courses/2-001-mechanics-materials-i-fall-2006/"),
            S("AISC 360 Specification for Structural Steel Buildings", "หน้าตัดเหล็กรูปตัว I และกำลังครากของเหล็ก", "ดาวน์โหลดได้ฟรีจาก AISC", "https://www.aisc.org/publications/steel-standards/"),
            S("กรมโยธาธิการและผังเมือง: กฎกระทรวงและมาตรฐานการออกแบบอาคาร (มยผ.)", "น้ำหนักบรรทุกจรของที่พักอาศัย ระเบียง และอาคารอุตสาหกรรม", "กฎหมายและมาตรฐานเผยแพร่บนเว็บไซต์หน่วยงาน", "https://www.dpt.go.th/"),
            S("Wikipedia: Euler–Bernoulli beam theory และ Von Mises yield criterion", "สูตรตรวจสอบผลวิเคราะห์ และความเค้นฟอนมิเซส √(σ² + 3τ²)", "เปิด สัญญาอนุญาต CC BY-SA", "https://en.wikipedia.org/wiki/Euler%E2%80%93Bernoulli_beam_theory"),
        ],
        "restricted": [
            S("Logan, D. L. A First Course in the Finite Element Method", "เมทริกซ์ความแข็งของเอลิเมนต์คาน และแรงที่โหนดจากน้ำหนักแผ่", "หนังสือ ต้องซื้อหรือยืมจากห้องสมุด"),
            S("ACI 318 และมาตรฐาน วสท. สำหรับคอนกรีตเสริมเหล็ก", "การออกแบบคานคอนกรีตจริง ซึ่งต้องคิดเหล็กเสริมและการแตกร้าว", "มาตรฐานต้องซื้อ หน้านี้ไม่ได้ใช้วิธีออกแบบตามมาตรฐานนี้"),
            S("ASCE 7 Minimum Design Loads", "หลักการรวมน้ำหนักบรรทุกคงที่และน้ำหนักบรรทุกจร", "มาตรฐานต้องซื้อ"),
            S("ซอฟต์แวร์ FEA เชิงพาณิชย์ เช่น ANSYS, Abaqus, SAP2000", "รูปแบบการแสดงสีความเค้นที่หน้านี้เลียนแบบ", "ต้องซื้อลิขสิทธิ์ มีรุ่นสำหรับนักศึกษาบางรุ่น"),
        ],
        "none": [
            S("คุณสมบัติวัสดุแบบง่าย", "เหล็ก E 200 GPa กำลัง 275 MPa ไม้ E 11 GPa กำลัง 24 MPa คอนกรีต E 30 GPa ความเค้นยอมให้ 13.5 MPa", "ค่าตัวอย่างทั่วไป วัสดุจริงต่างกันตามเกรด และคอนกรีตเสริมเหล็กไม่ได้ทำงานเหมือนวัสดุเนื้อเดียว"),
            S("สัดส่วนหน้าตัด", "ความกว้างคาน ความหนาปีกและเอวของเหล็กรูปตัว I คิดเป็นสัดส่วนของความลึก", "ค่าสมมติ ไม่ใช่หน้าตัดมาตรฐานรุ่นใด"),
            S("น้ำหนักบรรทุกในตัวอย่าง", "คอนโด เครนโรงงาน ระเบียง หลังคา และสะพานไม้", "ค่าตัวอย่างเพื่อการเรียนรู้ ไม่ได้มาจากแบบอาคารจริง"),
            S("เกณฑ์ความปลอดภัย", "ส่วนเผื่อความปลอดภัย 1.5 และการโก่งตัว L/360 (คานยื่น L/180)", "เป็นเกณฑ์ที่ใช้ทั่วไปแบบง่าย มาตรฐานจริงใช้ตัวคูณน้ำหนักและตัวลดกำลังแยกกัน"),
        ],
    },
    "circuit-lab": {
        "eyebrow": "CIRCUIT LAB · แหล่งข้อมูล",
        "back": ("Main.dc.html", "← กลับไปที่แล็บวงจรไฟฟ้า"),
        "intro": "แล็บวงจรใช้กฎของโอห์ม กฎของเคอร์ชอฟฟ์ และวงจร RC จากตำราฟิสิกส์ 2 ส่วนตู้ไฟในบ้านอ้างอิงหลักการของมาตรฐานการติดตั้งไฟฟ้า แต่ตัวเลขถูกทำให้ง่ายขึ้น งานไฟฟ้าจริงต้องทำโดยช่างที่มีใบอนุญาต",
        "open": [
            S("OpenStax University Physics Volume 2 บทที่ 9–10: กระแสไฟฟ้าและวงจรไฟฟ้ากระแสตรง", "กฎของโอห์ม วงจรอนุกรมและขนาน กำลังไฟฟ้า และวงจร RC", "ตำราเปิด สัญญาอนุญาต CC BY 4.0", "https://openstax.org/books/university-physics-volume-2/pages/10-introduction"),
            S("Falstad Circuit Simulator", "แนวคิดการแสดงกระแสเป็นจุดที่วิ่งตามสาย", "ใช้ได้ฟรีบนเว็บ ซอร์สโค้ดเปิด", "https://www.falstad.com/circuit/"),
            S("PhET Circuit Construction Kit: DC", "แนวคิดการต่อวงจรและวัดค่าแบบแล็บ", "ใช้ได้ฟรี สัญญาอนุญาต CC BY 4.0", "https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc"),
            S("การไฟฟ้านครหลวง (MEA) และการไฟฟ้าส่วนภูมิภาค (PEA)", "แรงดันไฟบ้าน 230 V 50 Hz อัตราค่าไฟ และคำแนะนำความปลอดภัย", "ข้อมูลเปิดบนเว็บไซต์หน่วยงาน", "https://www.mea.or.th/"),
        ],
        "restricted": [
            S("IEC 60479-1 Effects of current on human beings and livestock", "ระดับกระแสที่เป็นอันตรายต่อหัวใจ และความต้านทานร่างกาย", "มาตรฐาน IEC ต้องซื้อ ตัวเลขทั่วไปถูกอ้างในตำราความปลอดภัยไฟฟ้า"),
            S("มาตรฐานการติดตั้งทางไฟฟ้าสำหรับประเทศไทย (วสท. 2001) และ IEC 60364", "ขนาดเบรกเกอร์ สายไฟ สายดิน และเครื่องตัดไฟรั่ว 30 mA", "มาตรฐานต้องซื้อ หน้านี้ใช้เพียงหลักการทั่วไป"),
            S("IEC 60898 และ IEC 61008/61009", "เส้นโค้งการตัดของเบรกเกอร์ และเวลาตัดของเครื่องตัดไฟรั่ว", "มาตรฐานต้องซื้อ"),
        ],
        "none": [
            S("ค่าไฟต่อหน่วย", "ค่าเริ่มต้น 4.20 บาทต่อหน่วย", "ค่าสมมติ อัตราจริงเป็นแบบขั้นบันไดและมีค่า Ft ซึ่งเปลี่ยนทุกงวด ปรับค่าได้ด้วยแถบเลื่อน"),
            S("พิกัดกระแสสายไฟ", "1.5 mm² = 15 A, 2.5 mm² = 21 A, 4 mm² = 28 A และความยาวสาย 20 ม.", "ค่าประมาณ พิกัดจริงขึ้นกับชนิดสาย วิธีติดตั้ง และอุณหภูมิ"),
            S("ความต้านทานร่างกายและเส้นทางกระแสรั่ว", "ร่างกาย 2,000 Ω และสายดิน 20 Ω", "ค่าตัวอย่าง ความต้านทานจริงเปลี่ยนตามความชื้น แรงดัน และเส้นทางผ่านร่างกาย"),
            S("เวลาตัดของเบรกเกอร์ในภาพ", "ตัดแบบความร้อนหลังเกินพิกัดราว 2.5 วินาที และตัดทันทีเมื่อเกิน 5 เท่า", "ย่อเวลาให้เห็นผลเร็ว เบรกเกอร์จริงอาจใช้เวลาหลายนาทีเมื่อเกินพิกัดไม่มาก"),
            S("กำลังไฟฟ้าของเครื่องใช้ไฟฟ้า", "ทีวี ตู้เย็น กาต้มน้ำ แอร์ และอื่น ๆ", "ค่าทั่วไป เครื่องจริงดูได้จากป้ายบนตัวเครื่อง แอร์และตู้เย็นยังมีกระแสกระชากตอนเริ่มทำงาน"),
        ],
    },
    "chem-bio-lab": {
        "eyebrow": "CHEM · BIO LAB · แหล่งข้อมูล",
        "back": ("Main.dc.html", "← กลับไปที่แล็บเคมีและชีววิทยา"),
        "intro": "แล็บนี้ใช้ทฤษฎีการชน สมการอาร์เรเนียส และแบบจำลองระบาดวิทยา SEIR ซึ่งเป็นเนื้อหามาตรฐาน วิธีวิเคราะห์อัตราการเติบโตมาจากงานวิจัยที่ใช้จริงในการระบาด แต่พารามิเตอร์ในตัวจำลองเป็นค่าตัวอย่าง ไม่ใช่ข้อมูลของโรคใดโรคหนึ่ง",
        "open": [
            S("OpenStax Chemistry 2e บทที่ 12: จลนศาสตร์เคมี", "ทฤษฎีการชน พลังงานกระตุ้น สมการอาร์เรเนียส และตัวเร่งปฏิกิริยา", "ตำราเปิด สัญญาอนุญาต CC BY 4.0", "https://openstax.org/books/chemistry-2e/pages/12-introduction"),
            S("Kermack, W. O. & McKendrick, A. G. (1927). A contribution to the mathematical theory of epidemics. Proc. R. Soc. A 115", "ต้นแบบของแบบจำลองแบ่งกลุ่ม SIR/SEIR", "บทความเปิดให้อ่านฟรีบนเว็บไซต์ Royal Society", "https://doi.org/10.1098/rspa.1927.0118"),
            S("Wallinga, J. & Lipsitch, M. (2007). How generation intervals shape the relationship between growth rates and reproductive numbers. Proc. R. Soc. B 274", "สูตรแปลงอัตราการเติบโต r เป็น R0 ≈ (1 + r/σ)(1 + r/γ)", "บทความเปิดให้อ่านฟรีบนเว็บไซต์ Royal Society", "https://doi.org/10.1098/rspb.2006.3754"),
            S("Our World in Data: COVID-19, Influenza, Measles", "ตัวอย่างข้อมูลผู้ป่วยจริงที่ใช้วิธีวิเคราะห์แบบเดียวกันได้", "ข้อมูลเปิด สัญญาอนุญาต CC BY 4.0", "https://ourworldindata.org/coronavirus"),
            S("กรมควบคุมโรค กระทรวงสาธารณสุข", "ข้อมูลเฝ้าระวังโรคติดต่อในประเทศไทย", "รายงานเผยแพร่บนเว็บไซต์หน่วยงาน", "https://ddc.moph.go.th/"),
            S("องค์การอนามัยโลก (WHO)", "ภูมิคุ้มกันหมู่ และประสิทธิภาพของวัคซีนกับมาตรการทางสังคม", "ข้อมูลเปิดบนเว็บไซต์", "https://www.who.int/"),
        ],
        "restricted": [
            S("Anderson, R. M. & May, R. M. Infectious Diseases of Humans: Dynamics and Control", "ค่า R0 ของโรคต่าง ๆ และภูมิคุ้มกันหมู่ 1 − 1/R0", "หนังสือ ต้องซื้อหรือยืมจากห้องสมุด"),
            S("Guerra, F. M. et al. (2017). The basic reproduction number (R0) of measles: a systematic review. Lancet Infectious Diseases 17", "ช่วง R0 ของหัด 12–18 ที่มักอ้างถึง", "บทความวารสาร ต้องสมัครสมาชิกหรือซื้อบทความ"),
            S("ข้อมูลผู้ป่วยรายบุคคล", "การสอบสวนโรคและการหาห่วงโซ่การแพร่เชื้อจริง", "เป็นข้อมูลส่วนบุคคล เข้าถึงได้เฉพาะหน่วยงานสาธารณสุขและนักวิจัยที่ได้รับอนุญาต"),
        ],
        "none": [
            S("พารามิเตอร์ปฏิกิริยา A + B → C", "Ea 50 kJ/mol ความน่าจะเป็นในการเกิดปฏิกิริยา 6% ต่อการชนที่ 300 K และตัวเร่งลด Ea 8 kJ/mol", "ค่าสมมติ ไม่ใช่ปฏิกิริยาเคมีจริงใด ๆ ความเร็วโมเลกุลในภาพช้ากว่าจริงมาก"),
            S("กราฟการกระจายพลังงาน", "รูปกราฟและตำแหน่ง Ea", "วาดเป็นภาพประกอบ ไม่ตามสเกล"),
            S("พารามิเตอร์ของโรคในการจำลองทีละคน", "รัศมีแพร่เชื้อ โอกาสแพร่ต่อวัน ระยะฟักตัว 3 วัน ระยะแพร่เชื้อ 7 วัน", "ค่าตัวอย่าง ไม่ใช่โรคใดโรคหนึ่ง"),
            S("ประสิทธิภาพของมาตรการ", "หน้ากากลดการแพร่ 40% วัคซีนป้องกัน 90%", "ค่าสมมติเพื่อเปรียบเทียบ ค่าจริงต่างกันตามโรค สายพันธุ์ ชนิดวัคซีน และการใช้งานจริง"),
            S("ขีดความสามารถของโรงพยาบาล", "เส้น 3% ของประชากรในกราฟ SEIR", "ค่าสมมติเพื่อแสดงแนวคิดการทำให้กราฟแบนลง"),
        ],
    },
}

TEMPLATE = r'''<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>แหล่งข้อมูลและการเข้าถึง</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&amp;family=IBM+Plex+Sans+Thai:wght@400;500;600;700&amp;display=swap">
<style>
body{margin:0;background:#F3F6F7}
a{color:#0A6A94}a:hover{color:#074E6E}
a:focus-visible,button:focus-visible{outline:3px solid #B04A0C;outline-offset:2px}
</style>
</helmet>
<div style="font-family: 'IBM Plex Sans Thai', system-ui, sans-serif; color: #0F2A3A; background: #F3F6F7; box-sizing: border-box; padding: 32px clamp(16px, 3vw, 40px) 56px">
<div style="max-width: 1100px; margin: 0 auto; display: flex; flex-direction: column; gap: 28px">
<nav style="font-size: 15px; font-weight: 600"><a href="__BACKHREF__" style="min-height: 44px; display: inline-flex; align-items: center">__BACKLABEL__</a></nav>
<header style="display: flex; flex-direction: column; gap: 8px">
<div style="font-size: 14px; font-weight: 600; letter-spacing: 0.08em; color: #0A6A94">__EYEBROW__</div>
<h1 style="margin: 0; font-size: clamp(30px, 4vw, 44px); line-height: 1.2; font-weight: 700">แหล่งข้อมูลและการเข้าถึง</h1>
<p style="margin: 0; font-size: 17px; line-height: 1.7; color: #4A5D6A">__INTRO__</p>
</header>
<div role="group" aria-label="กรองตามการเข้าถึง" style="display: flex; flex-wrap: wrap; gap: 8px">
<sc-for list="{{filters}}" as="f" hint-placeholder-count="4">
<button type="button" onClick="{{f.pick}}" aria-pressed="{{f.pressed}}" style="min-height: 44px; padding: 0 16px; border-radius: 999px; border: 1.5px solid {{f.border}}; background: {{f.bg}}; color: {{f.fg}}; font-family: inherit; font-size: 15px; font-weight: 600; cursor: pointer">{{f.name}}</button>
</sc-for>
</div>
<sc-for list="{{groups}}" as="g" hint-placeholder-count="3">
<section style="display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap">
<span style="font-size: 13px; font-weight: 700; padding: 4px 12px; border-radius: 999px; background: {{g.tagBg}}; color: {{g.tagFg}}">{{g.tag}}</span>
<h2 style="margin: 0; font-size: 22px; font-weight: 700">{{g.title}}</h2>
<span style="font-family: 'IBM Plex Mono', monospace; font-size: 14px; color: #4A5D6A">{{g.count}}</span>
</div>
<p style="margin: 0; font-size: 15px; line-height: 1.7; color: #4A5D6A">{{g.desc}}</p>
<sc-for list="{{g.items}}" as="x" hint-placeholder-count="4">
<div style="background: #FFFFFF; border: 1px solid #D5DEE3; border-left-color: #D5DEE3; border-radius: 14px; padding: 16px 18px; display: flex; flex-direction: column; gap: 6px">
<div style="font-size: 16px; font-weight: 700; line-height: 1.5">{{x.title}}</div>
<div style="font-size: 14px; line-height: 1.65; color: #34495A"><strong>ใช้กับ:</strong> {{x.used}}</div>
<div style="font-size: 14px; line-height: 1.65; color: #34495A"><strong>การเข้าถึง:</strong> {{x.access}}</div>
<sc-if value="{{x.url}}" hint-placeholder-val="{{ true }}"><a href="{{x.url}}" target="_blank" rel="noopener" style="font-size: 14px; word-break: break-all">{{x.url}}</a></sc-if>
</div>
</sc-for>
</section>
</sc-for>
<p style="margin: 0; font-size: 13px; line-height: 1.7; color: #4A5D6A">ตรวจสอบลิงก์เมื่อเดือนพฤศจิกายน 2569 ถ้าพบข้อมูลผิดหรือมีแหล่งที่ดีกว่า แจ้งได้ใน GitHub ของโปรเจกต์</p>
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":1360,"height":2200}}'>
class Component extends DCLogic {
  constructor() {
    super(...arguments);
    this.state = { filter: 'all' };
    this.SRC = __DATA__;
  }

  renderVals() {
    var self = this, s = this.state, SRC = this.SRC;
    var meta = [
      { id: 'open', tag: 'เปิดเผย', title: 'ข้อมูลที่หาได้และใช้ได้ฟรี', desc: 'ใครก็ตรวจสอบได้ทันทีผ่านลิงก์', tagBg: '#DDEFF6', tagFg: '#0A4F70' },
      { id: 'restricted', tag: 'จำกัดการเข้าถึง', title: 'มีข้อมูลอยู่ แต่ต้องลงทะเบียน ซื้อ หรือเฉพาะหน่วยงาน', desc: 'ข้อมูลเหล่านี้มีอยู่จริง แต่เราใส่ได้แค่ส่วนที่เผยแพร่ทั่วไป หรือไม่ได้ใส่เลยเพราะเงื่อนไขการใช้งาน', tagBg: '#FFF1CC', tagFg: '#6B4A00' },
      { id: 'none', tag: 'ไม่มีข้อมูลเปิดเผย', title: 'ไม่มีข้อมูลที่ใช้ได้ ตัวจำลองจึงใช้ค่าประมาณ', desc: 'ตัวเลขในส่วนเหล่านี้เป็นค่าตัวอย่างหรือสมมติของเรา เพื่อให้เห็นหลักการ ไม่ควรนำไปใช้เป็นข้อมูลจริง', tagBg: '#FCE3CF', tagFg: '#7E3407' }
    ];
    var groups = meta.filter(function (m) { return s.filter === 'all' || s.filter === m.id; }).map(function (m) {
      var items = SRC[m.id] || [];
      return { tag: m.tag, title: m.title, desc: m.desc, tagBg: m.tagBg, tagFg: m.tagFg, count: items.length + ' รายการ', items: items };
    });
    var fl = [{ id: 'all', name: 'ทั้งหมด' }].concat(meta.map(function (m) { return { id: m.id, name: m.tag }; }));
    return {
      groups: groups,
      filters: fl.map(function (f) { var on = f.id === s.filter; return { name: f.name, pressed: on ? 'true' : 'false', bg: on ? '#0A6A94' : '#FFFFFF', fg: on ? '#FFFFFF' : '#0F2A3A', border: on ? '#0A6A94' : '#C9D4DA', pick: function () { self.setState({ filter: f.id }); } }; })
    };
  }
}
</script>
</body>
</html>
'''


def main():
    for sim, cfg in SIMS.items():
        data = {k: cfg[k] for k in ("open", "restricted", "none")}
        out = (TEMPLATE.replace("__BACKHREF__", cfg["back"][0]).replace("__BACKLABEL__", cfg["back"][1])
               .replace("__EYEBROW__", cfg["eyebrow"]).replace("__INTRO__", cfg["intro"])
               .replace("__DATA__", json.dumps(data, ensure_ascii=False)))
        path = os.path.join(ROOT, "src", sim, "Sources.dc.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", os.path.relpath(path, ROOT), sum(len(v) for v in data.values()), "sources")


if __name__ == "__main__":
    main()
