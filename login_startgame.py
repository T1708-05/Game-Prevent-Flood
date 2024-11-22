
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from database import UserDatabase
from game import *

# Constants and global variables
WINDOW_SIZE = (1300, 750)
class LoginMenu:

    def __init__(self, theme_idx = 0):
        self.running_menu = True

        self.surface = create_example_window('Prevent Flood', WINDOW_SIZE)
        icon = pygame.image.load('assets/LOGO UTE.png')
        pygame.display.set_icon(icon)

        self.sound = pygame_menu.sound.Sound()
        self.sound.load_example_sounds()
        self.sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, None)
        self.enabled_sound = True
        self.bgm_volume = 0.5
        self.theme_idx = theme_idx

        if theme_idx == 0:
            pygame.mixer.music.load('sound/bgm.mp3')
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)



    def init_login_menu(self):  #tao login_menu
        self.login_menu = pygame_menu.Menu(
            overflow=(False, False),
            height=WINDOW_SIZE[1],  # * 0.7,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=self.login_menu_theme,
            title='Login',
            center_content=False,
            width=WINDOW_SIZE[0],  # * 0.8
        )

        self.login_noti = self.login_menu.add.label('')
        usern_login = self.login_menu.add.text_input(
            title='                       ',
            maxchar=10,
            textinput_id='username',
            input_underline = '__',
            # input_underline_vmargin = 3,
            onchange = self.reset_noti_login)
        usern_login.set_margin(0, 60) 
        passw_login = self.login_menu.add.text_input(
            title='                       ',
            maxchar=17,
            textinput_id='password',
            input_underline = '__',
            # input_underline_vmargin = 1,
            password=True,
            onchange = self.reset_noti_login)
        self.login_menu.add.button('                 ', self.check_login).translate(170,30)
        self.login_menu.add.button('   Return to main menu  ', pygame_menu.events.BACK).translate(280,135)

    def init_register_menu(self):
        self.register_menu = pygame_menu.Menu(
            overflow=(False, False),
            height=WINDOW_SIZE[1],  # * 0.7,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=self.register_menu_theme,
            title='Register',
            center_content=False,
            width=WINDOW_SIZE[0]  # * 0.8
        )

        self.regis_noti = self.register_menu.add.label('')
        usern_regis = self.register_menu.add.text_input(
            title='                     ',
            maxchar=10,
            textinput_id='username',
            input_underline = '__',
            onchange = self.reset_noti_regis)
        passw_regis = self.register_menu.add.text_input(
            title='                     ',
            maxchar=17,
            textinput_id='password',
            input_underline = '__',
            password=True,
            onchange = self.reset_noti_regis)
        self.register_menu.add.button('    Register    ', self.check_register).translate(261,5)
        self.register_menu.add.button('   Return to main menu  ', pygame_menu.events.BACK).translate(375,135)

    def check_login(self):
        data = self.login_menu.get_input_data()
        #for k in data.keys():
            #print(f'\t{k}\t=>\t{data[k]}')

        DB = UserDatabase()
        if not DB.login_user(username = data['username'], password = data['password']):
            self.login_noti.set_title('Wrong username or password')
            print('wrongggggg')
        else:
            self.login_noti.set_title('Login DONE!')
            self.login_menu.force_surface_update()
            print('login successful')
            self.running_menu = False
            g = MenuGame(data['username'], data['password'], self.theme_idx)
            g.start(self.enabled_sound, self.sound)

    def check_register(self):
        data = self.register_menu.get_input_data()
        #for k in data.keys():
            #print(f'\t{k}\t=>\t{data[k]}')

        DB = UserDatabase()
        if DB.register_user(username = data['username'], password = data['password']):
            self.regis_noti.set_title('Register DONE!')
            print('register OK!')
            pygame.time.delay(1500)
            self.running_menu = False
            g = MenuGame(data['username'], data['password'])
            g.start()
        else:
            print('not register ok')
            self.regis_noti.set_title('Username already exists')

    def reset_noti_regis(self, a):
        self.regis_noti.set_title('')

    def reset_noti_login(self, a):
        self.login_noti.set_title('')
            
    def init_theme(self):
        asset= ['assets/']
        x = self.theme_idx
        b_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path=asset[x] + 'background.png',
            image_id='background')
       
        login_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path=asset[x]+ 'login.png',
            image_id='background')
            
        register_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path=asset[x]+'register.png',
            image_id='background')
        my_theme = pygame_menu.themes.Theme(
            background_color = b_img, 
            border_color = (0, 255, 0),
            border_width = 15,
            #cursor_color = (15, 15, 15),
            #focus_background_color = None,                          

            title = True,                                                 # có hay không title
            title_background_color = (249,72,82),                         # màu nền của title
            title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE, # style title bar
            title_close_button = True,                                    # nút thoát // quay lại
            title_close_button_background_color = (10, 10, 10),           # màu nút thoát // quay lại
            title_font = pygame_menu.font.FONT_COMIC_NEUE,                # font title
            title_font_antialias = True,                                  # khử răng cưa title font
            title_font_color = (255, 255, 255),                           # màu title
            title_font_shadow = True,                                     # bóng chữ title
            title_font_shadow_color = (0, 0, 0),                          # màu bóng chữ title

            # effect khi chọn
            widget_selection_effect = pygame_menu.widgets.LeftArrowSelection(
                arrow_size=(10, 15), arrow_right_margin=10, arrow_vertical_offset=0, blink_ms=0),

            widget_font = pygame_menu.font.FONT_COMIC_NEUE,               # font widget
            widget_font_antialias = True,                                 # font widget, khử răng cưa
            widget_font_color = (0, 0, 0),                                # màu chữ chưa được chọn
            selection_color = (249,16,23),                                # màu chữ được chọn
            widget_background_color = (249,72,82, 0),                     # màu nền widget
            widget_font_size = 30,                                        # size font widget                              
            widget_offset = (0, 0),                                       # x-axis and y-axis (x, y) offset
            widget_margin = (0, 25),                                      # khoảng cách của các ô
            widget_alignment = pygame_menu.locals.ALIGN_CENTER,           # căn giữa
            
            widget_box_arrow_color = (34, 24, 142),                       # màu mũi tên chọn hộp
            widget_box_border_width = 2,                                  # độ dày viền hộp chọn
            widget_box_border_color = (0, 0, 0),                          # màu viền hộp chọn
            widget_box_margin = (10, 0),                                  # vị trí hộp chọn
            widget_box_background_color = (255, 255, 255)                 # màu hộp chọn
        )

        self.main_menu_theme = my_theme.copy()
        self.main_menu_theme.background_color = b_img
        self.main_menu_theme.widget_offset = (0.01, 0.505) # need for main menu
        self.main_menu_theme.title_close_button = False
        self.main_menu_theme.selection_color=(249,16,23)

        self.login_menu_theme = my_theme.copy()
        self.login_menu_theme.background_color = login_img
        self.login_menu_theme.widget_offset = (0.515, 0.19)  
        self.login_menu_theme.title_close_button = True
        self.login_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        

        
        self.register_menu_theme = my_theme.copy()
        self.register_menu_theme.background_color = register_img
        self.register_menu_theme.widget_offset = (0.395, 0.28) 
        self.register_menu_theme.title_close_button = True
        self.register_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT


    def init_main_menu(self):
        self.main_menu = pygame_menu.Menu(
            overflow=(False, False),
            height=WINDOW_SIZE[1],  # * 0.7,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=self.main_menu_theme,
            title='Main menu',
            center_content=False,
            width=WINDOW_SIZE[0]  # * 0.8
        )

        Login_button = self.main_menu.add.button('Login', self.login_menu)
        
        Register_button = self.main_menu.add.button('Register', self.register_menu)
        
        Quit_button = self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

    def init_menu(self):
        self.init_login_menu()
        self.init_register_menu()
        self.init_main_menu()

    def start(self, enabled_sound = True, sound_engine = None):
        self.init_theme()
        self.init_menu()
        self.enabled_sound = enabled_sound

        if enabled_sound:
            if sound_engine != None:
                self.sound = sound_engine
            self.main_menu.set_sound(self.sound, recursive = True)
        else:
            self.main_menu.set_sound(None, recursive = True)

        self.running_menu = True
        while self.running_menu:

            # Main menu
            self.main_menu.mainloop(self.surface)

            # Flip surface
            pygame.display.flip()

class MenuGame:
    def __init__(self, username, password = None, theme_idx = 0):
        self.username = username
        self.password = password
        self.running_menu = True

        self.sound = pygame_menu.sound.Sound()
        self.sound.load_example_sounds()
        self.sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, None)
        self.enabled_sound = True # can be changed in init_def

        if theme_idx == 0:
            pygame.mixer.music.load('sound/paris.mp3')
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

        self.theme_idx = theme_idx

        self.surface = create_example_window('Maze Game', WINDOW_SIZE)
        icon = pygame.image.load('assets/LOGO UTE.png')
        pygame.display.set_icon(icon)

    def update_menu_sound_switch(self, enabled: bool) -> None:
        """
        Update menu sound.

        :param value: Value of the selector (Label and index)
        :param enabled: Parameter of the selector, (True/False)
        """
        # assert isinstance(value, tuple)
        self.enabled_sound = enabled
        if enabled:
            self.main_menu.set_sound(self.sound, recursive=True)
            print('Menu sounds were enabled')
            pygame.mixer.music.set_volume(self.bgm_volume)
        else:
            self.main_menu.set_sound(None, recursive=True)
            print('Menu sounds were disabled')
            pygame.mixer.music.set_volume(0)

    def return_to_login(self):
        self.running_menu = False
        g = LoginMenu(self.theme_idx)
        g.start(self.enabled_sound, self.sound)

    def change_bgm(self, volume):
        volume = int(volume) * 0.01
        self.bgm_volume = volume
        if self.enabled_sound:
            pygame.mixer.music.set_volume(volume)

    def init_theme(self):
        asset = ['assets/']
        x = self.theme_idx
        background_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path = asset[x] + 'nbackground.png',
            image_id = 'background')
        nbackground_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path = asset[x] + 'Home.png',
            image_id = 'nbackground')
        startgame_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path = asset[x] + 'start.png',
            image_id = 'nbackground')
        Setting_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path = asset[x] + 'Setting.png',
            image_id = 'nbackground')
        Help_img=pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path =asset[x] + 'Help.png',
            image_id = 'nbackground')
        About_img=pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path =asset[x] + 'About.png',
            image_id = 'nbackground')
              
        my_theme = pygame_menu.themes.Theme(
            background_color = background_img, 
            border_color = (0, 255, 0),
            border_width = 15,
            #cursor_color = (15, 15, 15),
            #focus_background_color = None,                          

            title = True,                                                 # có hay không title
            title_background_color = (249,72,82),                         # màu nền của title
            title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE, # style title bar
            title_close_button = True,                                    # nút thoát // quay lại
            title_close_button_background_color = (10, 10, 10),           # màu nút thoát // quay lại
            title_font = pygame_menu.font.FONT_COMIC_NEUE,                # font title
            title_font_antialias = True,                                  # khử răng cưa title font
            title_font_color = (255, 255, 255),                           # màu title
            title_font_shadow = True,                                     # bóng chữ title
            title_font_shadow_color = (0, 0, 0),                          # màu bóng chữ title

            # effect khi chọn
            widget_selection_effect = pygame_menu.widgets.LeftArrowSelection(
                arrow_size=(10, 15), arrow_right_margin=10, arrow_vertical_offset=0, blink_ms=0),

            widget_font = pygame_menu.font.FONT_COMIC_NEUE,               # font widget
            widget_font_antialias = True,                                 # font widget, khử răng cưa
            widget_font_color = (0, 0, 0),                                # màu chữ chưa được chọn
            selection_color = (255, 255, 255),                            # màu chữ được chọn
            widget_background_color = (249,72,82, 0),                     # màu nền widget
            widget_font_size = 30,                                        # size font widget                              
            widget_offset = (0, 0),                                       # x-axis and y-axis (x, y) offset
            widget_margin = (0, 25),                                      # khoảng cách của các ô
            widget_alignment = pygame_menu.locals.ALIGN_CENTER,           # căn giữa
            
            widget_box_arrow_color = (34, 24, 142),                       # màu mũi tên chọn hộp
            widget_box_border_width = 2,                                  # độ dày viền hộp chọn
            widget_box_border_color = (0, 0, 0),                          # màu viền hộp chọn
            widget_box_margin = (10, 0),                                  # vị trí hộp chọn
            widget_box_background_color = (255, 255, 255)                 # màu hộp chọn
            )

        self.my_main_menu_theme = my_theme.copy()
        self.my_main_menu_theme.background_color = nbackground_img
        #self.my_main_menu_theme # need for main menu
        self.my_main_menu_theme.title_close_button = False
        self.my_main_menu_theme.widget_margin = (-380, 10)
        self.my_main_menu_theme.widget_offset = (0, 50)
        self.my_main_menu_theme.selection_color=(249,16,23)

        self.my_start_game_theme = my_theme.copy()
        self.my_start_game_theme.background_color= startgame_img
        self.my_start_game_theme.widget_font_size = 25
        self.my_start_game_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        self.my_start_game_theme.widget_offset = (70, 200)
        self.my_start_game_theme.widget_margin = (-60, 20)
        self.my_start_game_theme.widget_font_color = (0, 0, 0),                        # màu chữ chưa được chọn
        self.my_start_game_theme.selection_color = (247, 12, 12),                            # màu chữ được chọn
        self.my_start_game_theme.widget_box_background_color = (0, 0, 0, 0) 
        #my_start_game_theme.widget_margin = (0, 0)

        self.my_settings_menu_theme = my_theme.copy()
        self.my_settings_menu_theme.background_color=Setting_img 
        self.my_settings_menu_theme.widget_font_size = 20
        self.my_settings_menu_theme.widget_font_color = (0, 0, 0),
        self.my_settings_menu_theme.selection_color = (247, 12, 12),                            # màu chữ được chọn
        self.my_settings_menu_theme.selection_color = (247, 12, 12),
        self.my_settings_menu_theme.widget_box_background_color = (0, 0, 0, 0)
        self.my_settings_menu_theme.widget_offset = (125, 0)
        self.my_settings_menu_theme.widget_margin = (-180, 25)
        self.my_settings_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        
        self.my_help_theme = my_theme.copy()
        self.my_help_theme.background_color= Help_img
        self.my_help_theme.widget_font_size = 25
        self.my_help_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        self.my_help_theme.widget_offset = (70, 200)
        self.my_help_theme.widget_margin = (-60, 20)
        self.my_help_theme.widget_font_color = (0, 0, 0),                        # màu chữ chưa được chọn
        self.my_help_theme.selection_color = (247, 12, 12),                            # màu chữ được chọn
        self.my_help_theme.widget_box_background_color = (0, 0, 0, 0) 
        
        
        self.my_about_theme = my_theme.copy()
        self.my_about_theme.background_color= About_img
        self.my_about_theme.widget_font_size = 25
        self.my_about_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        self.my_about_theme.widget_offset = (70, 200)
        self.my_about_theme.widget_margin = (-60, 20)
        self.my_about_theme.widget_font_color = (0, 0, 0),                        # màu chữ chưa được chọn
        self.my_about_theme.selection_color = (247, 12, 12),                            # màu chữ được chọn
        self.my_about_theme.widget_box_background_color = (0, 0, 0, 0) 
        #my_start_game_theme.widget_margin = (0, 0)

    def init_start_game(self):
        self.start_game_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1], #* 0.85,
        theme=self.my_start_game_theme,
        title='Start Game',
        width=WINDOW_SIZE[0], #* 0.6
        overflow = (False, False),
        center_content=False,
        #columns= 2,
        #rows = [5, 6],
        )
        items_levels = [('   Easy (20x20)   ', '20'),
             (' Medium (40x40) ', '40'),
             (' Hard (100x100)  ', '100')]

        def data_fun_sgm() -> None:
            """
            Print data of the menu.
            """
            print('Start game data:')
            data = self.start_game_menu.get_input_data()
            for k in data.keys():
                print(f'\t{k}\t=>\t{data[k]}')
            level = int(data['level'][0][1])

            print('random::')
            import random
            while True:
                a, b = random.randint(0, level - 1), random.randint(0, level - 1)
                c, d = random.randint(0, level - 1), random.randint(0, level - 1)
                if {a, b} != {c, d}:
                    break
            locations = [a, b, c, d]
            data['start_x'], data['start_y'], data['end_x'], data['end_y'] = a, b, c, d

            next_step = True
            if next_step:
                #pygame.mixer.music.stop()
                #pygame.mixer.music.unload()

                print('valid !! playgame now')

                if level == 20:
                    difficult = 'Easy'
                elif level == 40:
                    difficult = 'Medium'
                else:
                    difficult = 'Hard'

                tmp = data['mode_play'][1]
                if tmp == 0:
                    modePlay = 'Player'
                elif tmp == 1:
                    modePlay = 'Auto (A*)'
                else:
                    modePlay = 'Auto (BFS)'

                from game import Game
                if Game(self.surface, modePlay, difficult, data['start_x'], data['start_y'], data['end_x'], data['end_y'],
                     (0, 0), 0, data['game_name'], self.username).run() == False:
                    print('game done!!')
                    
                    self.running_menu = False
                    MenuGame(self.username, self.password, self.theme_idx).start(self.enabled_sound, self.sound)

        game_name = self.start_game_menu.add.text_input(
            title='Game name:  ',
            maxchar=10,
            textinput_id='game_name',
            input_underline = '__',)        

        # Add some buttons
        self.start_game_menu.add.selector(  # tao ra tro choi cho phep chon cac che do
            'Play mode',
            items=[('Play by yourself', 0),
                ('Auto play (A*)  ', 1),
                ('Auto play (BFS)', 2)],
            selector_id='mode_play',
            default=0,
            style='fancy'
        )
        size_map = self.start_game_menu.add.selector(  #chon cap do de choi
            'Level',
            items_levels,
            selector_id='level',
            default=0,
            style='fancy'
        )

        # Add final buttons
        #start_game_menu.add.button('Reset game setting', start_game_menu.reset_value)
        self.start_game_menu.add.button('Start game', data_fun_sgm, button_id='store')  # Call function
        self.start_game_menu.add.button('Return to main menu', pygame_menu.events.BACK,) #align=pygame_menu.locals.ALIGN_CENTER)

        # Add choose location input
        

    def init_setting(self):
        self.setting_help = pygame_menu.Menu(
        height=WINDOW_SIZE[1], #* 0.85,
        theme=self.my_help_theme,
        title='Help',
        width=WINDOW_SIZE[0], #* 0.6
        )
        button = self.setting_help.add.button('       Come Back         ', pygame_menu.events.BACK)
        button.translate(853, 334)

        self.setting_about = pygame_menu.Menu(
        height=WINDOW_SIZE[1], #* 0.85,
        theme=self.my_about_theme,
        title='About',
        width=WINDOW_SIZE[0], #* 0.6
        )
        button = self.setting_about.add.button('          Come Back            ', pygame_menu.events.BACK)
        button.translate(800, 430)

        self.settings_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1], #* 0.85,
        theme=self.my_settings_menu_theme,
        overflow = (False, False),
        title='Settings',
        width=WINDOW_SIZE[0], #* 0.6
        #columns = 2,
        #rows = [6, 6]
        )


        # Sound

        sound_switch = self.sound_switch = self.settings_menu.add.toggle_switch('Sound', self.enabled_sound,
                                        toggleswitch_id='sound_switch',
                                        onchange=self.update_menu_sound_switch,
                                        state_text=('Off', 'On'))

        volume_slider = self.settings_menu.add.range_slider(
            'BGM', 50, (0, 100), 1,
            rangeslider_id='volume',
            value_format=lambda x: str(int(x)),
            onchange = self.change_bgm)
        self.bgm_volume = int(volume_slider.get_value()) * 0.01

        # Add a clock
        #self.settings_menu.add.clock(clock_format='%Y/%m/%d %H:%M', title_format='Clock: {0}')

        # Add help, about
        help_button = self.settings_menu.add.button('Help', self.setting_help)
        about_button = self.settings_menu.add.button('About', self.setting_about)

        # Add final buttons
        return_button = self.settings_menu.add.button('Return to main menu', pygame_menu.events.BACK)#,align=pygame_menu.locals.ALIGN_CENTER)



    def init_main_menu(self):
        self.main_menu = pygame_menu.Menu(
        overflow = (False, False),
        height=WINDOW_SIZE[1] ,#* 0.7,
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        theme=self.my_main_menu_theme,
        title='Main menu',
        position = (20, 20),
        center_content=False,
        width=WINDOW_SIZE[0]) #* 0.8)

        self.main_menu.add.button('Start game', self.start_game_menu)
        self.main_menu.add.vertical_margin(85)
        self.main_menu.add.button('Settings', self.settings_menu)
        self.main_menu.add.vertical_margin(75)
        self.main_menu.add.button('Log out', self.return_to_login)  

        self.update_menu_sound_switch(self.enabled_sound)
    
    def init_menu(self):
        self.init_start_game()
        self.init_setting()
        self.init_main_menu()

    def start(self, enabled_sound = True, sound_engine = None):
        self.enabled_sound = enabled_sound
        if sound_engine != None:
            self.sound = sound_engine
        self.init_theme()
        self.init_menu()

        self.running_menu = True
        while self.running_menu:
            
            # Main menu
            self.main_menu.mainloop(self.surface)
            
            # Flip surface
            pygame.display.flip()

if __name__ == '__main__':
    g = LoginMenu()
    g.start()
    #g = MenuGame('user4','pas1')
    #g.start()
