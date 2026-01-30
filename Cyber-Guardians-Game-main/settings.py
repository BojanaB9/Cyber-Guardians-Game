import pygame
import os

class GameSettings:
    def __init__(self):
        self.screen_width = 900
        self.screen_height = 700
        self.language = None  # Ќе се постави при избор (MK, EN, AL, TR)
        self.show_language_selection = True
        self.reset_game()

    def reset_game(self):
        # Основни параметри за движење и тежина
        self.player_speed = 6
        self.bullet_speed = -8
        self.enemy_speed = 1.0
        self.score = 0
        self.last_life_score = 0
        self.knowledge_points = 0
        self.shields = 3
        self.current_level = 1
        self.game_active = True
        self.show_instructions = True
        self.boss_active = False
        self.victory = False
        self.font_path = os.path.join("assets", "PressStart2P-Regular.ttf")
        self.bg_color = (10, 10, 30)
        self.pending_boss_damage = 0

        # Целосен речник со преводи за сите клучеви и јазици
        self.translations = {
            'MK': {
                'hud': "НИВО: {} | ЖИВОТИ: {} | ПОЕНИ: {} | ЗНАЕЊЕ: {}",
                'hud_boss': "НИВО: {} | ЖИВОТИ: {} | ПОЕНИ: {}",
                'start': "ПРИТИСНИ SPACE ЗА СТАРТ",
                'game_over': "ИЗГУБИ? УЧИ ОД ГРЕШКИТЕ! ПРИТИСНИ 'R'!",
                'victory_msg': "ТИ СИ САЈБЕР ХЕРОЈ! СИСТЕМОТ Е БЕЗБЕДЕН!",
                'level_up': "НИВО {} ЗАВРШЕНО! ОДИМЕ ПОНАТАМУ!",
                'press_space': "Притисни SPACE за продолжување",
                'boss_title': "ГЛАВНИОТ ВИРУС НАПАЃА!",
                'boss_desc': ["Погоди го 5 пати за квиз.", "Одговори точно за да го победиш.", "Грешка = губиш живот!"],
                'level_titles': {
                    1: "НИВО 1: ПРВА ЛИНИЈА НА ОДБРАНА", 2: "НИВО 2: ЧУВАРОТ НА ПОРТАТА (БОС)",
                    3: "НИВО 3: ДИГИТАЛНА ЗАМКА", 4: "НИВО 4: ФИШИНГ ПРЕДАТОР (БОС)",
                    5: "НИВО 5: КРАЈНА ЗАШТИТА", 6: "НИВО 6: ФИНАЛНА ПРЕСМЕТКА (БОС)"
                },
                'level_desc': {
                    1: ["Добредојде, млади Сајбер Чувар!", "Твојата мисија започнува со основите.",
                        "Собери 5 токени за знаење.","БОНУС: На секои 250 поени добиваш +1 живот!", "Научи за HTTPS и силните лозинки.",
                        "Биди брз, вирусите се само почеток!", "За да ги видиш собраните знаења притисни 'P'"],
                    2: ["ВНИМАНИЕ! Се појави првиот голем вирус!", "Тој ја блокира портата со лозинки.",
                        "Погоди го 5 пати за квиз.", "Одговори точно на 5 прашања.", "Секоја грешка чини еден живот!"],
                    3: ["Одлично! Системот станува побрз.", "Сега учиме за Phishing измами.",
                        "Собери 10 знаења за VPN и линкови.", "Вирусите сега напаѓаат во групи.",
                        "Не дозволувај да те опколат!"],
                    4: ["Фишинг Предаторот сака да те измами!", "Тој е побрз од претходниот Бос.",
                        "Користи го знаењето од Ниво 3.", "10 точни одговори го чистат вирусот.",
                        "Биди фокусиран на прашањата!"],
                    5: ["Последна фаза на учење!", "Научи за Backup и Ransomware.", "Ова е најбрзото ниво досега!",
                        "Собери ги последните 15 знаења.", "Финалето е многу блиску!"],
                    6: ["ОВА Е ФИНАЛНАТА БИТКА!", "Најголемиот вирус ги користи сите моќи.",
                        "Ќе те прашува 15 прашања за сè што научи досега.", "Победи го за целосна безбедност.",
                        "Среќно, Сајбер Хероју!"]
                }
            },
            'EN': {
                'hud': "LEVEL: {} | LIVES: {} | POINTS: {} | KNOWLEDGE: {}",
                'hud_boss': "LEVEL: {} | LIVES: {} | POINTS: {}",
                'start': "PRESS SPACE TO START",
                'game_over': "LOST? LEARN FROM MISTAKES! PRESS 'R'!",
                'victory_msg': "YOU ARE A CYBER HERO! SYSTEM SECURED!",
                'level_up': "LEVEL {} COMPLETED! MOVING ON!",
                'press_space': "Press SPACE to continue",
                'boss_title': "THE MAIN VIRUS ATTACKS!",
                'boss_desc': ["Hit it 5 times for a quiz.", "Answer correctly to win.", "Mistake = lose a life!"],
                'level_titles': {
                    1: "LEVEL 1: FIRST LINE OF DEFENSE", 2: "LEVEL 2: GATE KEEPER (BOSS)",
                    3: "LEVEL 3: DIGITAL TRAP", 4: "LEVEL 4: PHISHING PREDATOR (BOSS)",
                    5: "LEVEL 5: ULTIMATE DEFENSE", 6: "LEVEL 6: FINAL SHOWDOWN (BOSS)"
                },
                'level_desc': {
                    1: ["Welcome, young Cyber Guardian!", "Your mission starts with the basics.",
                        "Collect 5 knowledge tokens.", "BONUS: Every 250 points gives you +1 life!", "Learn about HTTPS and strong passwords.",
                        "Be fast, viruses are just the beginning!", "To see the collected knowledge, press 'P'"],
                    2: ["WARNING! The first big virus appeared!", "He blocks the gate with passwords.",
                        "Hit him 5 times for a quiz.", "Answer 5 questions correctly.", "Every mistake costs one life!"],
                    3: ["Great! The system is getting faster.", "Now we learn about Phishing scams.",
                        "Collect 10 knowledge tokens for VPN and links.", "Viruses are now attacking in swarms.",
                        "Don't let them surround you!"],
                    4: ["The Phishing Predator is here to trick you!", "He is faster than the previous Boss.",
                        "Use the knowledge from Level 3.", "10 correct answers will clear the virus.",
                        "Stay focused on the questions!"],
                    5: ["Final learning phase!", "Learn about Backup and Ransomware.", "This is the fastest level yet!",
                        "Collect the last 15 tokens.", "The finale is very close!"],
                    6: ["THIS IS THE FINAL BATTLE!", "The Ultimate Virus uses all its powers.",
                        "He will ask 15 questions about everything you've learned.", "Defeat it for total security.",
                        "Good luck, Cyber Hero!"]
                }
            },
            'AL': {
                'hud': "NIVELI: {} | JETËT: {} | PIKËT: {} | NJOHURITË: {}",
                'hud_boss': "NIVELI: {} | JETËT: {} | PIKËT: {}",
                'start': "SHTYP SPACE PËR FILLIM",
                'game_over': "HUMBË? MËSO NGA GABIMET! SHTYP 'R'!",
                'victory_msg': "JE NJË HERO KIBERNETIK! SISTEMI I SIGURT!",
                'level_up': "NIVELI {} U KALUA! VAZHDOJMË!",
                'press_space': "Shtyp SPACE për të vazhduar",
                'boss_title': "SULMI I VIRUSIT KRYESOR!",
                'boss_desc': ["Gjuaj 5 herë për kuiz.", "Përgjigju saktë për fitore.", "Gabimi = humb jetë!"],
                'level_titles': {
                    1: "NIVELI 1: LINJA E PARË E MBROJTJES", 2: "NIVELI 2: ROJA E PORTËS (BOSS)",
                    3: "NIVELI 3: KURTHI DIGJITAL", 4: "NIVELI 4: PREDATORI PHISHING (BOSS)",
                    5: "NIVELI 5: MBROJTJA E FUNDIT", 6: "NIVELI 6: BALLAFAQIMI FINAL (BOSS)"
                },
                'level_desc': {
                    1: ["Mirësevini, Mbrojtës i ri Kibernetik!", "Misioni juaj fillon me bazat.",
                        "Mblidhni 5 argumente njohurish.", "BONUS: Çdo 250 pikë ju jep +1 jetë!", "Mësoni për HTTPS dhe fjalëkalimet.",
                        "Shpejtoni, viruset janë vetëm fillimi!", "Për të parë njohuritë e mbledhura, shtyp 'P'"],
                    2: ["KUJDES! U shfaq virusi i parë i madh!", "Ai bllokon portën me fjalëkalime.",
                        "Gjuaj 5 herë për të hapur kuizin.", "Përgjigju saktë në 5 pyetje.", "Çdo gabim ju kushton një jetë!"],
                    3: ["Shkëlqyeshëm! Sistemi po shpejtohet.", "Tani mësojmë për mashtrimet Phishing.",
                        "Mblidhni 10 njohuri për VPN dhe linqet.", "Viruset tani sulmojnë në grupe.",
                        "Mos i lini t'ju rrethojnë!"],
                    4: ["Predatori Phishing dëshiron t'ju mashtrojë!", "Ai është më i shpejtë se Boss-i i parë.",
                        "Përdorni njohuritë nga Niveli 3.", "10 përgjigje të sakta fshijnë virusin.",
                        "Fokusohuni te pyetjet!"],
                    5: ["Faza përfundimtare e mësimit!", "Mësoni për Backup dhe Ransomware.",
                        "Ky është niveli më i shpejtë deri tani!", "Mblidhni 15 njohuritë e fundit.",
                        "Finalja është shumë afër!"],
                    6: ["KJO ËSHTË BETEJA FINALE!", "Virusi më i madh përdor të gjitha fuqitë.",
                        "Do t'ju bëjë 15 pyetje për gjithçka që keni mësuar.", "Mposhtni atë për siguri të plotë.",
                        "Suksese, Hero Kibernetik!"]
                }
            },
            'TR': {
                'hud': "SEVİYE: {} | CAN: {} | PUANLAR: {} | BİLGİ: {}",
                'hud_boss': "SEVİYE: {} | CAN: {} | PUANLAR: {}",
                'start': "BAŞLAMAK İÇİN SPACE'E BASIN",
                'game_over': "KAYBETTİN Mİ? HATALARDAN ÖĞREN! 'R'YE BAS!",
                'victory_msg': "SİBER KAHRAMANSIN! SİSTEM GÜVENLİ!",
                'level_up': "SEVİYE {} TAMAMLANDI! DEVAM ET!",
                'press_space': "Devam etmek için SPACE'e basın",
                'boss_title': "ANA VİRÜS SALDIRIYOR!",
                'boss_desc': ["Test için 5 kez vur.", "Kazanmak için doğru cevapla.", "Hata = can kaybı!"],
                'level_titles': {
                    1: "SEVİYE 1: İLK SAVUNMA HATTI", 2: "SEVİYE 2: KAPI KORUYUCUSU (BOSS)",
                    3: "SEVİYE 3: DİJİTAL TUZAK", 4: "SEVİYE 4: PHISHING AVCI (BOSS)",
                    5: "SEVİYE 5: NİHAİ KORUMA", 6: "SEVİYE 6: FİNAL HESAPLAŞMASI (BOSS)"
                },
                'level_desc': {
                    1: ["Hoş geldin, genç Siber Koruyucu!", "Görevin temel bilgilerle başlıyor.",
                        "5 bilgi tokeni topla.", "BONUS: Her 250 puan size +1 can verir!", "HTTPS ve güçlü şifreleri öğren.",
                        "Hızlı ol, virüsler sadece başlangıç!", "Toplanan bilgileri görmek için 'P' tuşuna basın"],
                    2: ["DİKKAT! İlk büyük virüs ortaya çıktı!", "Kapıyı şifrelerle bloke ediyor.",
                        "Testi açmak için 5 kez vur.", "5 soruyu doğru cevaplamalısın.", "Her hata bir cana mal olur!"],
                    3: ["Harika! Sistem giderek hızlanıyor.", "Şimdi Phishing dolandırıcılığını öğreniyoruz.",
                        "VPN ve bağlantılar hakkında 10 bilgi topla.", "Virüsler artık sürüler halinde saldırıyor.",
                        "Etrafını sarmalarına izin verme!"],
                    4: ["Phishing Avcısı sizi kandırmaya çalışıyor!", "Önceki Boss'tan çok daha hızlı.",
                        "Seviye 3 bilgilerini kullan.", "10 doğru cevap virüsü temizler.", "Sorulara odaklan!"],
                    5: ["Son öğrenme aşaması!", "Yedekleme ve Ransomware öğren.", "Bu şimdiye kadarki en hızlı seviye!",
                        "Son 15 bilgiyi topla.", "Final çok yakında!"],
                    6: ["BU FİNAL SAVAŞI!", "En büyük virüs tüm gücünü kullanıyor.",
                        "Öğrendiğin her şey hakkında 15 soru soracak.", "Tam güvenlik için onu yen.",
                        "Başarılar, Siber Kahraman!"]
                }
            }
        }

    def next_level(self):
        self.current_level += 1
        # Позначајно забрзување на непријателите
        self.enemy_speed += 0.8
        # Зголемување на брзината на играчот
        self.player_speed += 0.5
        self.boss_active = False
