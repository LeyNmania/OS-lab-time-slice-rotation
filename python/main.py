from tkinter import *
import tkinter.filedialog
import threading
import time
from process import *

# whether opened a file
open_already = 0
# 就绪
ReadyPCBs = []
# 后备
BackupReadyPCBs = []
# 输入
InputWaitingPCBs = []
# 输出
OutputWaitingPCBs = []
# 其他
OtherWaitingPCBs = []
# 结束
FinishPCBs = []

# 当前运行
C_run = False
C_pcb = PCB([], '', 0)
# 当前输入
I_run = False
# 当前输出
O_run = False
# 当前其他
W_run = False

# 时间片大小
TimeSlice = 0
# 减少时间记录
timeslice = 0
# 记录运行状态
run_flag = True


class My_GUI():
    def __init__(self, window_tk):
        self.window_tk = window_tk

    def set_init_window(self):
        self.window_tk.title('yecq OS lab 248')  # title
        self.window_tk.geometry('850x500+500+250')

        menubar = Menu(self.window_tk)
        menubar.add_command(label='File', command=self.open_file)
        menubar.add_command(label='About', command=self.about_text)
        self.window_tk.config(menu=menubar)

        # 时间片-- StringVar is a dynamic variable which could display on screen dynamically
        self.timeslice_text = StringVar()
        self.C_entry_text = StringVar()
        self.Cwait_list_text = StringVar()
        self.wait_list_text = StringVar()
        self.Iwait_list_text = StringVar()
        self.Owait_list_text = StringVar()
        self.other_list_text = StringVar()

        btn_frame = Frame(width=850, height=50)

        self.time_label = Label(btn_frame, text='R Size:', width=10, height=1)
        self.time_entry = Entry(btn_frame, text='200', width=15, textvariable=self.timeslice_text)
        self.begin_btn = Button(btn_frame, text='Start', width=10, height=1, command=self.begin,state = DISABLED)
        self.stop_btn = Button(btn_frame, text='Stop', width=10, height=1, command=self.stop, state=DISABLED)


        # 显示
        btn_frame.place(x=50, y=20)
        self.begin_btn.place(x=30, y=5)
        self.stop_btn.place(x=265, y=5)
        self.time_label.place(x=500, y=8)
        self.time_entry.place(x=580, y=8)

        # 信息显示Frame
        message_frame = Frame(width=800, height=50)
        # 运行进程显示
        self.C_label = Label(message_frame, text='Running', width=15, height=1)
        self.C_entry = Entry(message_frame, width=15, state='readonly', textvariable=self.C_entry_text)
        # 显示
        message_frame.place(x=50, y=80)
        self.C_label.grid(row=0, column=1)
        self.C_entry.grid(row=0, column=2, sticky='we', ipadx=60, padx=5)

        # 队列信息Frame
        list_frame = Frame(width=850, height=330)
        # 队列显示
        self.Cwait_list_lf = LabelFrame(list_frame, width=160, height=340, text='Ready List')
        self.wait_list_lf = LabelFrame(list_frame, width=160, height=340, text='Backup List')
        self.Iwait_list_lf = LabelFrame(list_frame, width=160, height=340, text='Input Waiting')
        self.Owait_list_lf = LabelFrame(list_frame, width=160, height=340, text='Output Waiting')
        self.other_list_lf = LabelFrame(list_frame, width=160, height=340, text='Others')
        self.Cwait_list = Listbox(self.Cwait_list_lf, height=15, listvariable=self.Cwait_list_text)
        self.wait_list = Listbox(self.wait_list_lf, height=15, listvariable=self.wait_list_text)
        self.Iwait_list = Listbox(self.Iwait_list_lf, height=15, listvariable=self.Iwait_list_text)
        self.Owait_list = Listbox(self.Owait_list_lf, height=15, listvariable=self.Owait_list_text)
        self.other_list = Listbox(self.other_list_lf, height=15, listvariable=self.other_list_text)
        # 显示
        list_frame.place(x=50, y=130)
        self.Cwait_list_lf.pack(side=LEFT)
        self.wait_list_lf.pack(side=LEFT)
        self.Iwait_list_lf.pack(side=LEFT)
        self.Owait_list_lf.pack(side=LEFT)
        self.other_list_lf.pack(side=LEFT)
        self.Cwait_list.pack(anchor=CENTER)
        self.wait_list.pack(anchor=CENTER)
        self.Iwait_list.pack(anchor=CENTER)
        self.Owait_list.pack(anchor=CENTER)
        self.other_list.pack(anchor=CENTER)

    # 按钮

    def about_text(self):
        showinfo(u'yecOSlab-248',u'No copy')

    def open_file(self):
        # open read
        fileName = tkinter.filedialog.askopenfilename(initialdir='./')
        file_str = open_file(fileName)
        # get a list of PCBS including all info
        pcbs = make_pcbs(file_str)

        if pcbs != None:
            self.begin_btn.config(state = NORMAL)

        # get the PCB amount and record
        self.times = get_pcb_times(file_str)

        for pcb in pcbs:
            # write the read process into the writing list
            ReadyPCBs.append(pcb)

        # according to the backupqueue to add the display
        for pcb_print in ReadyPCBs:
            self.Cwait_list.insert(END, pcb_print.get_PName())

        # finish displaying and add the list content to places
        if ReadyPCBs != []:
            self.deal_with_list(ReadyPCBs)

        # create process when opened the file
        self.t1 = threading.Thread(target=self.run_one_timeslice)



    def begin(self):
        global timeslice
        global TimeSlice
        global run_flag

        # judge
        if run_flag:
            # judge whether the input
            if self.time_entry.get() == '':
                showerror(u'Error', u'Input rotate size plz')
            else:
                self.stop_btn.config(state=NORMAL)
                self.begin_btn.config(state=DISABLED)
                # get size of R
                # timeslice_text <==> self.time_entry
                TimeSlice = int(self.time_entry.get())
                timeslice = TimeSlice
                # run_one_timeslice
                self.t1.start()
        else:
            self.stop_btn.config(state=NORMAL)
            self.begin_btn.config(state=DISABLED)
            # continue
            threading.Thread(target=self.change_flag_true).start()

    def stop(self):
        self.begin_btn.config(state=NORMAL)
        self.stop_btn.config(state=DISABLED)
        # stop
        threading.Thread(target=self.change_flag_false).start()

    def change_flag_false(self):
        global run_flag
        run_flag = False

    def change_flag_true(self):
        global run_flag
        run_flag = True

    # figur out content
    # after terms
    def run_one_timeslice(self):
        global C_run
        global C_pcb
        global timeslice

        while (True):
            # entry this loop waiting
            while (not run_flag):
                pass

            # -1
            self.reduce_time()

            time.sleep(0.1)
            timeslice = timeslice - 1

            # do with time slices
            if timeslice < 0:
                timeslice = TimeSlice
                # if not done
                if C_pcb.RemainedTime > 0:
                    # make a Istruction added to pcb`s instruction`s list head
                    C_pcb.Plist.insert(0, CInstruction('C%s' % (C_pcb.RemainedTime + 1)))  # compensate
                    C_pcb.set_RemainedTime(0)
                    BackupReadyPCBs.append(C_pcb)
                    C_run = False

            # judge the current
            if C_run == True:
                if C_pcb.RemainedTime < 0:
                    C_run = False
                    self.go_to_where(C_pcb)

            # judge the list
            if ReadyPCBs != []:
                self.deal_with_list(ReadyPCBs)
            if BackupReadyPCBs != []:
                if_pcb_list = BackupReadyPCBs.copy()
                for Rpcb in if_pcb_list:
                    if Rpcb.get_RemainedTime() <= 0:
                        BackupReadyPCBs.remove(Rpcb)
                        if C_run:
                            BackupReadyPCBs.append(Rpcb)
                        else:
                            # get running time
                            Rpcb.set_RemainedTime(Rpcb.Plist[0].get_RunTime())
                            C_run = True
                            # 1st should get the right place after pushing ,then delete the first instruction
                            Rpcb.Plist.pop(0)
                            C_pcb = Rpcb
                pass
            if InputWaitingPCBs != []:
                self.deal_with_list(InputWaitingPCBs)
            if OutputWaitingPCBs != []:
                self.deal_with_list(OutputWaitingPCBs)
            if OtherWaitingPCBs != []:
                self.deal_with_list(OtherWaitingPCBs)

            # display
            self.re_print()
            self.print_log()

            # end
            if self.times == len(FinishPCBs):
                # clean the current
                self.timeslice_text.set('')

                print('+' * 30 + '\tEND\t' + '+' * 30)
                print(self.times, '\t\t', len(FinishPCBs))
                print('FinishPCBs', FinishPCBs, [fpcb.PName for fpcb in FinishPCBs])
                break

    # decrease time no judging if rest time <0
    def reduce_time(self):
        # running time -= 1
        if C_run == True:
            remainedtime = C_pcb.get_RemainedTime()
            C_pcb.set_RemainedTime(remainedtime - 1)
        # input list -1
        if InputWaitingPCBs != []:
            for pcb in InputWaitingPCBs:
                remainedtime = pcb.get_RemainedTime()
                pcb.RemainedTime = remainedtime - 1
        # output list -1
        if OutputWaitingPCBs != []:
            for pcb in OutputWaitingPCBs:
                remainedtime = pcb.get_RemainedTime()
                pcb.RemainedTime = remainedtime - 1
        # others -1
        if OtherWaitingPCBs != []:
            for pcb in OtherWaitingPCBs:
                remainedtime = pcb.get_RemainedTime()
                pcb.RemainedTime = remainedtime - 1
        pass

    # do with the list content
    def deal_with_list(self, pcb_list):

        if_pcb_list = pcb_list.copy()


        for Rpcb in if_pcb_list:
            # read the list within no rest time , keep the having the rest
            if Rpcb.get_RemainedTime() <= 0:

                pcb_list.remove(Rpcb)
                self.go_to_where(Rpcb)


    def go_to_where(self, Rpcb_tw: PCB):

        global C_run
        global I_run
        global O_run
        global W_run

        global C_pcb

        if Rpcb_tw.Plist[0].get_InstrucionId() == 'C':

            if not C_run:
                # get running time
                Rpcb_tw.set_RemainedTime(Rpcb_tw.Plist[0].get_RunTime())
                C_run = True

                Rpcb_tw.Plist.pop(0)
                C_pcb = Rpcb_tw
            else:
                ReadyPCBs.append(Rpcb_tw)
        elif Rpcb_tw.Plist[0].get_InstrucionId() == 'I':
            # if input , add to inputlist
            Rpcb_tw.set_RemainedTime(Rpcb_tw.Plist[0].get_RunTime())
            Rpcb_tw.Plist.pop(0)
            InputWaitingPCBs.append(Rpcb_tw)
        elif Rpcb_tw.Plist[0].get_InstrucionId() == 'O':
            Rpcb_tw.set_RemainedTime(Rpcb_tw.Plist[0].get_RunTime())
            Rpcb_tw.Plist.pop(0)
            OutputWaitingPCBs.append(Rpcb_tw)
        elif Rpcb_tw.Plist[0].get_InstrucionId() == 'W':
            Rpcb_tw.set_RemainedTime(Rpcb_tw.Plist[0].get_RunTime())
            Rpcb_tw.Plist.pop(0)
            OtherWaitingPCBs.append(Rpcb_tw)
        elif Rpcb_tw.Plist[0].get_InstrucionId() == 'H':
            FinishPCBs.append(Rpcb_tw)
        pass

    def re_print(self):
        # ud timeslice
        self.timeslice_text.set(str(timeslice))
        # display window
        if C_run == True:
            self.C_entry_text.set(C_pcb.get_PName() + ' : ' + str(C_pcb.RemainedTime))
        else:
            self.C_entry_text.set('')
        # ready redisplay
        pcb_list_Ready_print = []
        for pcb_print in ReadyPCBs:
            pcb_list_Ready_print.append(pcb_print.PName)
        self.Cwait_list_text.set(pcb_list_Ready_print)

        # backup redisplay
        pcb_list_Back_print = []
        for pcb_print in BackupReadyPCBs:
            pcb_list_Back_print.append(pcb_print.PName + ' : ' + str(pcb_print.RemainedTime) + ' : ' + str(
                pcb_print.Plist[0].get_RunTime()))
        self.wait_list_text.set(pcb_list_Back_print)

        # input redisplay
        pcb_list_Input_print = []
        for pcb_print in InputWaitingPCBs:
            pcb_list_Input_print.append(pcb_print.PName + '--> Input  ' + str(pcb_print.RemainedTime))
        self.Iwait_list_text.set(pcb_list_Input_print)

        # output redisplay
        pcb_list_Output_print = []
        for pcb_print in OutputWaitingPCBs:
            pcb_list_Output_print.append(pcb_print.PName + '--> Output  ' + str(pcb_print.RemainedTime))
        self.Owait_list_text.set(pcb_list_Output_print)

        # other redisplay
        pcb_list_Pure_print = []
        for pcb_print in OtherWaitingPCBs:
            pcb_list_Pure_print.append(pcb_print.PName + '--> Wait  ' + str(pcb_print.RemainedTime))
        self.other_list_text.set(pcb_list_Pure_print)
        pass

    # print logs
    def print_log(self):
        print('*' * 30 + '\tPrint logs\t' + '*' * 30)
        print('\t\tTimes_now--->%s' % (timeslice))
        print('-' * 30 + '\tList content\t' + '-' * 30)

        ReadyPCB_string = ''
        BackupReadyPCBs_string = ''
        InputWaitingPCBs_string = ''
        OutputWaitingPCBs_string = ''
        OtherWaitingPCBs_string = ''
        FinishPCBs_string = ''

        print('ReadyPCBs:\t')
        for p in ReadyPCBs:
            print(p.PName, p.RemainedTime, )
            ReadyPCB_string = ReadyPCB_string + p.PName + ' --> ' + str(p.RemainedTime) + '\tnext:' + p.Plist[
                0].get_InstrucionId() + ':' + str(p.Plist[0].get_RunTime()) + '\t'
        print('BackupReadyPCBs:')
        for p in BackupReadyPCBs:
            print(p.PName, p.RemainedTime, )
            BackupReadyPCBs_string = BackupReadyPCBs_string + p.PName + ' --> ' + str(p.RemainedTime) + '\tnext:' + \
                                     p.Plist[0].get_InstrucionId() + ':' + str(p.Plist[0].get_RunTime()) + '\t'
        print('InputWaitingPCBs:')
        for p in InputWaitingPCBs:
            print(p.PName, p.RemainedTime, )
            InputWaitingPCBs_string = InputWaitingPCBs_string + p.PName + ' --> ' + str(p.RemainedTime) + '\t'
        print('OutputWaitingPCBs:')
        for p in OutputWaitingPCBs:
            print(p.PName, p.RemainedTime, )
            OutputWaitingPCBs_string = OutputWaitingPCBs_string + p.PName + ' --> ' + str(p.RemainedTime) + '\t'
        print('OtherWaitingPCBs:')
        for p in OtherWaitingPCBs:
            print(p.PName, p.RemainedTime, )
            OtherWaitingPCBs_string = OtherWaitingPCBs_string + p.PName + ' --> ' + str(p.RemainedTime) + '\t'

        for p in FinishPCBs:
            FinishPCBs_string = FinishPCBs_string + p.PName + ' --> ' + str(p.RemainedTime) + '\t'

        print(' ' * 30 + '\t Running \t' + ' ' * 30)
        print('C_pcb: \t' + C_pcb.PName + '\t : \t' + str(C_pcb.RemainedTime))
        print('C_run: \t' + str(C_run))

        file_string = '*' * 60 + \
                      '\n    timeslice:\t' + str(timeslice) + \
                      '\n\t\tC_pcb:\t' + C_pcb.PName + '\t : \t' + str(C_pcb.RemainedTime) + \
                      '\t\t  C_run:\t' + str(C_run) + \
                      '\n    the_list_message:\n' + \
                      '\t    ReadyPCBs: ' + ReadyPCB_string + \
                      '\n\t  BackupReadyPCBs: ' + BackupReadyPCBs_string + \
                      '\n\t  InputWaitingPCBs: ' + InputWaitingPCBs_string + \
                      '\n\t  OutputWaitingPCBs: ' + OutputWaitingPCBs_string + \
                      '\n\t  OtherWaitingPCBs: ' + OtherWaitingPCBs_string + \
                      '\n\t  FinishPCBs: ' + FinishPCBs_string + '\n '




def labstart():
    w = Tk()
    gui = My_GUI(w)
    gui.set_init_window()

    w.mainloop()


if __name__ == '__main__':
    labstart()