import time
import wx
import random
import re
from threading import Thread
import urllib
import socket
from os.path import exists
def isempty(host):
    #THIS FUNCTION CHECKS IF THE SERVER IS FREE
    try:
       hostie=host
       port=host.split(":")[1]
       port=int(port)
       host=host.split(":")[0]
       sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       sock.connect((host, port))
       sock.send("\xFF\xFF\xFF\xFF %s\0" % ('status'))
       sock.settimeout(2)
       a=sock.recv(2048)
       a=a.split("\xff\xff\xff\xffprint\n")[1]
       a=a.split('\n')
       plrs=a[1:]
    except:
        return False;
    if len(plrs)==1:
        return True;
    else:
        return False;

def doesrun(host):
    #THIS FUNCTION CHECKS IF A SERVER IS RUNNING
    try:
       hostie=host
       port=host.split(":")[1]
       port=int(port)
       host=host.split(":")[0]
       sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       sock.connect((host, port))
       sock.send("\xFF\xFF\xFF\xFF %s\0" % ('status'))
       sock.settimeout(1)
       a=sock.recv(2048)
    except:
        return False;
    return True;

#PASSWORD LIST
pws=["pumpkin", "potato", "victory", "thx", "pb2", "dollar", "up", "at", "orange", "blue", "purple", "red", "green", "ulose", "nope", "gj", "gg", "2s", "3s", "2v2", "3v3", "nah", "no", "hello", "sup", "4s", "omg", "instinct", "coke", "cherry", "sick", "nobody", "never", "1234", "123", "welcome", "hi", "instinct", "nice", "bam"]
class panel_RentStd(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.slist = wx.Choice(self, pos=(10, 8), choices=[], size=(323, 22))
        self.b_refresh = wx.Button(self, pos=(335, 8), label="Refresh", size=(50, 22))
        self.t_password = wx.StaticText(self, pos=(10, 52), label="Join password [You can leave it empty]:")
        self.var_password = wx.TextCtrl(self, pos=(280, 50), size=(105, 22))
        self.t_login = wx.StaticText(self, pos=(10, 76), label="Login password [You can leave it empty]:")
        self.var_login = wx.TextCtrl(self, pos=(280, 74), size=(105, 22))
        self.t_elim = wx.StaticText(self, pos=(10, 100), label="Elim:")
        self.var_elim = wx.TextCtrl(self, pos=(280, 98), size=(20, 22))
        self.t_guntemp = wx.StaticText(self, pos=(10, 124), label="Guntemp:")
        self.var_guntemp = wx.Choice(self, pos=(280, 122), size=(75, 22), choices=["False", "True"])
        self.t_flagcapendsround = wx.StaticText(self, pos=(10, 148), label="Flagcapendsround:")
        self.var_flagcapendsround = wx.Choice(self, pos=(280, 146), size=(75, 22), choices=["False", "True"])
        self.t_flagmustbeatbase = wx.StaticText(self, pos=(10, 172), label="Flagmustbeatbase:")
        self.var_flagmustbeatbase = wx.Choice(self, pos=(280, 170), size=(75, 22), choices=["False", "True"])
        self.t_timelimit = wx.StaticText(self, pos=(10, 196), label="Time Limit:")
        self.var_timelimit = wx.TextCtrl(self, pos=(280, 194), size=(20, 22))
        self.t_fraglimit = wx.StaticText(self, pos=(10, 220), label="Frag Limit:")
        self.var_fraglimit = wx.TextCtrl(self, pos=(280, 218), size=(20, 22))
        self.t_sv_gravity = wx.StaticText(self, pos=(10, 244), label="sv_gravity:")
        self.var_sv_gravity = wx.TextCtrl(self, pos=(280, 242), size=(40, 22))
        self.t_observerblackout = wx.StaticText(self, pos=(10, 268), label="observerblackout:")
        self.var_observerblackout = wx.Choice(self, pos=(280, 266), size=(75, 22), choices=["False", "True"])
        self.t_gren_explodeonimpact = wx.StaticText(self, pos=(10, 292), label="gren_explodeonimpact:")
        self.var_gren_explodeonimpact = wx.Choice(self, pos=(280, 290), size=(75, 22), choices=["False", "True"])
        self.t_guntemp_2 = wx.StaticText(self, pos=(10, 316), label="Guntemp (Decrease, set to False for jump maps):")
        self.var_guntemp_2 = wx.Choice(self, pos=(280, 314), size=(75, 22), choices=["False", "True"])
        self.b_rent=wx.Button(self, pos=(150, 370), label="Rent", size=(100, 28))
        
        self.var_guntemp_2.SetSelection(1)
        self.var_gren_explodeonimpact.SetSelection(0)
        self.var_observerblackout.SetSelection(1)
        self.var_gren_explodeonimpact.SetSelection(0)
        self.var_sv_gravity.WriteText('800')
        self.var_fraglimit.WriteText('50')
        self.var_timelimit.WriteText('20')
        self.var_elim.WriteText('60')
        self.var_guntemp.SetSelection(0)
        self.var_flagcapendsround.SetSelection(0)
        self.var_flagmustbeatbase.SetSelection(0)
        
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.slist)
        self.Bind(wx.EVT_BUTTON, self.OnRent, self.b_rent)
        self.Bind(wx.EVT_BUTTON, self.RefreshServers, self.b_refresh)
        self.OnChoice("blablabla")

    def RefreshServers(self, e):
        #REFRESHING SERVERLIST
        global serverinfo
        self.serverlist=[]
        serverinfo=[]
        for i in serverinfox:
           hx=i[1]
           if isempty(hx):
              serverinfo.append(i)
              self.serverlist.append(i[0]+' (%s)' % i[-5])  
        self.slist.Destroy()
        self.slist = wx.Choice(self, pos=(10, 8), choices=self.serverlist, size=(323, 22))
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.slist) 
        if len(self.serverlist)>0: 
           self.slist.SetSelection(0)
           self.b_rent.Enable()
        else:
           self.b_rent.Disable()

    def OnRent(self, e):
        #CREATING A SUBMISSION AND SENDING IT
        sinfo=serverinfo[self.slist.GetSelection()]
        limits=sinfo[-1]
        pw=self.var_password.GetLineText(0)
        login=self.var_login.GetLineText(0)
        errors=""
        pw=re.sub("(\W)", "", pw)
        login=re.sub("(\W)", "", login)
        elim=self.var_elim.GetLineText(0)
        timelimit=self.var_timelimit.GetLineText(0)
        fraglimit=self.var_fraglimit.GetLineText(0)
        sv_gravity=self.var_sv_gravity.GetLineText(0)
        lvar=[]
        nvar=[]
        lim=[]
        req={}
        req["server"]=sinfo[-2]
        url=sinfo[-3]
        req["botcheck"]=re.findall('Enter the word <strong\\>(.*?)\\<\\/strong\\> into this box', urllib.urlopen(url).read())[0]
        if pw=="":
            pw=random.choice(pws)
        req["password"]=pw
        if login=="":
            for i in range(4):
                login=login+chr(random.randint(97, 122))
        req["login"]=str(login)
        if sinfo[2]:
            lvar.append(elim)
            nvar.append("var_elim")
            req["var_elim"]=elim
            lim.append(limits[0])
        if sinfo[3]:
            if self.var_guntemp.GetSelection()==0:
                req["var_guntemp_inc"]="0"
            else:
                req["var_guntemp_inc"]="11"
        if sinfo[4]:
            if self.var_flagcapendsround.GetSelection()==0:
                req["var_flagcapendsround"]="false"
            else:
                req["var_flagcapendsround"]="true"
        if sinfo[5]:
            if self.var_flagmustbeatbase.GetSelection()==0:
                req["var_flagmustbeatbase"]="false"
            else:
                req["var_flagmustbeatbase"]="true"
        if sinfo[6]:
            lvar.append(timelimit)
            nvar.append("var_timelimit")
            req["var_timelimit"]=timelimit
            lim.append(limits[1])
        if sinfo[7]:
            lvar.append(fraglimit)
            nvar.append("var_fraglimit")
            req["var_fraglimit"]=fraglimit
            lim.append(limits[2])
        if sinfo[8]:
            lvar.append(sv_gravity)
            nvar.append("var_sv_gravity")
            req["var_sv_gravity"]=sv_gravity
            lim.append(limits[3])
        if sinfo[9]:
            if self.var_observerblackout.GetSelection()==0:
                req["var_observerblackout"]="false"
            else:
                req["var_observerblackout"]="true"

        if sinfo[10]:
            if self.var_gren_explodeonimpact.GetSelection()==0:
                req["var_gren_explodeonimpact"]="false"
            else:
                req["var_gren_explodeonimpact"]="true"
        if sinfo[11]:
            if self.var_guntemp_2.GetSelection()==1:
                req["var_guntemp_dec"]="4"
            else:
                req["var_guntemp_dec"]="0"
        for i in range(len(lvar)):
            try:
               namex=nvar[i]
               valx=int(lvar[i])
               limx=lim[i]
               maxx=limx[1]
               minx=limx[0]
               req[namex]=str(valx)
               if valx<minx:
                  errors=errors+"ERROR: The value of \"%s\" must be equal to or greater than %s.\n" % (namex, minx)
               if valx>maxx:
                  errors=errors+"ERROR: The value of \"%s\" must be equal to or less than %s.\n" % (namex, maxx)

            except:
               errors=errors+"ERROR: The value of \"%s\" must be integer, not string.\n" % namex
        ok.rp.txt.Clear()
        if errors=="":
            r=urllib.urlopen(url+sinfo[-6], urllib.urlencode(req.items()))
            txt1=r.read()
            if txt1.find('errors')==-1:
                ok.rp.txt.WriteText("Server: %s (connect %s)\nJoin password: %s\nLogin password: %s" % (sinfo[0], sinfo[1], pw, login))
            else:
                ok.rp.txt.WriteText("An unknown error has occured.")
        else:
            ok.rp.txt.WriteText(errors)
        ok.Disable()
        ok.rp.Centre()
        ok.rp.Show()

    def OnChoice(self, e):
        #THIS FUNCTION ACTIVATES THE FORM WHEN USER A SERVER WAS SELECTED
        global sinfo
        sid=self.slist.GetSelection()
        if sid==wx.NOT_FOUND:
            self.b_rent.Disable()
            return
        else:
            self.b_rent.Enable()

        sinfo=serverinfo[sid]
        if sinfo[2]:
            self.var_elim.Enable()
        else:
            self.var_elim.Disable()
        if sinfo[3]:
            self.var_guntemp.Enable()
        else:
            self.var_guntemp.Disable()
        if sinfo[4]:
            self.var_flagcapendsround.Enable()
        else:
            self.var_flagcapendsround.Disable()
        if sinfo[5]:
            self.var_flagmustbeatbase.Enable()
        else:
            self.var_flagmustbeatbase.Disable()
        if sinfo[6]:
            self.var_timelimit.Enable()
        else:
            self.var_timelimit.Disable()
        if sinfo[7]:
            self.var_fraglimit.Enable()
        else:
            self.var_fraglimit.Disable()
        if sinfo[8]:
            self.var_sv_gravity.Enable()
        else:
            self.var_sv_gravity.Disable()
        if sinfo[9]:
            self.var_observerblackout.Enable()
        else:
            self.var_observerblackout.Disable()
        if sinfo[10]:
            self.var_gren_explodeonimpact.Enable()
        else:
            self.var_gren_explodeonimpact.Disable()
        if sinfo[11]:
            self.var_guntemp_2.Enable()
        else:
            self.var_guntemp_2.Disable()

class panel_Manage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.slist = wx.Choice(self, pos=(10, 8), choices=[], size=(323, 22))
        self.b_select = wx.Button(self, pos=(335, 8), label="Manage", size=(50, 22))
        self.t_password = wx.StaticText(self, pos=(10, 52), label="Join password [You can leave it empty]:")
        self.var_password = wx.TextCtrl(self, pos=(280, 50), size=(105, 22))
        self.t_login = wx.StaticText(self, pos=(10, 76), label="Login password [You can leave it empty]:")
        self.var_login = wx.TextCtrl(self, pos=(280, 74), size=(105, 22))
        self.t_elim = wx.StaticText(self, pos=(10, 100), label="Elim:")
        self.var_elim = wx.TextCtrl(self, pos=(280, 98), size=(20, 22))
        self.t_guntemp = wx.StaticText(self, pos=(10, 124), label="Guntemp:")
        self.var_guntemp = wx.Choice(self, pos=(280, 122), size=(75, 22), choices=["False", "True", ""])
        self.t_flagcapendsround = wx.StaticText(self, pos=(10, 148), label="Flagcapendsround:")
        self.var_flagcapendsround = wx.Choice(self, pos=(280, 146), size=(75, 22), choices=["False", "True", ""])
        self.t_flagmustbeatbase = wx.StaticText(self, pos=(10, 172), label="Flagmustbeatbase:")
        self.var_flagmustbeatbase = wx.Choice(self, pos=(280, 170), size=(75, 22), choices=["False", "True", ""])
        self.t_timelimit = wx.StaticText(self, pos=(10, 196), label="Time Limit:")
        self.var_timelimit = wx.TextCtrl(self, pos=(280, 194), size=(20, 22))
        self.t_fraglimit = wx.StaticText(self, pos=(10, 220), label="Frag Limit:")
        self.var_fraglimit = wx.TextCtrl(self, pos=(280, 218), size=(20, 22))
        self.t_sv_gravity = wx.StaticText(self, pos=(10, 244), label="sv_gravity:")
        self.var_sv_gravity = wx.TextCtrl(self, pos=(280, 242), size=(40, 22))
        self.t_observerblackout = wx.StaticText(self, pos=(10, 268), label="observerblackout:")
        self.var_observerblackout = wx.Choice(self, pos=(280, 266), size=(75, 22), choices=["False", "True", ""])
        self.t_gren_explodeonimpact = wx.StaticText(self, pos=(10, 292), label="gren_explodeonimpact:")
        self.var_gren_explodeonimpact = wx.Choice(self, pos=(280, 290), size=(75, 22), choices=["False", "True", ""])
        self.t_guntemp_2 = wx.StaticText(self, pos=(10, 316), label="Guntemp (Decrease, set to False for jump maps):")
        self.var_guntemp_2 = wx.Choice(self, pos=(280, 314), size=(75, 22), choices=["False", "True", ""])
        self.b_manage=wx.Button(self, pos=(100, 370), label="Save cvars (not specified will be skipped)", size=(280, 28))
        self.b_cancel=wx.Button(self, pos=(10, 370), label="Cancel", size=(85, 28))
        try:
            self.slist.SetSelection(0)
        except:
            pass
        #self.Bind(wx.EVT_BUTTON, self.OnRent, self.b_rent)
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.b_select)
        self.Bind(wx.EVT_BUTTON, self.OnCvars, self.b_manage)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.b_cancel)
        self.DisableAll('blablabla')
    
    def OnCancel(self, e):
        self.DefAll('blabla')
        self.DisableAll('blabla')
        self.slist.Enable()

    def DisableAll(self, e):
        self.var_password.Disable()
        self.var_login.Disable()
        self.var_flagmustbeatbase.Disable()
        self.var_elim.Disable()
        self.var_observerblackout.Disable()
        self.var_fraglimit.Disable()
        self.var_timelimit.Disable()
        self.var_flagcapendsround.Disable()
        self.var_fraglimit.Disable()
        self.var_sv_gravity.Disable()
        self.var_guntemp.Disable()
        self.var_guntemp_2.Disable()
        self.var_gren_explodeonimpact.Disable()
        self.b_manage.Disable()
        self.b_cancel.Disable()

    def DefAll(self, e):
        self.var_flagmustbeatbase.SetStringSelection('')
        self.var_elim.Clear()
        self.var_observerblackout.SetStringSelection('')
        self.var_fraglimit.Clear()
        self.var_timelimit.Clear()
        self.var_flagcapendsround.SetStringSelection('')
        self.var_observerblackout.SetStringSelection('')
        self.var_sv_gravity.Clear()
        self.var_guntemp.SetStringSelection('')


    def RefreshServers(self, e):
        self.serverlist=[]
        self.serverinfo=[]
        for i in serverinfom:
           hx=i[1]
           if doesrun(hx):
              self.serverinfo.append(i)
              self.serverlist.append(i[0]+' (%s)' % i[-5])  
        self.slist.Destroy()
        self.slist = wx.Choice(self, pos=(10, 8), choices=self.serverlist, size=(323, 22)) 
        try:
            self.slist.SetSelection(0)
        except:
            pass
        

    def OnCvars(self, e):
        sinfo=self.serverinfo[self.slist.GetSelection()]
        limits=sinfo[-1]
        pw=self.var_password.GetLineText(0)
        login=self.var_login.GetLineText(0)
        errors=""
        pw=re.sub("(\W)", "", pw)
        login=re.sub("(\W)", "", login)
        elim=self.var_elim.GetLineText(0)
        timelimit=self.var_timelimit.GetLineText(0)
        fraglimit=self.var_fraglimit.GetLineText(0)
        sv_gravity=self.var_sv_gravity.GetLineText(0)
        lvar=[]
        nvar=[]
        lim=[]
        req={}
        sidx=sinfo[-2]
        url=sinfo[-3]
        if sinfo[2]:
            if elim!="":
               lvar.append(elim)
               nvar.append("var_elim")
               req["var_elim"]=elim
               lim.append(limits[0])
        if sinfo[3]:
            if self.var_guntemp.GetSelection()==0:
                req["var_guntemp_inc"]="0"
            if self.var_guntemp.GetSelection()==1:
                req["var_guntemp_inc"]="11"
        if sinfo[4]:
            if self.var_flagcapendsround.GetSelection()==0:
                req["var_flagcapendsround"]="false"
            if self.var_flagcapendsround.GetSelection()==1:
                req["var_flagcapendsround"]="true"
        if sinfo[5]:
            if self.var_flagmustbeatbase.GetSelection()==0:
                req["var_flagmustbeatbase"]="false"
            if self.var_flagmustbeatbase.GetSelection()==1:
                req["var_flagmustbeatbase"]="true"
        if sinfo[6]:
            if timelimit!="":
               lvar.append(timelimit)
               nvar.append("var_timelimit")
               req["var_timelimit"]=timelimit
               lim.append(limits[1])
        if sinfo[7]:
            if fraglimit!="":
               lvar.append(fraglimit)
               nvar.append("var_fraglimit")
               req["var_fraglimit"]=fraglimit
               lim.append(limits[2])
        if sinfo[8]:
            if sv_gravity!="":
               lvar.append(sv_gravity)
               nvar.append("var_sv_gravity")
               req["var_sv_gravity"]=sv_gravity
               lim.append(limits[3])
        if sinfo[9]:
            if self.var_observerblackout.GetSelection()==0:
                req["var_observerblackout"]="false"
            if self.var_observerblackout.GetSelection()==1:
                req["var_observerblackout"]="true"
        if sinfo[10]:
            if self.var_gren_explodeonimpact.GetSelection()==0:
                req["var_gren_explodeonimpact"]="false"
            if self.var_gren_explodeonimpact.GetSelection()==1:
                req["var_gren_explodeonimpact"]="true"
        if sinfo[11]:
            if self.var_guntemp_2.GetSelection()==1:
                req["var_guntemp_dec"]="4"
            if self.var_guntemp_2.GetSelection()==0:
                req["var_guntemp_dec"]="0"
        for i in range(len(lvar)):
            try:
               namex=nvar[i]
               valx=int(lvar[i])
               limx=lim[i]
               maxx=limx[1]
               minx=limx[0]
               req[namex]=str(valx)
               if valx<minx:
                  errors=errors+"ERROR: The value of \"%s\" must be equal to or greater than %s.\n" % (namex, minx)
               if valx>maxx:
                  errors=errors+"ERROR: The value of \"%s\" must be equal to or less than %s.\n" % (namex, maxx)

            except:
               errors=errors+"ERROR: The value of \"%s\" must be integer, not string.\n" % namex
        ok.rp.txt.Clear()
        if errors=="":
            r=urllib.urlopen(url+"%s?server=%s&login=%s" % (sinfo[-6], sidx, self.login), urllib.urlencode(req.items()))
            txt2=r.read()
            if txt2.find('errors')!=-1:
               ok.rp.txt.WriteText("An unknown error has occured.")
            else:
               self.OnCancel('blabla')
               return
        else:
            ok.rp.txt.WriteText(errors)
        ok.Disable()
        ok.rp.Centre()
        ok.rp.Show()

    def OnStart(self, e):
        sid=self.slist.GetSelection()
        if sid==wx.NOT_FOUND:
            return
        self.DefAll('blabla')
        ok.Disable()
        ok.mp.Centre()
        ok.mp.Show()

    def OnManage(self):
        sid=self.slist.GetSelection()
        self.b_manage.Enable()
        self.b_cancel.Enable()
        self.slist.Disable()
        sinfo=self.serverinfo[sid]
        if sinfo[2]:
            self.var_elim.Enable()
        else:
            self.var_elim.Disable()
        if sinfo[3]:
            self.var_guntemp.Enable()
        else:
            self.var_guntemp.Disable()
        if sinfo[4]:
            self.var_flagcapendsround.Enable()
        else:
            self.var_flagcapendsround.Disable()
        if sinfo[5]:
            self.var_flagmustbeatbase.Enable()
        else:
            self.var_flagmustbeatbase.Disable()
        if sinfo[6]:
            self.var_timelimit.Enable()
        else:
            self.var_timelimit.Disable()
        if sinfo[7]:
            self.var_fraglimit.Enable()
        else:
            self.var_fraglimit.Disable()
        if sinfo[8]:
            self.var_sv_gravity.Enable()
        else:
            self.var_sv_gravity.Disable()
        if sinfo[9]:
            self.var_observerblackout.Enable()
        else:
            self.var_observerblackout.Disable()
        if sinfo[10]:
            self.var_gren_explodeonimpact.Enable()
        else:
            self.var_gren_explodeonimpact.Disable()
        if sinfo[11]:
            self.var_guntemp_2.Enable()
        else:
            self.var_guntemp_2.Disable()
        
class ManagePopup(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Server Rent", style=wx.CAPTION | wx.SYSTEM_MENU | wx.STAY_ON_TOP, size=(300, 100))
        p=wx.Panel(self, -1)
        p.SetBackgroundColour("white")
        self.pleasetypethelogin=wx.StaticText(p, pos=(20, 0), label="Please type the login password for this server:")
        self.wrong=wx.StaticText(p, pos=(20, 0), label="Wrong password/Server is empty")
        self.wrong.Hide()
        self.txt=wx.TextCtrl(p, size=(270, 22), pos=(10, 20))
        b=wx.Button(p, label="OK", size=(100, 28), pos=(100, 44))
        self.Bind(wx.EVT_BUTTON, self.OnOk)
    def OnOk(self, e):
        sinf=ok.page2.serverinfo
        sinf=sinf[ok.page2.slist.GetSelection()]
        r=urllib.urlopen(sinf[-3]+"cvars.php?server=%s&login=%s" % (sinf[-2], self.txt.GetLineText(0)))
        if r.read().find('errors')==wx.NOT_FOUND:
            ok.page2.login=self.txt.GetLineText(0)
            ok.page2.OnManage()
            ok.Enable()
            self.Hide()
        else:
            self.txt.Disable()
            self.pleasetypethelogin.Hide()
            self.wrong.Show()
            self.Bind(wx.EVT_BUTTON, self.OnOk2)
    def OnOk2(self, e):
        ok.Enable()
        self.txt.Enable()
        self.txt.Clear()
        self.Bind(wx.EVT_BUTTON, self.OnOk)
        self.wrong.Hide()
        self.pleasetypethelogin.Show()
        self.Hide()

class RentPopup(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Server Rent", style=wx.CAPTION | wx.SYSTEM_MENU | wx.STAY_ON_TOP, size=(400, 150))
        p=wx.Panel(self, -1)
        p.SetBackgroundColour("white")
        self.txt=wx.TextCtrl(p, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_NO_VSCROLL, size=(400, 95), pos=(0, 0))
        b=wx.Button(p, label="OK", size=(100, 28), pos=(150, 95))
        self.Bind(wx.EVT_BUTTON, self.OnOk)
    def OnOk(self, e):
        ok.Enable()
        self.Hide()
        

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs) 
        self.InitUI()
        
    def InitUI(self):
        if exists('qr_icon.ico'):
            self.SetIcon(wx.Icon("qr_icon.ico",wx.BITMAP_TYPE_ICO))
        self.mp=ManagePopup(self)
        self.rp=RentPopup(self)
        self.p = wx.Panel(self, -1)
        self.p.SetBackgroundColour("white")
        self.nb = wx.Notebook(self.p, -1)
        self.page1 = panel_RentStd(self.nb)
        self.page2 = panel_Manage(self.nb)
        self.nb.AddPage(self.page1, "Rent A Server", select=True)
        self.nb.AddPage(self.page2, "Change Cvars")
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.nb,1,wx.EXPAND)
        self.p.SetSizer(self.sizer)
        #wx.CallAfter(
        #nb.Refresh()#)
        
def main():
    global tim
    global ok
    app = wx.App()
    ok=MainWindow(None, title="Quick Rent v1.1", style=wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.CAPTION | wx.SYSTEM_MENU, size=(410, 460))
    ok.Show()
    tim = wx.Timer()
    def onTimer(e):
       global tim
       loadx()
       ok.page1.RefreshServers('blabla')
       ok.page2.RefreshServers('blabla')
       tim.Stop()
    tim.Bind(wx.EVT_TIMER,onTimer)
    tim.Start()
    app.MainLoop()

def loadx():
 global ok
 global serverinfom
 global serverinfox
 serverinfox=[]
 serverinfom=[]
 try:
    mirrors=open('mirrors.txt', 'w+')
    mirrors.write(urllib.urlopen('http://htmldp.com/qr/mirrors.txt').read())
 except:
    pass
 mirrors.close()
 try:
    mirrors=open('mirrors.txt', 'r')
    mir=mirrors.read().split('\n')
    if mir[-1]=='':
        mir.pop()
    mirrors.close()
 except Exception as e:
    mirrors=open('mirrors.txt', 'w+')
    mirrors.write('http://htmldp.com/qr/')
    mir=['http://htmldp.com/qr/']
    mirrors.close()
 for i in mir:
    try:
        txt=urllib.urlopen(i+'serverinfox.txt').read()
        if txt.find(';')!=-1:
            txt=txt.split(';')[0]
        exec('global serverinfox;serverinfox = %s' % txt)
        txt=urllib.urlopen(i+'serverinfom.txt').read()
        if txt.find(';')!=-1:
            txt=txt.split(';')[0]
        exec('global serverinfom;serverinfom = %s' % txt)
        break
    except:
        pass
    
if __name__ == "__main__":
    main()
