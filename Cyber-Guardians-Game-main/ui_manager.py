import pygame
import os
import random
import math


def draw_language_selection(screen, settings):
    screen.fill((10, 20, 50))
    font = pygame.font.Font(settings.font_path, 20)
    options = [("1. МАКЕДОНСКИ", 'MK'), ("2. ENGLISH", 'EN'), ("3. SHQIP", 'AL'), ("4. TÜRKÇE", 'TR')]
    title = font.render("CHOOSE LANGUAGE / ИЗБЕРИ ЈАЗИК", True, (255, 255, 255))
    screen.blit(title, (450 - title.get_width() // 2, 200))
    for i, (text, code) in enumerate(options):
        txt = font.render(text, True, (0, 255, 255))
        screen.blit(txt, (450 - txt.get_width() // 2, 300 + i * 60))


def draw_detailed_level_intro(screen, settings):
    lang = settings.language or 'MK'
    lvl = settings.current_level
    overlay = pygame.Surface((900, 700), pygame.SRCALPHA)
    overlay.fill((0, 0, 40, 230))
    screen.blit(overlay, (0, 0))
    panel_w, panel_h = 700, 500
    panel_x, panel_y = (900 - panel_w) // 2, (700 - panel_h) // 2
    pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, panel_w, panel_h), border_radius=20)
    pygame.draw.rect(screen, (0, 255, 255), (panel_x, panel_y, panel_w, panel_h), width=5, border_radius=20)
    font_title = pygame.font.Font(settings.font_path, 20)
    font_text = pygame.font.Font(settings.font_path, 14)
    title_str = settings.translations[lang]['level_titles'].get(lvl, "")
    title_surf = font_title.render(title_str, True, (0, 0, 100))
    screen.blit(title_surf, (450 - title_surf.get_width() // 2, panel_y + 40))
    lines = settings.translations[lang]['level_desc'].get(lvl, [])
    for i, line in enumerate(lines):
        txt_surf = font_text.render(line, True, (40, 40, 40))
        screen.blit(txt_surf, (450 - txt_surf.get_width() // 2, panel_y + 130 + i * 50))
    space_str = settings.translations[lang]['press_space']
    screen.blit(font_text.render(space_str, True, (150, 0, 0)),
                (450 - font_text.size(space_str)[0] // 2, panel_y + panel_h - 40))


class LayeredBackgroundBlue:
    def __init__(self, settings, folder="assets/layered", size=(900, 700)):
        self.settings = settings;
        self.t = 0.0
        try:
            self.back = pygame.transform.smoothscale(pygame.image.load(os.path.join(folder, "blue-back.png")).convert(),
                                                     size)
            self.stars = pygame.transform.smoothscale(
                pygame.image.load(os.path.join(folder, "blue-stars.png")).convert_alpha(), size)
            self.props = [
                {"img": pygame.image.load(os.path.join(folder, "prop-planet-big.png")).convert_alpha(),
                 "pos": (650, 90), "spd": 0.35, "amp": 8},
                {"img": pygame.image.load(os.path.join(folder, "asteroid-1.png")).convert_alpha(), "pos": (820, 360),
                 "spd": 0.9, "amp": 4}
            ]
        except:
            self.back = pygame.Surface(size);
            self.back.fill((10, 10, 30))
            self.stars = pygame.Surface(size, pygame.SRCALPHA);
            self.props = []

    def update(self, dt_ms):
        self.t += dt_ms / 1000.0

    def draw(self, screen):
        screen.blit(self.back, (0, 0))
        screen.blit(self.stars, (0, int(math.sin(self.t * 0.5) * 2)))
        for p in self.props:
            y = p["pos"][1] + math.sin(self.t * p["spd"]) * p["amp"]
            screen.blit(p["img"], (p["pos"][0], int(y)))


# Во ui_manager.py
class QuizSystem:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.active = False

        # ОВИЕ ЛИНИИ МОРА ДА ПОСТОЈАТ ЗА ДА НЕМА ГРЕШКА
        self.questions_pool = []  # Листа на достапни прашања за тековното ниво
        self.used_questions = []  # Листа на веќе одговорени прашања
        self.current_q = None

        self.correct_answers_count = 0
        self.showing_feedback = False
        self.correct = False

        # Речник што ги мапира нивоата со соодветните прашања (1->Ниво 2, 3->Ниво 4...)
        self.questions_map = {2: 1, 4: 3, 6: 5}
        self.all_questions = {
            'MK': {
                1: [  # 15 прашања за Ниво 2
                    {"q": "Што прави HTTPS?", "o": ["Шифрира податоци", "Забрзува нет"], "c": 0,
                     "e": "HTTPS е клуч за приватност."},
                    {"q": "Добра лозинка содржи?", "o": ["Име на милениче", "Букви и знаци"], "c": 1,
                     "e": "Комплексноста е заштита."},
                    {"q": "Што е 2FA?", "o": ["Двоен слој заштита", "Вид екран"], "c": 0,
                     "e": "Бара дополнителен код на моб."},
                    {"q": "Кој треба да ја знае твојата шифра?", "o": ["Само јас", "Најдобриот другар"], "c": 0,
                     "e": "Лозинката е лична тајна."},
                    {"q": "Јавен Wi-Fi е најчесто?", "o": ["Небезбеден", "Најбрз"], "c": 0,
                     "e": "Податоците не се шифрирани."},
                    {"q": "Што поправа софтверскиот Update?", "o": ["Дупки во безбедноста", "Боја на икони"], "c": 0,
                     "e": "Ги крпи пропустите за хакери."},
                    {"q": "Заклучуваш екран кога?", "o": ["Стануваш од компјутер", "Само кога спиеш"], "c": 0,
                     "e": "Никогаш не оставај отворен пристап."},
                    {"q": "Дали е добро да имаш иста шифра секаде?", "o": ["Не, користи различни", "Да, полесно е"],
                     "c": 0, "e": "Ако една падне, другите се безбедни."},
                    {"q": "Проверуваш име на сајт за?", "o": ["Печатни грешки", "Убав дизајн"], "c": 0,
                     "e": "Лажните сајтови имаат слични имиња."},
                    {"q": "Pop-up вели имаш вирус. Што правиш?", "o": ["Игнорирај/Затвори", "Кликни веднаш"], "c": 0,
                     "e": "Тоа е често измама за вирус."},
                    {"q": "Колку карактери е силна лозинка?", "o": ["Најмалку 12", "Максимум 6"], "c": 0,
                     "e": "Подолга лозинка е потешка за кршење."},
                    {"q": "Името на мачката е добра шифра?", "o": ["Не, лоша е", "Да, супер е"], "c": 0,
                     "e": "Личните имиња се лесни за погодување."},
                    {"q": "Дали HTTPS е задолжителен за плаќање?", "o": ["Да, секогаш", "Не, не мора"], "c": 0,
                     "e": "HTTPS гарантира безбедно плаќање."},
                    {"q": "Што е посигурно од ПИН код?", "o": ["Биометрика", "Роденден"], "c": 0,
                     "e": "Отпечатокот е уникатен за тебе."},
                    {"q": "Каде не внесуваш лозинка?", "o": ["На сомнителни линкови", "На официјални сајтови"], "c": 0,
                     "e": "Чувај ги податоците од измамници."}
                ],
                2: [  # 25 прашања за Ниво 4
                    {"q": "Што е Phishing?", "o": ["Лажна порака за податоци", "Спорт"], "c": 0,
                     "e": "Измама за крадење лозинки."},
                    {"q": "Што проверуваш кај испраќачот?", "o": ["Емаил адресата", "Сликата"], "c": 0,
                     "e": "Името може лесно да се лажира."},
                    {"q": "Банка бара шифра преку емаил?", "o": ["Никогаш", "Често"], "c": 0,
                     "e": "Банките не бараат тајни податоци вака."},
                    {"q": "Што крие VPN?", "o": ["IP адресата", "Името на РС"], "c": 0,
                     "e": "VPN те прави анонимен за хакери."},
                    {"q": "Итна порака 'делувај веднаш' е?", "o": ["Знак за измама", "Секогаш важна"], "c": 0,
                     "e": "Хакерите користат лажна итност."},
                    {"q": "Отвораш 'zip' од непознати?", "o": ["Не, никогаш", "Да, ако е интересно"], "c": 0,
                     "e": "Може да содржи скриен Malware."},
                    {"q": "Smishing е Phishing преку?", "o": ["СМС порака", "Телефонски повик"], "c": 0,
                     "e": "Текстуалните пораки се нова мета."},
                    {"q": "Линковите во Phishing мејл се?", "o": ["Лажни и опасни", "Секогаш точни"], "c": 0,
                     "e": "Те водат до заземени страници."},
                    {"q": "Што проверуваш пред најава?", "o": ["URL адресата", "Рекламите"], "c": 0,
                     "e": "Провери дали е вистинскиот домен."},
                    {"q": "Антивирусот помага при Phishing?", "o": ["Да, блокира некои", "Не, воопшто"], "c": 0,
                     "e": "Модерните програми препознаваат измами."},
                    {"q": "Плаќаш на сајт без HTTPS?", "o": ["Не, опасно е", "Да, нема врска"], "c": 0,
                     "e": "Податоците од картичката можат да се украдат."},
                    {"q": "Твој пријател праќа чуден вирус?", "o": ["Можеби е хакиран", "Верувај му"], "c": 0,
                     "e": "Хакерите праќаат вируси од туѓи профили."},
                    {"q": "Што е социјален инженеринг?", "o": ["Манипулација на луѓе", "Програмирање"], "c": 0,
                     "e": "Лажење за да се добијат шифри."},
                    {"q": "Наградна игра бара матичен број?", "o": ["Измама е, бегај", "Пополни сè"], "c": 0,
                     "e": "Личните податоци не се за игри."},
                    {"q": "Private Mode те крие од хакери?", "o": ["Не", "Да"], "c": 0,
                     "e": "Само не чува историја на твојот РС."},
                    {"q": "Што е Spear Phishing?", "o": ["Напад на одредена личност", "Напад на сите"], "c": 0,
                     "e": "Многу прецизен и опасен напад."},
                    {"q": "Одговараш на спам пораки?", "o": ["Не, ги бришам", "Да, за забава"], "c": 0,
                     "e": "Одговарањето потврдува дека мејлот е активен."},
                    {"q": "Каде чуваш приватни слики?", "o": ["На безбедно/шифрирано", "На јавен облак"], "c": 0,
                     "e": "Приватноста мора да биде приоритет."},
                    {"q": "Внимаваш што објавуваш на мрежи?", "o": ["Да, многу", "Не, сè објавувам"], "c": 0,
                     "e": "Објавите откриваат многу за тебе."},
                    {"q": "Проверуваш дозволи на апликации?", "o": ["Да, пред инсталација", "Никогаш"], "c": 0,
                     "e": "Апликациите често бараат премногу пристап."},
                    {"q": "Инкогнито мод користиш на?", "o": ["Јавни компјутери", "Дома"], "c": 0,
                     "e": "Спречува другите да ја видат твојата сесија."},
                    {"q": "Ги зачувуваш лозинките во Chrome на факултет?", "o": ["Не, никако", "Да"], "c": 0,
                     "e": "Следниот корисник може да ти влезе во профил."},
                    {"q": "Wi-Fi се поврзува сам. Тоа е?", "o": ["Ризично", "Одлично"], "c": 0,
                     "e": "Можеш да се поврзеш на хакерска мрежа."},
                    {"q": "Полниш телефон на јавно USB?", "o": ["Избегнувам", "Секогаш"], "c": 0,
                     "e": "Постои ризик од Juice Jacking (крадење податоци)."},
                    {"q": "Ја читаш политиката за приватност?", "o": ["Треба да ја знам", "Досадно е"], "c": 0,
                     "e": "Таму пишува кој ги користи твоите податоци."}
                ],
                3: [  # 30 прашања за Ниво 6
                    {"q": "Што е Ransomware?", "o": ["Вирус за уцена", "Подарок"], "c": 0,
                     "e": "Ги заклучува фајловите за пари."},
                    {"q": "Backup помага при Ransomware?", "o": ["Да, ги враќа фајловите", "Не"], "c": 0,
                     "e": "Резервната копија е единствен спас."},
                    {"q": "Malware е кратенка за?", "o": ["Штетен софтвер", "Добар софтвер"], "c": 0,
                     "e": "Секој програм што прави штета."},
                    {"q": "Cloud Backup е безбеден?", "o": ["Да, на сервери", "Не"], "c": 0,
                     "e": "Податоците се чуваат надвор од твојот уред."},
                    {"q": "Што прави Password Manager?", "o": ["Чува лозинки безбедно", "Ги краде"], "c": 0,
                     "e": "Најдобар начин за менаџирање шифри."},
                    {"q": "Тројански коњ е?", "o": ["Маскиран вирус", "Игра"], "c": 0,
                     "e": "Изгледа корисно, но е опасно."},
                    {"q": "Што снима Keylogger?", "o": ["Сè што пишуваш", "Слики"], "c": 0,
                     "e": "Ги краде лозинките додека ги внесуваш."},
                    {"q": "Скенираш USB пред употреба?", "o": ["Да, задолжително", "Не"], "c": 0,
                     "e": "USB е најчест преносител на Malware."},
                    {"q": "Rootkit му дава на хакерот?", "o": ["Целосна контрола", "Ништо"], "c": 0,
                     "e": "Најтежок вирус за откривање."},
                    {"q": "Ажуриран Windows е?", "o": ["Потежок за хакирање", "Побавен"], "c": 0,
                     "e": "Сигурносните закрпи се пресудни."},
                    {"q": "Што прави Spyware?", "o": ["Те следи тајно", "Те штити"], "c": 0,
                     "e": "Снима активност и праќа до хакери."},
                    {"q": "Adware служи за?", "o": ["Досадни реклами", "Игри"], "c": 0,
                     "e": "Може да те пренасочи на опасни сајтови."},
                    {"q": "Worm (црв) се шири?", "o": ["Автоматски низ мрежа", "Само со клик"], "c": 0,
                     "e": "Не му треба човечка помош за ширење."},
                    {"q": "Енкрипција ги прави фајловите?", "o": ["Нечитливи за други", "Помали"], "c": 0,
                     "e": "Само ти со клуч можеш да ги отвориш."},
                    {"q": "Најслаба карика во безбедноста?", "o": ["Човекот", "Компјутерот"], "c": 0,
                     "e": "Луѓето најлесно се лажат со манипулација."},
                    {"q": "Zero-day напад е?", "o": ["Непозната закана", "Стар вирус"], "c": 0,
                     "e": "Напад за кој уште нема лек."},
                    {"q": "Што е Firewall?", "o": ["Филтер за сообраќај", "Вид антивирус"], "c": 0,
                     "e": "Одлучува што смее да влезе во мрежата."},
                    {"q": "DDoS напад го прави сајтот?", "o": ["Недостапен", "Побрз"], "c": 0,
                     "e": "Го преоптоварува со лажни барања."},
                    {"q": "Botnet е мрежа од?", "o": ["Заразени уреди", "Паметни луѓе"], "c": 0,
                     "e": "Хакерот ги користи за масовни напади."},
                    {"q": "Што е Sandboxing?", "o": ["Безбедна тест зона", "Игра"], "c": 0,
                     "e": "Изолира вирус за да не се рашири."},
                    {"q": "Digital Signature гарантира?", "o": ["Оригиналност", "Боја"], "c": 0,
                     "e": "Потврдува дека документот не е менуван."},
                    {"q": "Индустриска шпионажа користи?", "o": ["Malware", "Телефони"], "c": 0,
                     "e": "Крадење тајни од големи компании."},
                    {"q": "Го исклучуваш антивирусот за инсталација?", "o": ["Никогаш", "Да"], "c": 0,
                     "e": "Многу пиратски програми вака заразуваат."},
                    {"q": "Силна лозинка на рутер е?", "o": ["Задолжителна", "Неважна"], "c": 0,
                     "e": "Спречува соседи и хакери да ти влезат во мрежа."},
                    {"q": "Кој Wi-Fi е најнов и најбезбеден?", "o": ["WPA3", "WEP"], "c": 0,
                     "e": "WPA3 нуди најдобра заштита денес."},
                    {"q": "IoT (Smart) уредите се?", "o": ["Честа мета на напади", "100% безбедни"], "c": 0,
                     "e": "Имаат слаба вградена заштита."},
                    {"q": "Секогаш правиш Log out?", "o": ["Да, секогаш", "Не"], "c": 0,
                     "e": "Ја затвораш активната сесија за другите."},
                    {"q": "Проверуваш активни сесии на профил?", "o": ["Да, за упад", "Не"], "c": 0,
                     "e": "Види дали некој друг е најавен на твојот FB/Mail."},
                    {"q": "Шифрирање на хард диск?", "o": ["Максимална заштита", "Непотребно"], "c": 0,
                     "e": "Дури и да ти го украдат РС, нема да читаат податоци."},
                    {"q": "Учењето за дигитални закани е?", "o": ["Постојан процес", "Еднократно"], "c": 0,
                     "e": "Светот се менува, мора да бидеш во тек."}
                ]
            },
            'EN': {
                1: [  # 15 Questions for Level 2
                    {"q": "What does HTTPS do?", "o": ["Encrypts data", "Speeds up net"], "c": 0,
                     "e": "HTTPS is key for privacy."},
                    {"q": "A strong password has?", "o": ["Pet's name", "Letters and symbols"], "c": 1,
                     "e": "Complexity is protection."},
                    {"q": "What is 2FA?", "o": ["Second layer of security", "Screen type"], "c": 0,
                     "e": "Requires a mobile code."},
                    {"q": "Who should know your password?", "o": ["Only me", "Best friend"], "c": 0,
                     "e": "Passwords are personal secrets."},
                    {"q": "Public Wi-Fi is usually?", "o": ["Insecure", "The fastest"], "c": 0,
                     "e": "Data is not encrypted."},
                    {"q": "What do software updates fix?", "o": ["Security holes", "Icon colors"], "c": 0,
                     "e": "They patch hacker exploits."},
                    {"q": "Lock your screen when?", "o": ["Leaving the PC", "Only when sleeping"], "c": 0,
                     "e": "Never leave open access."},
                    {"q": "Is one password for all sites good?", "o": ["No, use different ones", "Yes, it's easier"],
                     "c": 0, "e": "Keeps other accounts safe."},
                    {"q": "Check a site name for?", "o": ["Typos", "Nice design"], "c": 0,
                     "e": "Fake sites use similar names."},
                    {"q": "Pop-up says 'virus found'. Action?", "o": ["Ignore/Close", "Click now"], "c": 0,
                     "e": "It's often a virus scam."},
                    {"q": "Length of a strong password?", "o": ["At least 12", "Max 6"], "c": 0,
                     "e": "Longer is harder to crack."},
                    {"q": "Is a cat's name a good password?", "o": ["No, it's weak", "Yes, it's great"], "c": 0,
                     "e": "Personal names are easy to guess."},
                    {"q": "Is HTTPS mandatory for payments?", "o": ["Yes, always", "No, not needed"], "c": 0,
                     "e": "HTTPS ensures safe payments."},
                    {"q": "What is more secure than a PIN?", "o": ["Biometrics", "Birthday"], "c": 0,
                     "e": "Fingerprints are unique to you."},
                    {"q": "Where to NEVER enter a password?", "o": ["On suspicious links", "Official sites"], "c": 0,
                     "e": "Keep data away from scammers."}
                ],
                2: [  # 25 Questions for Level 4
                    {"q": "What is Phishing?", "o": ["Fake message for data", "A sport"], "c": 0,
                     "e": "Scam to steal passwords."},
                    {"q": "Check what in the sender?", "o": ["Email address", "Picture"], "c": 0,
                     "e": "Names can be easily faked."},
                    {"q": "Does a bank ask for PIN via email?", "o": ["Never", "Often"], "c": 0,
                     "e": "Banks don't request secrets this way."},
                    {"q": "What does a VPN hide?", "o": ["IP address", "PC Name"], "c": 0,
                     "e": "VPN makes you anonymous to hackers."},
                    {"q": "Urgent 'act now' message is?", "o": ["Scam sign", "Always important"], "c": 0,
                     "e": "Hackers use fake urgency."},
                    {"q": "Open 'zip' from strangers?", "o": ["No, never", "Yes, if interesting"], "c": 0,
                     "e": "Can contain hidden Malware."},
                    {"q": "Smishing is Phishing via?", "o": ["SMS message", "Phone call"], "c": 0,
                     "e": "Text messages are a new target."},
                    {"q": "Links in Phishing emails are?", "o": ["Fake and dangerous", "Always correct"], "c": 0,
                     "e": "They lead to malicious pages."},
                    {"q": "Check what before logging in?", "o": ["URL address", "Ads"], "c": 0,
                     "e": "Verify the real domain."},
                    {"q": "Does antivirus help with Phishing?", "o": ["Yes, blocks some", "No, not at all"], "c": 0,
                     "e": "Modern programs detect scams."},
                    {"q": "Pay on a site without HTTPS?", "o": ["No, it's dangerous", "Yes, it's fine"], "c": 0,
                     "e": "Card data can be stolen."},
                    {"q": "Friend sends a weird link?", "o": ["Maybe hacked", "Trust them"], "c": 0,
                     "e": "Hackers use stolen profiles."},
                    {"q": "What is social engineering?", "o": ["Manipulating people", "Programming"], "c": 0,
                     "e": "Lying to get passwords."},
                    {"q": "Contest asks for ID number?", "o": ["Scam, run", "Fill it all"], "c": 0,
                     "e": "Personal data isn't for games."},
                    {"q": "Private Mode hides from hackers?", "o": ["No", "Yes"], "c": 0,
                     "e": "Only hides history on your PC."},
                    {"q": "What is Spear Phishing?", "o": ["Targeted attack", "Attack on everyone"], "c": 0,
                     "e": "A very precise and dangerous attack."},
                    {"q": "Reply to spam messages?", "o": ["No, delete them", "Yes, for fun"], "c": 0,
                     "e": "Confirms your email is active."},
                    {"q": "Where to store private photos?", "o": ["Secure/Encrypted", "Public cloud"], "c": 0,
                     "e": "Privacy must be a priority."},
                    {"q": "Mind what you post on socials?", "o": ["Yes, very much", "No, I post all"], "c": 0,
                     "e": "Posts reveal a lot about you."},
                    {"q": "Check app permissions?", "o": ["Yes, before install", "Never"], "c": 0,
                     "e": "Apps often ask for too much access."},
                    {"q": "Incognito mode is for?", "o": ["Public computers", "Home"], "c": 0,
                     "e": "Prevents others from seeing sessions."},
                    {"q": "Save passwords in public Chrome?", "o": ["No, never", "Yes"], "c": 0,
                     "e": "Next user can enter your profile."},
                    {"q": "Wi-Fi connects automatically. Risk?", "o": ["Risky", "Great"], "c": 0,
                     "e": "Could be a hacker's network."},
                    {"q": "Charge phone at public USB?", "o": ["Avoid", "Always"], "c": 0,
                     "e": "Risk of Juice Jacking data theft."},
                    {"q": "Read the privacy policy?", "o": ["I should know it", "It's boring"], "c": 0,
                     "e": "It says who uses your data."}
                ],
                3: [  # 30 Questions for Level 6
                    {"q": "What is Ransomware?", "o": ["Extortion virus", "A gift"], "c": 0,
                     "e": "Locks files for money."},
                    {"q": "Backup helps with Ransomware?", "o": ["Yes, restores files", "No"], "c": 0,
                     "e": "Backup is the only salvation."},
                    {"q": "Malware stands for?", "o": ["Harmful software", "Good software"], "c": 0,
                     "e": "Any program that does harm."},
                    {"q": "Is Cloud Backup safe?", "o": ["Yes, on servers", "No"], "c": 0,
                     "e": "Data is stored off your device."},
                    {"q": "What does a Password Manager do?", "o": ["Stores keys safely", "Steals them"], "c": 0,
                     "e": "Best way to manage passwords."},
                    {"q": "A Trojan horse is?", "o": ["Disguised virus", "A game"], "c": 0,
                     "e": "Looks useful but is dangerous."},
                    {"q": "Keylogger records what?", "o": ["Everything you type", "Pictures"], "c": 0,
                     "e": "Steals keys as you enter them."},
                    {"q": "Scan USB before use?", "o": ["Yes, mandatory", "No"], "c": 0,
                     "e": "USB is a top Malware carrier."},
                    {"q": "A Rootkit gives a hacker?", "o": ["Full control", "Nothing"], "c": 0,
                     "e": "Hardest virus to detect."},
                    {"q": "Is updated Windows better?", "o": ["Harder to hack", "Slower"], "c": 0,
                     "e": "Security patches are vital."},
                    {"q": "What does Spyware do?", "o": ["Tracks you secretly", "Protects you"], "c": 0,
                     "e": "Sends activity to hackers."},
                    {"q": "Adware is used for?", "o": ["Annoying ads", "Games"], "c": 0,
                     "e": "Can redirect to dangerous sites."},
                    {"q": "Does a Worm spread?", "o": ["Automatically on net", "Only by click"], "c": 0,
                     "e": "No human help needed to spread."},
                    {"q": "Encryption makes files?", "o": ["Unreadable to others", "Smaller"], "c": 0,
                     "e": "Only you with the key can open."},
                    {"q": "Weakest link in security?", "o": ["Humans", "Computers"], "c": 0,
                     "e": "People are easiest to manipulate."},
                    {"q": "What is a Zero-day attack?", "o": ["Unknown threat", "Old virus"], "c": 0,
                     "e": "An attack with no current cure."},
                    {"q": "What is a Firewall?", "o": ["Traffic filter", "Type of AV"], "c": 0,
                     "e": "Decides what enters the network."},
                    {"q": "DDoS attack makes a site?", "o": ["Unavailable", "Faster"], "c": 0,
                     "e": "Overloads it with fake requests."},
                    {"q": "A Botnet is a network of?", "o": ["Infected devices", "Smart people"], "c": 0,
                     "e": "Hacker uses them for mass attacks."},
                    {"q": "What is Sandboxing?", "o": ["Safe test zone", "A game"], "c": 0,
                     "e": "Isolates a virus from spreading."},
                    {"q": "Digital Signature guarantees?", "o": ["Originality", "Color"], "c": 0,
                     "e": "Confirms document wasn't changed."},
                    {"q": "Industrial espionage uses?", "o": ["Malware", "Phones"], "c": 0,
                     "e": "Stealing secrets from companies."},
                    {"q": "Turn off AV for install?", "o": ["Never", "Yes"], "c": 0,
                     "e": "Pirated software infects this way."},
                    {"q": "Strong router password is?", "o": ["Mandatory", "Unimportant"], "c": 0,
                     "e": "Stops neighbors and hackers."},
                    {"q": "Newest and safest Wi-Fi?", "o": ["WPA3", "WEP"], "c": 0,
                     "e": "WPA3 offers best current protection."},
                    {"q": "IoT (Smart) devices are?", "o": ["Frequent targets", "100% safe"], "c": 0,
                     "e": "They have weak built-in security."},
                    {"q": "Always Log out?", "o": ["Yes, always", "No"], "c": 0, "e": "Closes the session for others."},
                    {"q": "Check active sessions?", "o": ["Yes, for intrusion", "No"], "c": 0,
                     "e": "See if others are in your FB/Mail."},
                    {"q": "Hard drive encryption?", "o": ["Max protection", "Unneeded"], "c": 0,
                     "e": "Stops data theft even if PC is stolen."},
                    {"q": "Learning digital security is?", "o": ["Ongoing process", "One-time"], "c": 0,
                     "e": "World changes, stay updated."}
                ]
            },
            'AL': {
                1: [  # 15 Pyetje për Nivelin 2
                    {"q": "Çfarë bën HTTPS?", "o": ["Kodon të dhënat", "Përshpejton netin"], "c": 0,
                     "e": "HTTPS është kyç për privatësinë."},
                    {"q": "Fjalëkalimi i fortë ka?", "o": ["Emrin e maces", "Shkronja dhe simbole"], "c": 1,
                     "e": "Kompleksiteti është mbrojtje."},
                    {"q": "Çfarë është 2FA?", "o": ["Shtresë e dytë sigurie", "Lloj ekrani"], "c": 0,
                     "e": "Kërkon një kod celular."},
                    {"q": "Kush duhet ta dijë kodin tuaj?", "o": ["Vetëm unë", "Shoku i ngushtë"], "c": 0,
                     "e": "Kodet janë sekrete personale."},
                    {"q": "Wi-Fi publik është zakonisht?", "o": ["I pasigurt", "Më i shpejti"], "c": 0,
                     "e": "Të dhënat nuk kodohen."},
                    {"q": "Çfarë rregullojnë update-et?", "o": ["Vrimat e sigurisë", "Ngjyrat"], "c": 0,
                     "e": "Mbyllin rrugët për hakerët."},
                    {"q": "Blloko ekranin kur?", "o": ["Largohesh nga PC", "Vetëm kur fle"], "c": 0,
                     "e": "Mos lejo qasje të hapur."},
                    {"q": "Një kod për të gjitha faqet?", "o": ["Jo, përdor të ndryshëm", "Po, është më lehtë"], "c": 0,
                     "e": "Mbron llogaritë e tjera."},
                    {"q": "Kontrollo emrin e faqes për?", "o": ["Gabime shtypi", "Dizajn të bukur"], "c": 0,
                     "e": "Faqet false kanë emra të ngjashëm."},
                    {"q": "Pop-up thotë 'ke virus'. Veprimi?", "o": ["Injoroje/Mbylle", "Kliko tani"], "c": 0,
                     "e": "Shpesh është mashtrim virusi."},
                    {"q": "Gjatësia e një kodi të fortë?", "o": ["Të paktën 12", "Maksimum 6"], "c": 0,
                     "e": "Më i gjatë = më i vështirë."},
                    {"q": "Emri i maces është kod i mirë?", "o": ["Jo, është i dobët", "Po, është super"], "c": 0,
                     "e": "Emrat personalë gjehen lehtë."},
                    {"q": "A është HTTPS detyrim për pagesa?", "o": ["Po, gjithmonë", "Jo, s'duhet"], "c": 0,
                     "e": "HTTPS garanton pagesa të sigurta."},
                    {"q": "Çfarë është më e sigurt se PIN-i?", "o": ["Biometrika", "Ditëlindja"], "c": 0,
                     "e": "Shenjat e gishtave janë unike."},
                    {"q": "Ku mos vendosni KURRË fjalëkalim?", "o": ["Në linqe të dyshimta", "Në faqe zyrtare"], "c": 0,
                     "e": "Ruani të dhënat nga mashtruesit."}
                ],
                2: [  # 25 Pyetje për Nivelin 4
                    {"q": "Çfarë është Phishing?", "o": ["Mesazh i rremë", "Sport"], "c": 0,
                     "e": "Mashtrim për vjedhje kodesh."},
                    {"q": "Çfarë kontrollon te dërguesi?", "o": ["Adresën email", "Foton"], "c": 0,
                     "e": "Emrat mund të falsifikohen lehtë."},
                    {"q": "Banka kërkon PIN me email?", "o": ["Asnjëherë", "Shpesh"], "c": 0,
                     "e": "Bankat nuk kërkojnë sekrete kështu."},
                    {"q": "Çfarë fsheh VPN-ja?", "o": ["Adresën IP", "Emrin e PC-së"], "c": 0,
                     "e": "VPN ju bën anonim për hakerët."},
                    {"q": "Mesazhi 'vepro tani' është?", "o": ["Shenjë mashtrimi", "Gjithmonë me rëndësi"], "c": 0,
                     "e": "Hakerët përdorin urgjencë false."},
                    {"q": "Hap 'zip' nga të panjohur?", "o": ["Jo, asnjëherë", "Po, po qe interesant"], "c": 0,
                     "e": "Mund të ketë Malware të fshehur."},
                    {"q": "Smishing është Phishing me?", "o": ["Mesazh SMS", "Telefonatë"], "c": 0,
                     "e": "SMS-të janë shënjestra e re."},
                    {"q": "Linqet në emailat Phishing janë?", "o": ["Të rremë dhe rrezik", "Gjithmonë saktë"], "c": 0,
                     "e": "Ju dërgojnë në faqe dashakeqe."},
                    {"q": "Çfarë kontrollon para login-it?", "o": ["Adresën URL", "Reklamat"], "c": 0,
                     "e": "Verifikoni domenin e vërtetë."},
                    {"q": "Antivirusi ndihmon me Phishing?", "o": ["Po, bllokon disa", "Jo, aspak"], "c": 0,
                     "e": "Programet moderne zbulojnë mashtrime."},
                    {"q": "Paguaj në faqe pa HTTPS?", "o": ["Jo, rrezik", "Po, s'ka gjë"], "c": 0,
                     "e": "Të dhënat e kartës vidhen."},
                    {"q": "Miku dërgon një link të çuditshëm?", "o": ["Ndoshta i hakuar", "Besoja"], "c": 0,
                     "e": "Hakerët përdorin profile të vjedhura."},
                    {"q": "Inxhinieria sociale?", "o": ["Manipulim njerëzish", "Programim"], "c": 0,
                     "e": "Gënjeshtër për të marrë kodet."},
                    {"q": "Loja kërkon numrin e ID-së?", "o": ["Mashtrim, ik", "Plotesoje"], "c": 0,
                     "e": "Të dhënat personale s'janë lojë."},
                    {"q": "Private Mode fsheh nga hakerët?", "o": ["Jo", "Po"], "c": 0,
                     "e": "Vetëm fsheh historinë në PC-në tuaj."},
                    {"q": "Çfarë është Spear Phishing?", "o": ["Sulm i synuar", "Sulm ndaj të gjithëve"], "c": 0,
                     "e": "Sulm shumë preciz dhe i rrezikshëm."},
                    {"q": "Përgjigju mesazheve spam?", "o": ["Jo, fshiji", "Po, për qejf"], "c": 0,
                     "e": "Konfirmon që emaili është aktiv."},
                    {"q": "Ku ruhen fotot private?", "o": ["Vendi sigurt/koduar", "Cloud publik"], "c": 0,
                     "e": "Privatësia duhet prioritizuar."},
                    {"q": "Kujdes çfarë poston në rrjete?", "o": ["Po, shumë", "Jo, postoj gjithçka"], "c": 0,
                     "e": "Postimet zbulojnë shumë për ju."},
                    {"q": "Kontrollo lejet e aplikacioneve?", "o": ["Po, para instalimit", "Asnjëherë"], "c": 0,
                     "e": "Apps kërkojnë shumë qasje."},
                    {"q": "Incognito mode përdoret në?", "o": ["PC publike", "Shtëpi"], "c": 0,
                     "e": "Nuk lejon të tjerët të shohin sesionet."},
                    {"q": "Ruaj kodet në Chrome publik?", "o": ["Jo, asnjëherë", "Po"], "c": 0,
                     "e": "Tjetri mund të hyjë në profilin tuaj."},
                    {"q": "Wi-Fi lidhet vetë. Rrezik?", "o": ["I rrezikshëm", "Super"], "c": 0,
                     "e": "Mund të jetë rrjet hakerësh."},
                    {"q": "Kariko telin në USB publike?", "o": ["Shmange", "Gjithmonë"], "c": 0,
                     "e": "Rrezik vjedhjeje Juice Jacking."},
                    {"q": "Lexo politikën e privatësisë?", "o": ["Duhet ta dij", "Është e mërzitshme"], "c": 0,
                     "e": "Tregon kush përdor të dhënat tuaja."}
                ],
                3: [  # 30 Pyetje për Nivelin 6
                    {"q": "Çfarë është Ransomware?", "o": ["Virus shantazhi", "Dhuratë"], "c": 0,
                     "e": "Bllokon skedarët për para."},
                    {"q": "Backup ndihmon Ransomware?", "o": ["Po, kthen skedarët", "Jo"], "c": 0,
                     "e": "Backup është shpëtimi i vetëm."},
                    {"q": "Malware do të thotë?", "o": ["Softuer i dëmshëm", "Softuer i mirë"], "c": 0,
                     "e": "Çdo program që bën dëm."},
                    {"q": "Cloud Backup i sigurt?", "o": ["Po, në serverë", "Jo"], "c": 0,
                     "e": "Të dhënat ruhen jashtë pajisjes."},
                    {"q": "Çfarë bën Password Manager?", "o": ["Ruan kodet sigurt", "I vjedh"], "c": 0,
                     "e": "Mënyra më e mirë për kodet."},
                    {"q": "Kali i Trojës është?", "o": ["Virus i maskuar", "Lojë"], "c": 0,
                     "e": "Duket i dobishëm por është i keq."},
                    {"q": "Keylogger regjistron?", "o": ["Gjithçka që shkruan", "Foto"], "c": 0,
                     "e": "Vjedh kodet gjatë shkrimit."},
                    {"q": "Skano USB para përdorimit?", "o": ["Po, detyrim", "Jo"], "c": 0,
                     "e": "USB është bartësi kryesor i Malware."},
                    {"q": "Rootkit i jep hakerit?", "o": ["Kontroll të plotë", "Asgjë"], "c": 0,
                     "e": "Virusi më i vështirë për t'u gjetur."},
                    {"q": "Windows i përditësuar?", "o": ["Më i vështirë hakuar", "Më i ngadaltë"], "c": 0,
                     "e": "Pjesët e sigurisë janë jetike."},
                    {"q": "Çfarë bën Spyware?", "o": ["Të ndjek fshehurazi", "Të mbron"], "c": 0,
                     "e": "Dërgon aktivitetin te hakerët."},
                    {"q": "Adware shërben për?", "o": ["Reklama bezdisshme", "Lojëra"], "c": 0,
                     "e": "Mund të të çojë në faqe rrezik."},
                    {"q": "A shpërndahet Worm-i?", "o": ["Vetvetiu në rrjet", "Vetëm me klik"], "c": 0,
                     "e": "Nuk duhet ndihmë njeriu."},
                    {"q": "Enkriptimi i bën skedarët?", "o": ["Të palexueshëm", "Më të vegj"], "c": 0,
                     "e": "Vetëm ju me çelës i shihni."},
                    {"q": "Lidhja më e dobët?", "o": ["Njerëzit", "Kompjuterët"], "c": 0,
                     "e": "Njerëzit manipulohen më lehtë."},
                    {"q": "Zero-day attack është?", "o": ["Rrezik i panjohur", "Virus i vjetër"], "c": 0,
                     "e": "Sulm pa ilaç momental."},
                    {"q": "Çfarë është Firewall?", "o": ["Filtër trafiku", "Lloj AV"], "c": 0,
                     "e": "Vendos kush hyn në rrjet."},
                    {"q": "Sulmi DDoS e bën faqen?", "o": ["Të paqasshme", "Më të shpejtë"], "c": 0,
                     "e": "E mbingarkon me kërkesa false."},
                    {"q": "Botnet është rrjet me?", "o": ["Pajisje të infektuara", "Njerëz smart"], "c": 0,
                     "e": "Përdoret për sulme masive."},
                    {"q": "Sandboxing është?", "o": ["Zonë prove sigurt", "Lojë"], "c": 0,
                     "e": "Izolon virusin mos hapet."},
                    {"q": "Digital Signature garanton?", "o": ["Origjinalitetin", "Ngjyrën"], "c": 0,
                     "e": "Konfirmon që skedari s'ka ndryshuar."},
                    {"q": "Spiunazhi industrial?", "o": ["Malware", "Celularë"], "c": 0,
                     "e": "Vjedhje sekretesh nga firmat."},
                    {"q": "Fik AV për instalim?", "o": ["Asnjëherë", "Po"], "c": 0,
                     "e": "Programet pirate infektojnë kështu."},
                    {"q": "Kodi i router-it duhet?", "o": ["I fortë", "S'ka rëndësi"], "c": 0,
                     "e": "Ndalon fqinjët dhe hakerët."},
                    {"q": "Wi-Fi më i ri?", "o": ["WPA3", "WEP"], "c": 0, "e": "WPA3 ofron mbrojtjen më të mirë."},
                    {"q": "Pajisjet IoT janë?", "o": ["Shpesh shënjestra", "100% sigurt"], "c": 0,
                     "e": "Kanë siguri të dobët të brendshme."},
                    {"q": "Bëj gjithmonë Log out?", "o": ["Po, gjithmonë", "Jo"], "c": 0,
                     "e": "Mbyll sesionin për të tjerët."},
                    {"q": "Kontrollo active sessions?", "o": ["Po, për hyrje", "Jo"], "c": 0,
                     "e": "Shih nëse dikush hyri në FB/Email."},
                    {"q": "Hard drive encryption?", "o": ["Mbrojtje maksimale", "E kotë"], "c": 0,
                     "e": "Ndalon vjedhjen edhe po u mor PC-ja."},
                    {"q": "Mësimi për sigurinë është?", "o": ["Proces i vazhdueshëm", "Një herë"], "c": 0,
                     "e": "Bota ndryshon, mbetu i informuar."}
                ]
            },
            'TR': {
                1: [  # Seviye 2 için 15 Soru
                    {"q": "HTTPS ne yapar?", "o": ["Veriyi şifreler", "Neti hızlandırır"], "c": 0,
                     "e": "HTTPS gizlilik için anahtardır."},
                    {"q": "Güçlü şifrede ne olur?", "o": ["Evcil hayvan adı", "Harf ve semboller"], "c": 1,
                     "e": "Karmaşıklık korumadır."},
                    {"q": "2FA nedir?", "o": ["İkinci güvenlik katmanı", "Ekran türü"], "c": 0,
                     "e": "Mobil kod gerektirir."},
                    {"q": "Şifrenizi kim bilmeli?", "o": ["Sadece ben", "En iyi arkadaş"], "c": 0,
                     "e": "Şifreler kişisel sırdır."},
                    {"q": "Genel Wi-Fi nasıldır?", "o": ["Güvensiz", "En hızlı"], "c": 0, "e": "Veriler şifrelenmez."},
                    {"q": "Güncellemeler neyi çözer?", "o": ["Güvenlik açıkları", "Renkleri"], "c": 0,
                     "e": "Hacker yollarını kapatır."},
                    {"q": "Ekranı ne zaman kitle?", "o": ["PC'den ayrılınca", "Sadece uyurken"], "c": 0,
                     "e": "Açık erişim bırakmayın."},
                    {"q": "Tek şifre her yer için iyi mi?", "o": ["Hayır, farklı kullan", "Evet, kolay olur"], "c": 0,
                     "e": "Diğer hesapları korur."},
                    {"q": "Site adında neye bakılır?", "o": ["Yazım hataları", "Tasarım"], "c": 0,
                     "e": "Sahte siteler benzer ad kullanır."},
                    {"q": "Pop-up 'virüs' diyor. Eylem?", "o": ["Yoksay/Kapat", "Hemen tıkla"], "c": 0,
                     "e": "Genelde virüs tuzağıdır."},
                    {"q": "Güçlü şifre uzunluğu?", "o": ["En az 12", "Maks 6"], "c": 0,
                     "e": "Uzun olanın kırılması zordur."},
                    {"q": "Kedi adı iyi şifre mi?", "o": ["Hayır, zayıf", "Evet, harika"], "c": 0,
                     "e": "Kişisel adlar kolay tahmin edilir."},
                    {"q": "Ödeme için HTTPS şart mı?", "o": ["Evet, her zaman", "Hayır, gerekmez"], "c": 0,
                     "e": "HTTPS güvenli ödeme sağlar."},
                    {"q": "PIN'den daha güvenli olan?", "o": ["Biyometri", "Doğum günü"], "c": 0,
                     "e": "Parmak izi size özeldir."},
                    {"q": "Şifreyi nereye girmemeli?", "o": ["Şüpheli linklere", "Resmi sitelere"], "c": 0,
                     "e": "Verileri dolandırıcılardan koru."}
                ],
                2: [  # Seviye 4 için 25 Soru
                    {"q": "Phishing nedir?", "o": ["Sahte mesaj tuzağı", "Spor"], "c": 0,
                     "e": "Şifre çalma dolandırıcılığı."},
                    {"q": "Gönderende neye bakılır?", "o": ["E-posta adresi", "Resim"], "c": 0,
                     "e": "İsimler kolayca sahtelenebilir."},
                    {"q": "Banka e-postayla PIN ister mi?", "o": ["Asla", "Sıkça"], "c": 0,
                     "e": "Bankalar sırları böyle istemez."},
                    {"q": "VPN neyi gizler?", "o": ["IP adresi", "PC Adı"], "c": 0,
                     "e": "VPN sizi hackerlara anonim yapar."},
                    {"q": "Acil 'şimdi yap' mesajı?", "o": ["Tuzak belirtisi", "Hep önemli"], "c": 0,
                     "e": "Hackerlar sahte aciliyet kullanır."},
                    {"q": "Yabancıdan 'zip' açılır mı?", "o": ["Hayır, asla", "Evet, ilginçse"], "c": 0,
                     "e": "Gizli Malware içerebilir."},
                    {"q": "Smishing nedir?", "o": ["SMS ile Phishing", "Telefon araması"], "c": 0,
                     "e": "SMS'ler yeni hedef."},
                    {"q": "Phishing linkleri nasıldır?", "o": ["Sahte ve tehlikeli", "Hep doğru"], "c": 0,
                     "e": "Zararlı sayfalara götürür."},
                    {"q": "Girişten önce neye bakılır?", "o": ["URL adresi", "Reklamlar"], "c": 0,
                     "e": "Gerçek alanı doğrulayın."},
                    {"q": "Antivirüs Phishing'i engeller mi?", "o": ["Evet, bazılarını", "Hayır, asla"], "c": 0,
                     "e": "Modern programlar tuzakları anlar."},
                    {"q": "HTTPS'siz sitede ödeme?", "o": ["Hayır, tehlikeli", "Evet, sorun yok"], "c": 0,
                     "e": "Kart verileri çalınabilir."},
                    {"q": "Arkadaş garip link attı?", "o": ["Hacklenmiş olabilir", "Güven"], "c": 0,
                     "e": "Çalınmış profiller kullanılır."},
                    {"q": "Sosyal mühendislik nedir?", "o": ["İnsan manipülasyonu", "Programlama"], "c": 0,
                     "e": "Yalanla şifre alma."},
                    {"q": "Çekiliş T.C. no istiyor?", "o": ["Tuzak, kaç", "Hepsini doldur"], "c": 0,
                     "e": "Kişisel veriler oyun değildir."},
                    {"q": "Gizli Mod hackerlardan korur mu?", "o": ["Hayır", "Evet"], "c": 0,
                     "e": "Sadece PC'de geçmişi gizler."},
                    {"q": "Spear Phishing nedir?", "o": ["Hedefli saldırı", "Genel saldırı"], "c": 0,
                     "e": "Çok hassas ve tehlikeli bir saldırı."},
                    {"q": "Spam mesajlara cevap verilir mi?", "o": ["Hayır, sil", "Evet, eğlenceye"], "c": 0,
                     "e": "E-postanın aktif olduğunu onaylar."},
                    {"q": "Özel fotolar nerede saklanır?", "o": ["Güvenli/Şifreli", "Genel bulut"], "c": 0,
                     "e": "Gizlilik öncelik olmalı."},
                    {"q": "Sosyal medya paylaşımları?", "o": ["Dikkat edilmeli", "Her şeyi atarım"], "c": 0,
                     "e": "Paylaşımlar sizin hakkınızda çok şey söyler."},
                    {"q": "Uygulama izinleri?", "o": ["Yüklemeden önce bak", "Asla bakmam"], "c": 0,
                     "e": "Aplikasyonlar çok erişim ister."},
                    {"q": "Gizli mod nerede kullanılır?", "o": ["Genel PC'lerde", "Evde"], "c": 0,
                     "e": "Başkalarının oturumu görmesini engeller."},
                    {"q": "Genel Chrome'da şifre kaydet?", "o": ["Hayır, asla", "Evet"], "c": 0,
                     "e": "Sonraki kullanıcı profilinize girebilir."},
                    {"q": "Wi-Fi kendiliğinden bağlandı?", "o": ["Riskli", "Harika"], "c": 0,
                     "e": "Hacker ağı olabilir."},
                    {"q": "Genel USB'de şarj et?", "o": ["Kaçınırım", "Her zaman"], "c": 0,
                     "e": "Juice Jacking veri hırsızlığı riski."},
                    {"q": "Gizlilik politikasını oku?", "o": ["Bilmem gerekir", "Sıkıcı"], "c": 0,
                     "e": "Verileri kimin kullandığını yazar."}
                ],
                3: [  # Seviye 6 için 30 Soru
                    {"q": "Ransomware nedir?", "o": ["Fidye virüsü", "Hediye"], "c": 0,
                     "e": "Dosyaları para için kilitler."},
                    {"q": "Backup fidye için çözüm mü?", "o": ["Evet, veriyi kurtarır", "Hayır"], "c": 0,
                     "e": "Yedekleme tek kurtuluştur."},
                    {"q": "Malware neyin kısaltması?", "o": ["Zararlı yazılım", "İyi yazılım"], "c": 0,
                     "e": "Zarar veren her program."},
                    {"q": "Bulut yedekleme güvenli mi?", "o": ["Evet, sunucularda", "Hayır"], "c": 0,
                     "e": "Veri cihaz dışında saklanır."},
                    {"q": "Şifre Yöneticisi ne yapar?", "o": ["Şifreleri saklar", "Onları çalar"], "c": 0,
                     "e": "Şifre yönetimi için en iyi yol."},
                    {"q": "Truva Atı (Trojan) nedir?", "o": ["Maskeli virüs", "Oyun"], "c": 0,
                     "e": "Faydalı görünür ama kötüdür."},
                    {"q": "Keylogger neyi kaydeder?", "o": ["Yazılan her şeyi", "Resimleri"], "c": 0,
                     "e": "Yazarken şifreleri çalar."},
                    {"q": "USB'yi taratmalı mı?", "o": ["Evet, şart", "Hayır"], "c": 0,
                     "e": "USB en büyük Malware taşıyıcısıdır."},
                    {"q": "Rootkit hacker'a ne verir?", "o": ["Tam kontrol", "Hiçbir şey"], "c": 0,
                     "e": "Tespit edilmesi en zor virüstür."},
                    {"q": "Güncel Windows iyi mi?", "o": ["Zor hacklenir", "Yavaştır"], "c": 0,
                     "e": "Güvenlik yamaları hayatidir."},
                    {"q": "Spyware ne yapar?", "o": ["Gizlice izler", "Korur"], "c": 0,
                     "e": "Hackerlara etkinliklerinizi atar."},
                    {"q": "Adware ne için kullanılır?", "o": ["Sinir bozucu reklam", "Oyun"], "c": 0,
                     "e": "Tehlikeli sitelere yönlendirebilir."},
                    {"q": "Solucan (Worm) yayılır mı?", "o": ["Net üzerinden kendi", "Sadece tıkla"], "c": 0,
                     "e": "Yayılmak için insan yardımı gerekmez."},
                    {"q": "Şifreleme dosyaları ne yapar?", "o": ["Okunamaz hale getirir", "Küçültür"], "c": 0,
                     "e": "Sadece anahtarı olan açabilir."},
                    {"q": "En zayıf halka?", "o": ["İnsanlar", "Bilgisayarlar"], "c": 0,
                     "e": "İnsanlar manipülasyona açıktır."},
                    {"q": "Zero-day saldırısı nedir?", "o": ["Bilinmeyen tehdit", "Eski virüs"], "c": 0,
                     "e": "Henüz çözümü olmayan saldırı."},
                    {"q": "Güvenlik Duvarı nedir?", "o": ["Trafik filtresi", "AV türü"], "c": 0,
                     "e": "Ağa kimin gireceğine karar verir."},
                    {"q": "DDoS saldırısı siteyi ne yapar?", "o": ["Erişilemez", "Daha hızlı"], "c": 0,
                     "e": "Sahte isteklerle aşırı yükler."},
                    {"q": "Botnet nedir?", "o": ["Zombi cihaz ağı", "Zeki insanlar"], "c": 0,
                     "e": "Kitlesel saldırılar için kullanılır."},
                    {"q": "Sandboxing nedir?", "o": ["Güvenli test alanı", "Oyun"], "c": 0,
                     "e": "Virüsün yayılmasını izole eder."},
                    {"q": "Dijital İmza neyi garanti eder?", "o": ["Orijinallik", "Renk"], "c": 0,
                     "e": "Belgenin değişmediğini kanıtlar."},
                    {"q": "Endüstriyel casusluk?", "o": ["Malware", "Telefon"], "c": 0,
                     "e": "Şirket sırlarını çalmak."},
                    {"q": "Kurulumda AV kapatılır mı?", "o": ["Asla", "Evet"], "c": 0,
                     "e": "Korsan yazılımlar böyle bulaşır."},
                    {"q": "Router şifresi nasıl olmalı?", "o": ["Güçlü", "Önemsiz"], "c": 0,
                     "e": "Komşuları ve hackerları durdurur."},
                    {"q": "En yeni Wi-Fi standardı?", "o": ["WPA3", "WEP"], "c": 0,
                     "e": "WPA3 en iyi güncel korumayı sunar."},
                    {"q": "IoT cihazları nasıldır?", "o": ["Sık hedeflerdir", "%100 güvenli"], "c": 0,
                     "e": "Dahili güvenlikleri zayıftır."},
                    {"q": "Her zaman çıkış (Log out) yap?", "o": ["Evet, her zaman", "Hayır"], "c": 0,
                     "e": "Oturumu başkalarına kapatır."},
                    {"q": "Aktif oturumları kontrol et?", "o": ["Evet, sızma için", "Hayır"], "c": 0,
                     "e": "Başkası hesabınızda mı görün."},
                    {"q": "Disk şifreleme?", "o": ["Maks koruma", "Gereksiz"], "c": 0,
                     "e": "PC çalınsa bile veriyi korur."},
                    {"q": "Dijital güvenlik eğitimi?", "o": ["Sürekli süreç", "Bir seferlik"], "c": 0,
                     "e": "Dünya değişiyor, güncel kalın."}
                ]
            }

        }

    def load_for_level(self, level, collected_lessons=None):
        lang = self.settings.language or 'MK'
        q_idx = self.questions_map.get(level, 1)

        # Обиди се да вчиташ прашања за избраниот јазик
        full_pool = self.all_questions.get(lang, {}).get(q_idx, [])

        # Ако нема прашања за тој јазик, земи ги од Македонски како резерва (fallback)
        if not full_pool:
            full_pool = self.all_questions.get('MK', {}).get(q_idx, [])

        self.questions_pool = list(full_pool)
        random.shuffle(self.questions_pool)
        self.used_questions = []
        self.active = False
        self.correct_answers_count = 0

    def trigger_random(self):
        # Филтрирај ги само неупотребените прашања
        avail = [q for q in self.questions_pool if q not in self.used_questions]

        if not avail:
            # Ако сите се искористени, ресетирај ја листата
            self.used_questions = []
            avail = self.questions_pool

        if avail:
            self.current_q = random.choice(avail)
            self.used_questions.append(self.current_q)
            self.active = True
            self.showing_feedback = False

    # Во ui_manager.py во методот _check на класата QuizSystem:
    def _check(self, idx):
        self.correct = (idx == self.current_q["c"])
        if self.correct:
            self.correct_answers_count += 1
            # Секој точен одговор прави 10 штета (Вкупно 50 од квизот)
            self.settings.pending_boss_damage = 10
        else:
            self.settings.shields = max(0, self.settings.shields - 1)
        self.showing_feedback = True

    def draw(self):
        if not self.active: return

        # Позадински слој (overlay)
        ov = pygame.Surface((900, 700), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 240))
        self.screen.blit(ov, (0, 0))

        font = pygame.font.Font(self.settings.font_path, 16)
        # Главен панел за квизот
        pygame.draw.rect(self.screen, (255, 255, 255), (100, 150, 700, 420), border_radius=15)

        # 1. ДИНАМИЧНИ ПРЕВОДИ
        lang = self.settings.language or 'MK'

        # Преводи за прогрес барот (ТОЧНИ: 0/5)
        correct_labels = {
            'MK': "ТОЧНИ", 'EN': "CORRECT", 'AL': "TË SAKTA", 'TR': "DOĞRU"
        }

        # Преводи за "ИНФО:"
        info_labels = {
            'MK': "ИНФО:", 'EN': "INFO:", 'AL': "INFO:", 'TR': "BİLGİ:"
        }

        # Преводи за статус (ТОЧНО/ГРЕШНО)
        status_labels = {
            'MK': ("ТОЧНО!", "ГРЕШНО!"),
            'EN': ("CORRECT!", "WRONG!"),
            'AL': ("E SAKTË!", "GABIM!"),
            'TR': ("DOĞRU!", "YANLIŞ!")
        }

        label = correct_labels.get(lang, "CORRECT")
        info_text = info_labels.get(lang, "INFO:")
        correct_status, wrong_status = status_labels.get(lang, ("CORRECT!", "WRONG!"))

        # Приказ на прогресот во горниот лев агол на панелот
        limit = 5 if self.settings.current_level == 2 else 10 if self.settings.current_level == 4 else 15
        prog = f"{label}: {self.correct_answers_count}/{limit}"
        self.screen.blit(font.render(prog, True, (0, 0, 150)), (130, 170))

        # 2. ПРИКАЗ НА ПРАШАЊА ИЛИ ФИДБЕК
        if not self.showing_feedback:
            # Цртање на прашањето
            draw_text_wrapped(self.screen, self.current_q["q"], 130, 210, 640, font, (0, 0, 0))

            # Цртање на опциите (копчињата)
            for i, opt in enumerate(self.current_q["o"]):
                r = pygame.Rect(130, 320 + i * 80, 640, 60)
                pygame.draw.rect(self.screen, (100, 150, 255), r, border_radius=10)
                self.screen.blit(font.render(f"{i + 1}. {opt}", True, (255, 255, 255)), (150, 335 + i * 80))
        else:
            # Цртање на фидбекот по одговорено прашање
            if self.correct:
                display_status = correct_status
                color = (0, 150, 0)  # Зелена за точно
            else:
                display_status = wrong_status
                color = (200, 0, 0)  # Црвена за грешно

            # Статус (ТОЧНО! / ГРЕШНО!)
            self.screen.blit(font.render(display_status, True, color), (130, 210))

            # Наслов "ИНФО:"
            self.screen.blit(font.render(info_text, True, (0, 0, 0)), (130, 250))

            # Објаснување на лекцијата
            draw_text_wrapped(self.screen, self.current_q["e"], 130, 290, 640, font, (30, 30, 30))

            # Инструкција за продолжување на дното
            cont = self.settings.translations[lang]['press_space']
            self.screen.blit(font.render(cont, True, (150, 0, 0)), (130, 520))

    def handle_event(self, event):
        if not self.active: return
        if self.showing_feedback and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.active = False
        elif not self.showing_feedback and event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(self.current_q.get("o", []))):
                if pygame.Rect(130, 320 + i * 80, 640, 60).collidepoint(event.pos): self._check(i)


def draw_text_wrapped(screen, text, x, y, max_w, font, color):
    words = text.split(' ');
    line = "";
    curr_y = y
    for word in words:
        if font.size(line + word)[0] < max_w:
            line += word + " "
        else:
            screen.blit(font.render(line, True, color), (x, curr_y))
            curr_y += font.get_linesize() + 5
            line = word + " "
    screen.blit(font.render(line, True, color), (x, curr_y))
    return curr_y


class Boss(pygame.sprite.Sprite):
    def __init__(self, settings, level=1):
        super().__init__()
        self.settings = settings
        self.level = level

        # ДЕФИНИРАЊЕ НА target_y (ова ја решава грешката)
        self.target_y = 80

        # Здравје според нивото
        self.max_hp = 100 if level == 2 else 200 if level == 4 else 300
        self.current_hp = self.max_hp
        self.t = 0.0

        try:
            img = pygame.image.load(os.path.join('assets', 'monster1.png')).convert_alpha()
            self.image = pygame.transform.scale(img, (180, 180))
        except:
            self.image = pygame.Surface((150, 150))
            self.image.fill((150, 0, 0))

        self.rect = self.image.get_rect(center=(450, -100))

    def update(self, player_x):
        # Прво се спушта до својата позиција (target_y)
        if self.rect.y < self.target_y:
            self.rect.y += 2
        else:
            # ДИНАМИЧНА БРЗИНА И ДВИЖЕЊЕ:
            # Ниво 2: 0.02
            # Ниво 4: 0.04
            # Ниво 6: 0.06
            speed_factor = 0.02 + (self.level - 2) * 0.01
            self.t += speed_factor

            # Амплитуда (замав)
            amplitude = 200 + (self.level * 10)

            # Синусоидно движење лево-десно
            self.rect.x = 360 + math.sin(self.t) * amplitude

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (50, 50, 50), (300, 20, 300, 15))
        pygame.draw.rect(screen, (255, 0, 0), (300, 20, (max(0, self.current_hp) / self.max_hp) * 300, 15))


def draw_knowledge_summary(screen, settings, knowledge_list):
    lang = settings.language or 'MK'
    overlay = pygame.Surface((900, 700), pygame.SRCALPHA);
    overlay.fill((0, 20, 60, 245));
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (30, 30, 840, 640), border_radius=15)
    pygame.draw.rect(screen, (255, 215, 0), (30, 30, 840, 640), width=5, border_radius=15)

    font_t = pygame.font.Font(settings.font_path, 18);
    font_s = pygame.font.Font(settings.font_path, 9)

    # ДИНАМИЧЕН ПРЕВОД НА НАСЛОВОТ
    summary_titles = {
        'MK': "РЕЗИМЕ НА ЗНАЕЊЕТО",
        'EN': "KNOWLEDGE SUMMARY",
        'AL': "PËRMBLEDHJA E NJOHURIVE",
        'TR': "BİLGİ ÖZETİ"
    }
    title_text = summary_titles.get(lang, summary_titles['EN'])

    # Цртање на насловот на средина
    title_surf = font_t.render(title_text, True, (0, 0, 100))
    screen.blit(title_surf, (450 - title_surf.get_width() // 2, 50))

    # Приказ во две колони (по 8 лекции во колона за читливост)
    for i, lesson in enumerate(knowledge_list):
        col = 0 if i < 8 else 1
        row = i % 8
        x = 65 if col == 0 else 465
        y_pos = 110 + row * 65

        # Маркер
        pygame.draw.circle(screen, (255, 140, 0), (x - 15, y_pos + 5), 4)
        draw_text_wrapped(screen, lesson, x, y_pos, 360, font_s, (30, 30, 30))

    # Превод за пораката на дното (Space)
    space_txt = settings.translations[lang]['press_space']
    screen.blit(font_s.render(space_txt, True, (200, 0, 0)), (450 - font_s.size(space_txt)[0] // 2, 645))


def draw_victory_screen(screen, settings):
    screen.fill((0, 40, 0));
    f = pygame.font.Font(settings.font_path, 20)
    msg = settings.translations[settings.language]['victory_msg']
    screen.blit(f.render(msg, True, (255, 255, 0)), (450 - f.size(msg)[0] // 2, 350))


def draw_level_complete(screen, settings):
    lang = settings.language or 'MK'
    # Го влече текстот "НИВО {} ЗАВРШЕНО! ОДИМЕ ПОНАТАМУ!"
    msg = settings.translations[lang].get('level_up', "LEVEL COMPLETE").format(settings.current_level)

    font = pygame.font.Font(settings.font_path, 22)
    txt_surf = font.render(msg, True, (0, 255, 0))  # Зелена боја

    # Се црта на средина на екранот
    screen.blit(txt_surf, (450 - txt_surf.get_width() // 2, 350))