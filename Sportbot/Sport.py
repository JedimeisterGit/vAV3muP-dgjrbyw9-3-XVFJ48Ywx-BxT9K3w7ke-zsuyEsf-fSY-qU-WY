"""
Made by JimmysNeutron
You may use the tool if you got my permission.
If you use it without permission you may ask for it or stop using the tool.
THIS TOOL DOES NOT COME WITH ANY WARRANTY OR WHAT SO EVER!
This software is not distributed with any license and thus it is not allowed
to edit, distribute, copy or use it!
"""
# This product uses the TMDb API but is not endorsed or certified by TMDb

# INFO --> STUFF FROM UPLOAD-HELPER
# NFO --> NFO STUFF


from webbot import Browser
import os, time, sys, requests, json, shutil, string, re, codecs

username = ''
userpassword = ''

def GeneratePost(title,cover,description,nfo,header,password):
    base =  """
            [CENTER]

            [COLOR=#ff0000][FONT=book antiqua][SIZE=5]%pgTitle%[/SIZE][/FONT][/COLOR]

            [IMG]%pgCover%[/IMG]

            [IMG]https://image.revenge-of-usenet.com/images/OTHER/beschreibung.png[/IMG]

            [SIZE=2][FONT=arial]%pgDescription%[/SIZE][/FONT]

            [CODE]%pgNFO%[/CODE]

            [HIDE]

            [COLOR=#ffa07a][SIZE=4]
            Es dauert etwas bis die Datein auf dem Indexer vorhanden sind![/SIZE][/COLOR]

        [IMG]https://image.revenge-of-usenet.com/images/OTHER/suchmaschinen.png[/IMG]

            [COLOR=#00ff00][SIZE=4]Header: %pgHeader%[/SIZE][/COLOR]
            [COLOR=#ff0000][SIZE=4]Passwort: %pgPassword%[/SIZE][/COLOR]

            [SIZE=3]

            [COLOR=#00ff00][URL="https://nzbindex.nl/?q=%pgHeader%&max=25&minage=&maxage=&hidespam=1&hidepassword=0&sort=agedesc&minsize=&maxsize=&complete=0&hidecross=0&hasNFO=0&poster="]NZBindex.nl[/URL] [/COLOR]
            [COLOR=#FF0000][URL="https://binsearch.info/?q=%pgHeader%&max=100&adv_age=1100&server="]Binsearch.info[/URL] [/COLOR]

            [COLOR=#ff0000]NZBlnk:[/COLOR] [B][URL="nzblnk://?t=%pgTitle%&h=%pgHeader%&p=%pgPassword%"]%pgTitle%[/URL][/B]

            [/SIZE]

            [SIZE=4][COLOR=#ffd700]NZB-Name: %pgTitle%{{%pgPassword%}}[/COLOR][/SIZE]

            [/HIDE]

            [/CENTER]

            [SIZE=1]Information might be by The Movie DB, OpenMovie DB or  The TV DB[/SIZE]
            """
    # Set values
    base = base.replace('%pgTitle%',title)
    base = base.replace('%pgCover%', cover)
    base = base.replace('%pgDescription%',description)
    base = base.replace('%pgNFO%', nfo)
    base = base.replace('%pgHeader%', header)
    base = base.replace('%pgPassword%', password)

    return base

def detect_encoding(path):
        with open(path, 'rb') as infile:
            s = infile.readline()

        if s.startswith(codecs.BOM_UTF16_BE):
            return 'utf-16-be'
        if s.startswith(codecs.BOM_UTF16_LE):
            return 'utf-16-le'
        if s.startswith(codecs.BOM_UTF32_BE):
            return 'utf-32-be'
        if s.startswith(codecs.BOM_UTF32_LE):
            return 'utf-32-le'
        if s.startswith(codecs.BOM_UTF8):
            return 'utf-8'

        # No encoding found -- what should the default be?
        return 'utf-8'

def LogintoRoU(username, userpassword, web):
    # Login
    web.go_to('https://revenge-of-usenet.online/board/portal.php')
    print('Opened Login Page')
    Wait()
    # put in the login data
    web.type(username, into="vb_login_username", id="vb_login_username")
    Wait()
    web.click(id="navbar_password_hint")
    web.type(userpassword) # enter password
    Wait()
    web.click(id='cb_cookieuser_navbar')    # Stay logged check mark
    Wait()
    web.click("Anmelden")
    Wait()
    print('Logged in')
    if IsPageWorking(web) == False:
        print('Website not loading correctly!')
        exit() 

def Wait():
    time.sleep(2)

def FixSpecialChars(original):
    # due to decoding some special chars are broken
    # Replace broken special chars
    return original.replace('ÃŸ','ß').replace('Ã¤', 'ä').replace('Ã¼','ü').replace('Ã¶','ö')

def IsPageWorking(web):
    pageSource = web.get_page_source()
    if 'Error 502' in pageSource:   # Bad Gateway
        return False
    if 'Error 504' in pageSource:   # Bad Timeout
        return False
    elif 'Error 520' in pageSource: # Web server is returning an unknown error
        return False
    elif 'Error 521' in pageSource: # Web server is down
        return False
    elif 'Error 522' in pageSource: # Connection timed out
        return False
    elif 'Error 525' in pageSource: # SSL handshake failed
        return False
    else:
        return True









# --------- MAIN ---------

while(True):
    print('Starting posting run')
    
    basePath = os.path.dirname(os.path.abspath(__file__))
    web = Browser(True)



    # Fetch config Data
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json'), 'r') as f:
        config = json.load(f)

        username = config['username']
        userpassword = config['password']


    # Check if fetching data worked
    if username == '' or userpassword == '':
        # Fetching failed
        print('Fetching config failed!')
        time.sleep(5)
        sys.exit(0)
    # Fetching worked
    print('Config data Fetched!')


    LogintoRoU(username, userpassword, web)
    del(userpassword)
    del(username)

    # Get amount of Files to post
    amount = 0
    amountDone = 1
    for dir in os.listdir(basePath):
        if not dir.endswith('.py') and not dir.endswith('.txt') and not dir.endswith('.json') and not dir.endswith('.cache') and not dir.endswith('.log'):
            amount += 1

    # Run Through all Folders in current directory
    for dir in os.listdir(basePath):
        if not dir.endswith('.py') and not dir.endswith('.txt') and not dir.endswith('.json') and not dir.endswith('.cache') and not dir.endswith('.log') :
            print('----------------------------')
            print('Posted ' + str(amountDone) + ' of ' + str(amount))
            print('Start posting ' + dir)

            if 'DIRFIX' in dir.upper():
                print('DIRFIX --> Ignore')
                continue

            title = ''
            cover = ''
            description = ''
            header = ''
            password = ''
            nfo = ''

            # Open subdir
            subdirPath = os.path.join(basePath,dir)
            for file in os.listdir(subdirPath):
                # Get Header, PW and Title
                if file.endswith('.txt'):
                    
                    filewithpath = ''
                    filewithpath = os.path.join(subdirPath, file)
                    codec = str(detect_encoding(filewithpath))  # Detect Encoding of textfile

                    with open(os.path.join(subdirPath, file), 'r', encoding=codec,errors='replace') as infoFile:
                        for line in infoFile.readlines():
                            if 'Titel' in line:
                                split = line.split(':')
                                title = split[1].strip()
                            if 'Header' in line:
                                split = line.split(':')
                                header = split[1].strip()
                            if 'Passwort' in line:
                                split = line.split(':')
                                password = split[1].strip()
                        readinfo = True
                
                # Get NFO
                if file.endswith('.nfo'):
                    
                    filewithpath = ''
                    filewithpath = os.path.join(subdirPath, file)
                    codec = str(detect_encoding(filewithpath)) # Detect Encoding of textfile

                    with open(os.path.join(subdirPath, file), 'r', encoding=codec,errors='replace') as nfoFile:
                        for line in nfoFile.readlines():
                            nfo += line


            # Check if Title, header or password is empty --> skip
            if title == '' or header == '' or password == '':
                print('Getting Title, Header or password failed')
                amountDone += 1
                continue
            
            title = title.replace('_', ' ').replace('.',' ').replace('-', ' - ')
            

            # Search for imDb-ID in NFO
            # example: tt8579674
            try:
                imdbId = re.search('(tt\d{5,8})', nfo).group()
            except Exception:
                # Gets called if no IMDB-ID was found
                imdbId = None            

            tempName = title.replace('.', ' ').upper()

            # Set images
            if 'FUSSBALL' in tempName or 'A-LEAGUE' or 'A - LEAGUE' in tempName or 'A LEAGUE' in tempName or 'FA CUP' in tempName or 'UEFA' in tempName or 'MATCH OF THE DAY' in tempName:
                cover = 'https://image.revenge-of-usenet.com/images/2020/08/07/16d77ff64af4ea46842d2f9a8ab91929.jpg'
            elif 'FORMEL 1' in tempName or 'FORMEL 2' in tempName or 'DTM' in tempName or 'FORMULA 3' or 'FORMULA E' in tempName or 'FORMULAE' in tempName or 'F1' in tempName or 'F2' in tempName or 'F3' in tempName or 'MOTOGP' in tempName or 'MOTO1' in tempName or 'MOTO2' in tempName or 'MOTO3' in tempName or 'MOTOE' in tempName or 'NASCAR' in tempName or 'FORMULA 1' in tempName or 'FORMULA 2' in tempName or 'FORMEL E' in tempName or 'FORMULA E' in tempName:
                cover = 'https://image.revenge-of-usenet.com/images/2020/08/07/e057cc8c97d5140faa2430901abb4607.jpg'
            elif 'WWE' in tempName or 'WCW' in tempName or 'AEW' in tempName or 'NJPW' in tempName:
                cover = 'https://image.revenge-of-usenet.com/images/2020/08/07/4888d2df1b01f2a4310022fc78cd4c61.png'
            elif 'FOOTBALL' in tempName or 'NFL' in tempName or 'XFL' in tempName or 'ROAD TO SUPER BOWL' in tempName or '':
                cover = 'https://image.revenge-of-usenet.com/images/2020/08/07/bb6d1b4bfbb0e650e6182e9a7c38801f.jpg'
            elif 'INVICTA' in tempName or 'BELLATOR' in tempName or 'UFC' in tempName:
                cover = 'https://image.revenge-of-usenet.com/images/2020/08/07/28819a995d400cb06dee538b33ada04f.jpg'
            else:
                cover = 'https://revenge-of-usenet.online/board/images/styles/TheBeaconDark/style_blue/logo.png'
     
            # Generate post
            print('Generating Post') 
            text = GeneratePost(title,cover,description,nfo,header,password)


            # Post on Forum
            if 'FUSSBALL' in tempName or 'A-LEAGUE' in tempName or 'A - LEAGUE' in tempName or 'A LEAGUE' in tempName or 'FA CUP' in tempName or 'UEFA' in tempName or 'MATCH OF THE DAY' in tempName:
                web.go_to('https://revenge-of-usenet.online/board/newthread.php?do=newthread&f=123')
            elif 'FORMEL 1' in tempName or 'FORMEL 2' in tempName or 'DTM' in tempName or 'FORMULA 3' or 'FORMULA E' in tempName or 'FORMULAE' in tempName or 'F1' in tempName or 'F2' in tempName or 'F3' in tempName or 'MOTOGP' in tempName or 'MOTO1' in tempName or 'MOTO2' in tempName or 'MOTO3' in tempName or 'MOTOE' in tempName or 'NASCAR' in tempName or 'FORMULA 1' in tempName or 'FORMULA 2' in tempName or 'FORMEL E' in tempName or 'FORMULA E' in tempName:
                web.go_to('https://revenge-of-usenet.online/board/newthread.php?do=newthread&f=124')
            elif 'WWE' in tempName or 'WCW' in tempName or 'AEW' in tempName or 'NJPW' in tempName:
                web.go_to('https://revenge-of-usenet.online/board/newthread.php?do=newthread&f=125')
            elif 'FOOTBALL' in tempName or 'NFL' in tempName or 'XFL' in tempName or 'ROAD TO SUPER BOWL' in tempName:
                web.go_to('https://revenge-of-usenet.online/board/newthread.php?do=newthread&f=126')
            elif 'INVICTA' in tempName or 'BELLATOR' in tempName or 'UFC' in tempName:
                web.go_to('https://revenge-of-usenet.online/board/newthread.php?do=newthread&f=130')
            else:
                web.go_to('https://revenge-of-usenet.online/board/newthread.php?do=newthread&f=127')

            if IsPageWorking(web) == False:
                print('Website not loading correctly!')
                exit() 

            Wait()
            web.scrolly(300)
            web.type(title.replace('_', ' ').replace('.',' ').replace('-', ' - '), into='subject', id='subject')   # Enter Title

            Wait()
            
            #Set correct image
            if '720' in tempName:
                web.click(id='pi_119')
            if '1080' in tempName:
                web.click(id='pi_120')
            if 'x265' in tempName:
                web.click(id='pi_165')
            else:
                web.click(id='pi_164')

                    
            # Create post
            Wait()
            print('Typing template')
            web.type(text,tag='textarea', id='cke_source cke_enable_context_menu')  # Enter Content
            web.click(text='Thema erstellen',id='vB_Editor_001_save')
            print(title + ' posted! \n\n\n')
            

            if IsPageWorking(web) == False:
                print('Website not loading correctly!')
                exit() 
            
            amountDone += 1

            # Delete folder
            shutil.rmtree(subdirPath)
            
    print('\n\n\n\n\n\nAll posted!\n\n\n\n\n\n')




    time.sleep(600)
