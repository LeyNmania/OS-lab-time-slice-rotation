from tkinter.messagebox import *
import re

def open_file(fileName):
    file = open(fileName,'r',encoding='UTF-8')
    file_content = file.read()
    if len(file_content)<0:
        showerror('Error Doc','Fail to read')
    return file_content # type str

def make_dict(s):
    s_array = s.split('\n')
    print('=' * 20 + 'Make - Dic-Feel result' + '=' * 20)
    print(s_array)

    P = locals() #命名空间(duplicated) can only read / P is a copy
    P_dict = {}
    P_account = 0

    for s in s_array:
        if s.find('P')>=0:
            P_account = P_account + 1
            P['P%s' % P_account] = []
        else:
            P['P%s' % P_account].append(s)

    for times in range(1, P_account + 1):
        print('=' * 20 + 'Make Dic-Proc result' + '=' * 20)
        print('P%s:%s' % (times, P['P%s' % times]))

        P_dict['P%s' % times] = P['P%s' % times]

    print('=' * 20 + 'DicRI-DicRI result' + '=' * 20)
    print(P_dict)
    return P_account, P_dict

def get_pcb_times(str):
    times = 0
    str_array = str.split('\n')
    for s in str_array:
        if s.find('P')>=0:
            times = times + 1
    return times

def make_pcbs(file_str):
    Ptimes,Pdict = make_dict(file_str)
    #  make PCB
    pcbs = []
    for times in range(1, Ptimes + 1):
        # extract process
        CIS = []
        for cis_str in Pdict['P%s' % times]:
            cis = CInstruction(cis_str)
            CIS.append(cis)

        pcb = PCB(CIS, 'P%s' % times, times)
        pcbs.append(pcb)
        # display PCB content
        print('=' * 30 + 'Display PCB content: ' + '=' * 30)
        pcb.pcb_print()
    print(pcbs)
    return pcbs


class PCB():
    # self.PName
    def __init__(self, P_list, PName, Pid):
        # name
        self.PName = 'P%s' % Pid
        # pid
        self.Pid = Pid
        # instruction list
        self.Plist = P_list
        # left time
        self.RemainedTime = 0

    def get_PName(self):
        return self.PName

    def get_Pid(self):
        return self.Pid

    def get_Plist(self) -> list:
        return self.Plist

    def get_RemainedTime(self) -> int:
        return self.RemainedTime

    def set_Plist(self, plist):
        self.Plist = plist

    def set_RemainedTime(self, time):
        self.RemainedTime = time

    def pcb_print(self):
        print('PNamem:%s \nPid:%s \nPlist:%s \nReaminedTime:%s' % (self.PName, self.Pid, self.Plist, self.RemainedTime))
        for i in range(len(self.Plist)):
            print('Plist.list[0]:\t%s' % self.Plist[i].get_InstrucionId())
        print()

class CInstruction(object):
    def __init__(self, string):
        # instruction running time
        self.RunTime = int(re.findall('(\d+)',string)[0])
        # instruction type
        self.InstructionId = re.findall('(\w)',string)[0]

    def get_RunTime(self):
        return self.RunTime

    def get_InstrucionId(self):
        return self.InstructionId

if __name__ == '__main__':
    print('Test Class CIs')
    c = CInstruction('C')
    print('%s %s' %(c.get_RunTime(),c.get_InstrucionId()))

    # file_str = open_file(u'.\test.txt')
    # pcbs = make_pcbs(file_str)
