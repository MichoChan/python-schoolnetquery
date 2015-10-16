import urllib2,urllib
import cookielib
import re
import wx

def Browser(url,user,password):
    try:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        postdata = urllib.urlencode({
            'username':user,
            'password':password,
            'reffer':'http://www2.ahnu.edu.cn/home/'
            }
            )
        headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                'Referer':'http://nic.ahnu.edu.cn/cgi-bin/service'
            }
        req = urllib2.Request(url,data=postdata,headers=headers)
        opener.open(req)
        postdata = urllib.urlencode({
            'username':user,
            'password':password,
            #'credential':'F2732E78B8C7E236E859BEAB3B8739F64AAA8C057BF6556FB425791718AFF75C',
            'echo':'分担费查询'
            }
            )
        req = urllib2.Request(url,data=postdata,headers=headers)
        rlt=opener.open(req)
        return rlt.read()
    except Exception,e:
        print str(e)


def query(event):    
    usr = usrin.GetValue()
    pwd = pwdin.GetValue()    
    page = Browser('http://nic.ahnu.edu.cn/cgi-bin/service',usr,pwd)
    rule = 'right">(.*?)</'
    ans = re.findall(rule,page)
    if ans==[]:
        out.SetValue('请输入有效的帐户名和密码!')
        return 
    su = 0.0
    for i in ans[:2]:
        s = ''
        for j in i:
            if j!=',':
                s+=j
        su = su+int(s)
    s = int(su/(2**30)*100)/100.0
    out.SetValue(str(s)+'G')
    
if __name__ == '__main__':
    app = wx.App()
    win = wx.Frame(None,title='校园网费用查询',size=(250,180))

    bkg = wx.Panel(win)

    usrlabel = wx.StaticText(bkg,-1,'账户',(100,10))
    pwdlabel = wx.StaticText(bkg,-1,'密码',(100,10))

    usrin = wx.TextCtrl(bkg,value='cj1207')
    pwdin = wx.TextCtrl(bkg,value='120705008',style=wx.TE_PASSWORD)
    
    ubox = wx.BoxSizer()
    ubox.Add(usrlabel,proportion=0,flag=wx.LEFT,border=5)
    ubox.Add(usrin,proportion=1,flag=wx.LEFT,border=5)
    
    pbox = wx.BoxSizer()
    pbox.Add(pwdlabel,proportion=0,flag=wx.LEFT,border=5)
    pbox.Add(pwdin,proportion=1,flag=wx.LEFT,border=5,)

    out = wx.TextCtrl(bkg)

    qryButton = wx.Button(bkg,label='查询')
    qryButton.Bind(wx.EVT_BUTTON,query)    
    
    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(ubox,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
    vbox.Add(pbox,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
    vbox.Add(qryButton,proportion=0,flag=wx.EXPAND|wx.ALL,border=5) 
    vbox.Add(out,proportion=1,flag=wx.EXPAND|wx.ALL,border=5) 
    
    bkg.SetSizer(vbox)
    win.Show()
    app.MainLoop()
