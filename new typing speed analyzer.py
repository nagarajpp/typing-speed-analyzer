import wx
import time
import random

# --------------------------
# PARAGRAPHS
# --------------------------
paragraphs = [
    "Python is a powerful and easy to learn programming language that is widely used in web development, data science, artificial intelligence, automation, and software testing. Regular practice helps programmers write efficient and readable code.",
    "Typing speed improves with regular practice and focus. Accuracy is just as important as speed because making fewer mistakes saves time. Developing good typing habits early can greatly improve productivity and confidence.",
    "Artificial intelligence is transforming the world by enabling machines to learn from data and make decisions. From healthcare to transportation, AI is helping humans solve complex problems more efficiently than ever before.",
    "Data science requires strong logical thinking, statistical knowledge, and programming skills. By analyzing large amounts of data, data scientists extract meaningful insights that help organizations make informed decisions."
]

LEADERBOARD_FILE = "leaderboard.txt"

# -------------------------------------------------
# LEADERBOARD FUNCTIONS (NO os USED)
# -------------------------------------------------
def save_score(name, wpm, accuracy):
    with open(LEADERBOARD_FILE, "a") as f:
        f.write(f"Name:{name},WPM:{wpm},Accuracy:{accuracy}\n")


def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            raw = [line.strip().split(",") for line in f]
    except FileNotFoundError:
        return []

    data = []
    for row in raw:
        try:
            name = row[0].split("Name:")[1]
            wpm = int(row[1].split("WPM:")[1])
            acc = int(row[2].split("Accuracy:")[1])
            data.append((name, wpm, acc))
        except:
            pass

    data.sort(key=lambda x: x[1], reverse=True)
    return data[:5]

# -------------------------------------------------
# MAIN APP
# -------------------------------------------------
class TypingTest(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Typing Speed Analyzer", size=(800, 600))

        self.running = False
        self.start_time = 0
        self.TEST_TIME = 60

        panel = wx.Panel(self)
        panel.SetBackgroundColour("#121212")
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="⌨ Typing Speed Test")
        title.SetForegroundColour(wx.WHITE)
        title.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        self.timer_label = wx.StaticText(panel, label="Time: 60")
        self.timer_label.SetForegroundColour("#B0B0B0")
        vbox.Add(self.timer_label, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        self.result_label = wx.StaticText(panel, label="WPM: 0   Accuracy: 0%")
        self.result_label.SetForegroundColour(wx.WHITE)
        vbox.Add(self.result_label, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        self.paragraph = random.choice(paragraphs)
        self.para_label = wx.StaticText(panel, label=self.paragraph)
        self.para_label.SetForegroundColour(wx.WHITE)
        self.para_label.Wrap(700)
        vbox.Add(self.para_label, 0, wx.ALL | wx.ALIGN_CENTER, 25)

        self.typing_box = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(700, 140))
        self.typing_box.Bind(wx.EVT_TEXT, self.start_test)
        vbox.Add(self.typing_box, 0, wx.ALIGN_CENTER)

        restart_btn = wx.Button(panel, label="Restart Test")
        restart_btn.Bind(wx.EVT_BUTTON, self.restart)
        vbox.Add(restart_btn, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    # -------------------------------------------------
    # LOGIC
    # -------------------------------------------------
    def start_test(self, event):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_timer()
        self.calculate_results()

    def update_timer(self):
        if self.running:
            elapsed = int(time.time() - self.start_time)
            time_left = self.TEST_TIME - elapsed

            if time_left >= 0:
                self.timer_label.SetLabel(f"Time: {time_left}")
                wx.CallLater(1000, self.update_timer)
            else:
                self.running = False
                self.typing_box.Disable()
                self.show_results()

    def calculate_results(self):
        typed = self.typing_box.GetValue()
        elapsed = max(1, time.time() - self.start_time)

        chars = len(typed)
        self.wpm = int(((chars / 5) / elapsed) * 60)

        correct = sum(
            typed[i] == self.paragraph[i]
            for i in range(min(len(typed), len(self.paragraph)))
        )
        self.accuracy = int((correct / len(typed)) * 100) if typed else 0

        self.result_label.SetLabel(
            f"WPM: {self.wpm}   Accuracy: {self.accuracy}%"
        )

    def show_results(self):
        dlg = wx.TextEntryDialog(self, "Enter your name:", "Test Finished")
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue().strip() or "Unknown"
            save_score(name, self.wpm, self.accuracy)
        dlg.Destroy()

        leaderboard = load_leaderboard()
        msg = "🏆 Leaderboard (Top 5)\n\n"
        for i, (name, wpm, acc) in enumerate(leaderboard, 1):
            msg += f"{i}. {name} — {wpm} WPM — {acc}%\n"

        wx.MessageBox(msg, "Results", wx.OK | wx.ICON_INFORMATION)

    def restart(self, event):
        self.running = False
        self.typing_box.Enable()
        self.typing_box.Clear()

        self.paragraph = random.choice(paragraphs)
        self.para_label.SetLabel(self.paragraph)
        self.para_label.Wrap(700)

        self.timer_label.SetLabel("Time: 60")
        self.result_label.SetLabel("WPM: 0   Accuracy: 0%")

# -------------------------------------------------
# RUN APP
# -------------------------------------------------
app = wx.App()
TypingTest()
app.MainLoop()
