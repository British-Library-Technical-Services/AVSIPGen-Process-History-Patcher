# GUI Application to copy the Process History from one SIP to another
# The script requires config.py to run
# A compiled stand-alone executable version is available to download from [url]


from requests.packages import urllib3
import wx
import time
import requests
import json
import config

# Mutes SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# GUI framework
class MainFrame(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER | wx.STAY_ON_TOP,
                         title="PM Patcher", size=(200, 240))

        panel = wx.Panel(self)

        self.status = 200
        self.URL = config.URL

        src_text = wx.StaticText(panel, label='SOURCE ID')
        self.src_id = wx.TextCtrl(panel, style=wx.TE_CENTRE)

        dest_text = wx.StaticText(panel, label='DESTINATION ID')
        self.dest_id = wx.TextCtrl(panel, style=wx.TE_CENTRE)

        button = wx.Button(panel, label='<< PATCH >>', size=(150, 60))
        button.Bind(wx.EVT_BUTTON, self.on_press)

        self.gauge = wx.Gauge(panel, range=20, size=(110, 10), style=wx.GA_HORIZONTAL)
        self.count = 1

        v_box = wx.BoxSizer(wx.VERTICAL)
        v_box.Add(src_text, 0, wx.TOP | wx.CENTRE, 5)
        v_box.Add(self.src_id, 0, wx.BOTTOM | wx.CENTRE, 5)
        v_box.Add(dest_text, 0, wx.ALL | wx.CENTRE)
        v_box.Add(self.dest_id, 0, wx.BOTTOM | wx.CENTRE, 5)
        v_box.Add(button, 0, wx.TOP | wx.CENTRE, 5)
        v_box.Add(self.gauge, 0, wx.ALL | wx.CENTRE, 5)

        v_box.Add((-1, 25))

        panel.SetSizer(v_box)

        self.report = self.CreateStatusBar(1)
        self.Show()

        self.src_sip_id = None
        self.dest_sip_id = None

    def on_press(self, event):
        self.src_sip_id = self.src_id.GetValue()
        self.dest_sip_id = self.dest_id.GetValue()

        self.status_check()

    # Function to capture process metadata from source SIP
    def status_check(self):
        src_url = "{}/SIP/{}".format(self.URL, self.src_sip_id)
        src_get = requests.get(src_url, verify=False)
        self.status = src_get.status_code

        if self.status == 200:
            self.report.PushStatusText('{}: SIP ID OKAY'.format(self.status))
            self.patchPM(src_get)
            self.count = 20
            self.gauge.SetValue(self.count)
            time.sleep(1)
            self.count = 0
            self.gauge.SetValue(self.count)
            self.report.PushStatusText('SUCCESS')
            time.sleep(3)
            self.report.PushStatusText('')
        else:
            self.report.PushStatusText('{}: ERROR'.format(self.status))
            time.sleep(3)
            self.report.PushStatusText('')

    # Function to Patch (copy) the process metadata to the destination SIP
    def patchPM(self, src_get):
        src_get.encoding = src_get.apparent_encoding
        src_json = src_get.json()

        d = json.loads(src_json['ProcessMetadata'])

        dest_url = '{}/SIP/{}'.format(self.URL, self.dest_sip_id)
        dest_req = requests.get(dest_url, verify=False)
        dest_json = dest_req.json()

        dest_process_metadata = json.dumps(d)
        dest_user_id = dest_json['UserId']

        for x in dest_json['StepStates']:
            if x['StepTitle'] == 'Process Metadata':
                dest_step_id = x['StepStateId']

        patch_url = '{}/SIP/processmetadata/{}/{}/{}/true'.format(
            self.URL,
            self.dest_sip_id,
            dest_step_id,
            dest_user_id
        )

        r = requests.patch(
            patch_url,
            json=dest_process_metadata,
            verify=False
        )


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
