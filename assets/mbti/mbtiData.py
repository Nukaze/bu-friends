import random
def get_MbtiQuizEN():
    return [["IE","Expend energy, enjoy groups or b. conserve energy, enjoy one-on-one"],
            ["IE","Are u out-going?"],
            ["IE","Are u out-going?"],
            ["IE","Are u out-going?"],
            ["IE","Are u out-going?"],
            ["IE","Are u out-going?"],
            ["IE","Are u out-going?"],
            
            ["NS","Which one you trust Present or Future?"],
            ["NS","Which one you trust Present or Future?"],
            ["NS","Which one you trust Present or Future?"],
            ["NS","Which one you trust Present or Future?"],
            ["NS","Which one you trust Present or Future?"],
            ["NS","Which one you trust Present or Future?"],
            ["NS","Which one you trust Present or Future?"],
            
            ["FT","When someone make mistake what you do to help?"],
            ["FT","When someone make mistake what you do to help?"],
            ["FT","When someone make mistake what you do to help?"],
            ["FT","When someone make mistake what you do to help?"],
            ["FT","When someone make mistake what you do to help?"],
            ["FT","When someone make mistake what you do to help?"],
            ["FT","When someone make mistake what you do to help?"],
            
            ["PJ","WHEN YOU GO SOMEWHERE FOR THE DAY, WOULD YOU RATHER?"],
            ["PJ","Have you wake-up instanly when alarm is clocking"],
            ["PJ","Have you wake-up instanly when alarm is clocking"],
            ["PJ","Have you wake-up instanly when alarm is clocking"],
            ["PJ","Have you wake-up instanly when alarm is clocking"],
            ["PJ","Have you wake-up instanly when alarm is clocking"],
            ["PJ","Have you wake-up instanly when alarm is clocking"]    
]

def get_MbtiQuizTH():
     return [["IE","คูณชื่นชอบการอยู่กับกลุ่มเพื่อนแบบไหน ?"],
            ["IE","ในหมู่เพื่อนของคุณคือคุณคือ ?"],
            ["IE","เมื่อคุณพบปะเพื่อนใหม่ คุณจะบอกความสนใจหรืองานอดิเรกในตอน ?"],
            ["IE","การแสดงออกทางอารมณ์ของคุณมักจะเป็นแบบไหน"],
            ["IE",""],
            ["IE",""],
            ["IE",""],
            
            ["NS","ถ้าหากว่าวันนึงคุณได้เป็นอาจารย์ คุณอยากสอนนักเรียนแบบไหน?"],
            ["NS","เมื่อคุณพบเจอกับปัญหา ที่อาจจะมีหลาย ๆ คนประสบคุณจะแก้ไขปัญหาแบบไหน?"],
            ["NS","คุณคิดว่าคุณนั้นเป็นคนมีเป็นมีแนวคิดและวิธีการแบบไหน"],
            ["NS","คุณอยากจะมีเพื่อนแบบไหนมากกว่ากันระหว่าง"],
            ["NS",""],
            ["NS",""],
            ["NS",""],
            
            ["FT","คำชมของคนอื่นแบบไหนที่คุณรู้สึกว่าชื่นชอบมากกว่ากัน ระหว่าง"],
            ["FT","โดยปกติแล้วคุณนั้นเป็นคนแบบไหน ระหว่าง"],
            ["FT",""],
            ["FT",""],
            ["FT",""],
            ["FT",""],
            ["FT",""],
            
            ["PJ","เมื่อคุณหรือเพื่อน ๆ ของคุณจะไปเที่ยวกันคุณจะทำอย่างไร ?"],
            ["PJ","หากว่าคุณมีจะทำงาน รูปแบบในการทำงานคุณจะเป็นแบบไหน ?"],
            ["PJ","ในการทำงานทั่วไปประจำวันของคุณนั้น"],
            ["PJ",""],
            ["PJ",""],
            ["PJ",""],
            ["PJ",""]    
]
    
def get_MbtiAnsTH():
    return [["E","I","เพลิดเพลินกับเพื่อน ๆ กลุ่มใหญ่","เพลิดเพลินกับเพื่อน ๆ กลุ่มเล็ก"],
            ["I","E","คนสุดท้ายที่จะรู้เรื่องราวภายในกลุ่ม","รับรู้ข่าวสารของเพื่อนในกลุ่มอยู่ตลอด"],
            ["I","E","หลังจากที่ได้ทำความรู้จักจริง ๆ แล้ว","ตอนที่เจอกันเลย"],
            ["E","I","แสดงความรู้สึกออกมาอย่างเต็มที่ ไม่อัดอั้น","เก็บความรู้สึกไว้กับตัวเอง ไม่แสดงมากนัก"],
            ["E","I","",""],
            ["I","E","",""],
            ["I","E","",""],
            
            ["S","N","สอนตามหลักสูตรตามข้อเท็จจริงที่มีการพิสูจน์แล้ว","หลักสูตรที่เกี่ยวกับหลักการ แนวคิด ทฤษฎี"],
            ["N","S","คิดค้นวิธีการแก้ไขปัญหาขึ้นมาเอง","แก้ไขด้วยวิธีที่มีการแก้ไขมาก่อนแล้วและเป็นที่ยอมรับ"],
            ["N","S","คนที่คิดนอกกรอบ สร้างสรรค์ ไม่ยึดติดตามหลักการ","คนที่นำหลักการมาปรับใช้ได้อย่างดี ปฏิบัติเก่ง"],
            ["N","S","คนที่มีความคิดสร้างสรรค์ มักมาพร้อมกับอะไรใหม่ ๆ","คนที่มีเหตุผลบนพื้นฐานความเป็นจริง เชื่อถือได้"],
            ["S","N","",""],
            ["S","N","",""],
            ["S","N","",""],
            
            ["F","T","คุณเป็นคนมีความจริงใจ ซื่อตรงและน่าคบหา","คุณเป็นคนที่มีเหตุผล และสม่ำเสมอ"],
            ["T","F","ใช้ตรรกะเหตุผล มากกว่าความรู้สึกต่าง ๆ","ใช้ความรู้สึกและความเห็นอกเห็นใจ มากกว่าเหตุผล"],
            ["F","T","",""],
            ["T","F","",""],
            ["F","T","",""],
            ["T","F","",""],
            ["F","T","",""],
            
            ["J","P","งั้นเรามาวางแผนกันว่าจะทำอะไรบ้าง ไปวันไหน","ไปกันเลย ลุย!!"],
            ["P","J","เริ่มทำงานได้เลยโดยจัดการปัญหา ไปพร้อม ๆ กันได้","วางแผนอย่างเป็นระบบก่อนเริ่มทำงาน"],
            ["P","J","ค่อนข้างชอบเหตุฉุกเฉินที่ทำให้คุณแก้ไขได้","มักจะวางแผนงานของคุณ โดยให้ความกดดันน้อยลง"],
            ["P","J","",""],
            ["P","J","",""],
            ["P","J","",""],
            ["P","J","",""]    
]

#randLst = random.sample(range(len(quiz)),len(quiz))