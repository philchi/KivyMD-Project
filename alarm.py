from imports import *
timerCount = 1
timerSaved = timerCount
remainTime = 1
startTime = 0
swstartTime = 0
swPrevTime = 0
rtTemp = 'Alarm01.wav'

class clock(Screen):

    def __init__(self, area = 'Asia/Taipei', **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_clock, 0.2)
        self.timerClock = Clock
        self.stopwatch = Clock
        self.area = area
        self.ringtone = 'Alarm01.wav'

    def update_clock(self, *args):
        loc1 = pt.timezone(self.area)
        time1 = datetime.now(loc1)
        cleant1 = time1.strftime('%H:%M:%S')
        self.ids.time1.text = cleant1
        self.ids.time2.text = self.area
    
    def changeReg(self, reg):
        self.area = reg
        t.sleep(0.1)
        self.manager.current = 'clock'

    def update_timer(self, *args):
        global timerCount
        global remainTime
        global startTime

        remainTime = 1
        startTime = t.time()
        print(startTime)
        timerCount -= 1
        timer = self.formatTime(timerCount)
        self.ids.timer.text = timer

        if timerCount <= 0:
            winsound.PlaySound('ringtones/' + self.ringtone, winsound.SND_ASYNC + winsound.SND_LOOP)
            self.dia = MDDialog(
                title = 'Time is up',
                buttons = [MDFlatButton(text = 'OK', on_press = self.closeNotif)]
            )
            self.dia.open()
            return

        self.timerClock.schedule_once(self.update_timer, 1)
    
    def formatTime(self, tInSec):
        min, sec = divmod(tInSec, 60)
        hour, min = divmod(min, 60)
        time = "{:02d}:{:02d}:{:02d}".format(hour, min, sec)
        return time
    
    def timerBut(self):
        global startTime
        global remainTime

        if self.ids.timerStart.text == 'start':
            startTime = t.time()
            self.timerClock.schedule_once(self.update_timer, remainTime)
            self.ids.timerStart.text = 'pause'
        else:
            remainTime = remainTime - (t.time() - startTime)
            self.timerClock.unschedule(self.update_timer)
            self.ids.timerStart.text = 'start'
            print(remainTime)

    def resetTimer(self):
        global timerCount
        global remainTime

        remainTime = 1
        self.timerClock.unschedule(self.update_timer)
        timerCount = timerSaved
        self.ids.timer.text = self.formatTime(timerCount)
        self.ids.timerStart.text = 'start'
        print('reset')
    
    def closeNotif(self, dialog):
        self.resetTimer()
        winsound.PlaySound(None, winsound.SND_ASYNC)
        self.dia.dismiss()
    
    def selRingtone(self):
        files = list(os.walk('ringtones', topdown=True))[0][2]
        contentLayout = rtSelect(adaptive_height = True)
        contentSub = ScrollView()
        content = MDList()
        for f in files:
            content.add_widget(ItemConfirm(text=f))
        contentSub.add_widget(content)
        contentLayout.add_widget(contentSub)

        self.rtDia = MDDialog(
            title = 'Ringtones',
            type = 'custom',
            content_cls = contentLayout,
            buttons = [MDFlatButton(text = 'CANCEL', on_release = self.closeSelRingtone), MDFlatButton(text = 'OK' , on_release = self.saveSelRingtone)]
        )

        self.rtDia.open()
    
    def saveSelRingtone(self, dialog):
        global rtTemp
        
        winsound.PlaySound(None, winsound.SND_ASYNC)
        self.ringtone = rtTemp
        self.rtDia.dismiss()
    
    def closeSelRingtone(self, dialog):
        winsound.PlaySound(None, winsound.SND_ASYNC)
        self.rtDia.dismiss()

    def formatSW(self, tInSec):
        global swPrevTime
        global tempswTime

        curTime = tInSec + swPrevTime
        dec = int(round(curTime - int(curTime), 2) * 100)
        if dec == 100:
            dec = 0
        min, sec = divmod(int(curTime), 60)
        hour, min = divmod(min, 60)
        tempswTime = "{:02d}:{:02d}:{:02d}.{:02d}".format(hour, min, sec, dec)
        return tempswTime

    def stopwatchBut(self):
        global swstartTime
        global swPrevTime

        if self.ids.swStart.text == 'start': 
            swstartTime = t.time()
            self.stopwatch.schedule_once(self.update_stopwatch)
            self.ids.swStart.text = 'stop'
            self.ids.swCancel.text = 'lap'
        else:
            self.stopwatch.unschedule(self.update_stopwatch)
            self.ids.swStart.text = 'start'
            self.ids.swCancel.text = 'cancel'
            swPrevTime += swCurTime
        
    def update_stopwatch(self, *args):
        global swstartTime
        global swCurTime

        swCurTime = t.time() - swstartTime
        self.ids.stopwatch.text = self.formatSW(swCurTime)
        self.stopwatch.schedule_once(self.update_stopwatch)
    
    def resetSW(self):
        global swPrevTime
        global tempswTime

        if self.ids.swCancel.text == 'cancel':
            swPrevTime = 0
            self.ids.stopwatch.text = '00:00:00.00'
            self.ids.swLaps.clear_widgets()
            self.ids.swScroll.scroll_y = 1
        else:
            self.ids.swLaps.add_widget(
                OneLineListItem(
                    text = tempswTime,
                    font_style = 'H5'
                )
            )
            if self.ids.swScroll.viewport_size[1] > self.ids.swScrollLayout.size[1]:
                self.ids.swScroll.scroll_y = 0

class regiSelect(Screen):
    def __init__(self, clock, **kw):
        super().__init__(**kw)
        self.clock = clock
    
    def regSearch(self):
        self.ids.regions.clear_widgets()
        input = self.ids.textbox.text.lower()
        
        for reg in pt.all_timezones:
            temp = reg.lower()

            if input in temp:
                self.ids.regions.add_widget(
                    tzItem(
                        clock = self.clock,
                        text = reg
                    )
                )

class tzItem(OneLineListItem):
    def __init__(self, clock, **kwargs):
        super().__init__(**kwargs)
        self.clock = clock

class timerSelect(Screen):
    def __init__(self, clock, **kw):
        super().__init__(**kw)
        self.clock = clock
        self.hr = 0
        self.min = 0
        self.sec = 0

        for i in range(24):
            self.ids.hrs.add_widget(
                tsButton(
                    sc = self,
                    mark = 'hr',
                    text = str(i)
                )
            )
        
        for i in range(60):
            self.ids.mins.add_widget(
                tsButton(
                    sc = self,
                    mark = 'min',
                    text = str(i)
                )
            )
        for i in range(60):
            self.ids.secs.add_widget(
                tsButton(
                    sc = self,
                    mark = 'sec',
                    text = str(i)
                )
            )
    
    def returnSc(self):
        global timerCount
        global timerSaved
        global remainTime

        timerCount = 0
        timerCount += self.hr * 3600
        timerCount += self.min * 60
        timerCount += self.sec
        timerSaved = timerCount
        remainTime = 1  
        self.clock.ids.timer.text = self.ids.timerPrev.text
    
    def changeTimerPrev(self, button):
        if button.mark == 'hr':
            self.hr = int(button.text)
        elif button.mark == 'min':
            self.min = int(button.text)
        elif button.mark == 'sec':
            self.sec = int(button.text)
        
        temp = '{:02d}:{:02d}:{:02d}'.format(self.hr, self.min, self.sec)
        self.ids.timerPrev.text = temp

class tsButton(Button):
    def __init__(self, sc, mark, **kwargs):
        super().__init__(**kwargs)
        self.mark = mark
        self.sc = sc

class rtSelect(MDRelativeLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ItemConfirm(OneLineAvatarIconListItem):
    def set_icon(self, instance_check):
        global rtTemp

        instance_check.active = True
        rtTemp = self.text
        winsound.PlaySound(None, winsound.SND_ASYNC)
        winsound.PlaySound('ringtones/' + self.text, winsound.SND_ASYNC)
        

class TimeApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'LightGreen'
        screen = ScreenManager(transition = FadeTransition())
        sc1 = clock(name = 'clock')
        sc2 = regiSelect(clock = sc1, name = 'regiSelect')
        sc3 = timerSelect(clock = sc1, name = 'timerSelect')
        screen.add_widget(sc1)
        screen.add_widget(sc2)
        screen.add_widget(sc3)

        return screen

if __name__ == '__main__':
    TimeApp().run()
