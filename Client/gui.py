#!/usr/bin/python3

from tkinter import*
from tkinter import messagebox
from values import *
from hexapod_connection import*
import hardcoded_movements
import sys

ENGINES = {
    "rrh": REAR_R_HORI,
    "rrv": REAR_R_VERT,
    "rrk": REAR_R_KNEE,
    "rlh": REAR_L_HORI,
    "rlv": REAR_L_VERT,
    "rlk": REAR_L_KNEE,
    "mrh": MIDD_R_HORI,
    "mrv": MIDD_R_VERT,
    "mrk": MIDD_R_KNEE,
    "mlh": MIDD_L_HORI,
    "mlv": MIDD_L_VERT,
    "mlk": MIDD_L_KNEE,
    "frh": FRON_R_HORI,
    "frv": FRON_R_VERT,
    "frk": FRON_R_KNEE,
    "flh": FRON_L_HORI,
    "flv": FRON_L_VERT,
    "flk": FRON_L_KNEE
}

class RadiobuttonGroup:
    def __init__(self, vals, etiqs, default_value, row, fen):
        if len(vals) != len(etiqs):
            print("len differs")
            exit(1)
        self.var = StringVar()
        self.var.set(default_value)
        self.btn = []
        for i in range(len(vals)):
            self.btn.append(Radiobutton(fen, variable=self.var, text=etiqs[i], value=vals[i]))
            self.btn[i].grid(column=1 + i, row=row)

    def get(self):
        return self.var.get()

    def disable(self):
        for i in self.btn:
            i.config(state='disable')

    def enable(self):
        for i in self.btn:
            i.config(state='normal')

class Gui:
    def __init__(self, mode):
        self.fen = Tk()

        self.fen.geometry("1280x520")
        self.fen.title("Hexapod Client")
        self.connection = HexapodConnection(mode=mode)
        self.hardcoded_movements = hardcoded_movements.HardcodedMovements(self.connection)

        self.btn_side = RadiobuttonGroup(['l', 'r'], ['Left', 'Right'], 'l', 1, self.fen)
        self.btn_zone = RadiobuttonGroup(['f', 'm', 'r'], ['Front', 'Middle', 'Rear'], 'f', 2, self.fen)
        self.btn_type = RadiobuttonGroup(['k', 'v', 'h'], ['Knee', 'Verti', 'Hori'], 'k', 3, self.fen)

        # Type all
        self.type_all = IntVar()
        self.btn_all = Checkbutton(self.fen, text="All type", variable=self.type_all, command=self.disable_toggle)
        self.btn_all.grid(row=3, column=5)

        # live
        self.live_var = IntVar()
        self.btn_live = Checkbutton(self.fen, text="Live", variable=self.live_var, command=self.change_send_btn_state)
        self.btn_live.grid(row=3, column=6)

        # angle
        self.angle = DoubleVar()
        self.angle.set(0.5)
        self.custom_angle = IntVar()
        self.btn_enable_custom_angle = Checkbutton(self.fen, text="use custom", variable=self.custom_angle, command=self.change_angle_scale_state)
        self.btn_enable_custom_angle.grid(row=5, column=2)
        self.custom_angle_ent = Entry(self.fen, width=5, textvariable=self.angle, state='disable')
        self.custom_angle_ent.grid(column=1, row=5)
        self.scale_angle = Scale(self.fen, orient='horizontal', from_=0, to=1, resolution=0.05, tickinterval=0.05, length=800, variable=self.angle, command=self.send_live)
        self.scale_angle.grid(column=1, row=4, columnspan=8)
        self.angle_equivalent = IntVar()
        self.set_angle_equivalent()
        Label(self.fen, text="Angle Equivalent  --> ").grid(column=7, row=5)
        self.label_angle_equivalent = Label(self.fen, textvariable=self.angle_equivalent)
        self.label_angle_equivalent.grid(column=8, row=5)

        # min/max scale
        self.min_max_enable = IntVar()
        self.min_max_enable.set(0)
        self.btn_enable_custom_minmax = Checkbutton(self.fen, text="use custom min/max", variable=self.min_max_enable, command=self.change_min_max_state)
        self.btn_enable_custom_minmax.grid(row=1, column=9)

        self.min_scale = Scale(self.fen, orient='vertical', from_=0, to=3000, resolution=50, tickinterval=200, length=500, label='min', state='disable')
        self.min_scale.grid(column=10, row=1, rowspan=12)
        self.max_scale = Scale(self.fen, orient='vertical', from_=0, to=3000, resolution=50, tickinterval=200, length=500, label='max', state='disable')
        self.max_scale.grid(column=11, row=1, rowspan=12)

        # speed
        self.speed = IntVar()
        self.speed.set(1500)
        self.custom_speed = IntVar()
        self.btn_enable_custom_speed = Checkbutton(self.fen, text="use custom", variable=self.custom_speed, command=self.change_speed_scale_state)
        self.btn_enable_custom_speed.grid(row=7, column=2)
        self.custom_speed_ent = Entry(self.fen, width=5, textvariable=self.speed, state='disable')
        self.custom_speed_ent.grid(column=1, row=7)
        self.scale_speed = Scale(self.fen, orient='horizontal', from_=0, to=3000, resolution=50, tickinterval=200, length=800, variable=self.speed)
        self.scale_speed.grid(column=1, row=6, columnspan=8)

        # actions
        self.action_btn = ["sit", "stand", "stand1", "stand2", "stand3", "wave", "dab", "forward", "stop"]
        for i in range(len(self.action_btn)):
            Button(self.fen, text=self.action_btn[i], command=getattr(self.hardcoded_movements, self.action_btn[i])).grid(row=9, column=i+1, pady=10)

        # Ok
        self.btn_send = Button(self.fen, text="send", command=self.send)
        self.btn_send.grid(column=1, row=10 ,columnspan=8, pady=20)

        self.fen.bind_all("<Escape>", self.quit)
        self.fen.mainloop()

    def change_min_max_state(self):
        if self.min_max_enable.get() == 1:
            self.min_scale.config(state='normal')
            self.max_scale.config(state='normal')
        else:
            self.min_scale.config(state='disable')
            self.max_scale.config(state='disable')

    def set_angle_equivalent(self):
        angle = float(self.angle.get())
        engine = ENGINES[self.btn_zone.get() + self.btn_side.get() + self.btn_type.get()]
        self.btn_type.get()
        val = self.convert_angle(angle, engine, self.btn_type.get())
        self.angle_equivalent.set(val)

    def change_angle_scale_state(self, event=None):
        if self.custom_angle.get() == 1:
            self.live_var.set(0)
            self.btn_live.config(state='disable')
            self.btn_send.config(state='normal')
            self.custom_angle_ent.config(state='normal')
        else:
            self.btn_live.config(state='normal')
            self.custom_angle_ent.config(state='disable')

    def change_speed_scale_state(self, event=None):
        if self.custom_speed.get() == 1:
            self.custom_speed_ent.config(state='normal')
        else:
            self.custom_speed_ent.config(state='disable')

    def disable_toggle(self):
        if self.type_all.get() == 1:
            self.btn_side.disable()
            self.btn_zone.disable()
        else:
            self.btn_side.enable()
            self.btn_zone.enable()

    def change_send_btn_state(self):
        if self.live_var.get() == 1:
            self.btn_send.config(state='disable')
        else:
            self.btn_send.config(state='normal')

    def convert_angle(self, angle, engine, kind):
        side = engine <= 15   # We need to know which side the engine is on
        if kind == "v":
            vals = VERT_VALUES
        elif kind == "h":
            vals = HORI_VALUES
        else: # k
            vals = KNEE_VALUES
        return angle * (vals[side][0] - vals[side][1]) + vals[side][1]

    def send_live(self, event=None):
        if self.live_var.get() == 1:
            self.send()

    def send(self, event=None):
        angle = float(self.angle.get())
        speed = int(self.speed.get())

        engine = ENGINES[self.btn_zone.get() + self.btn_side.get() + self.btn_type.get()]
        command = ""

        if self.type_all.get() == 1:
            initial_angle = angle
            for key, value in ENGINES.items():
                if self.btn_type.get() not in key:
                    continue
                angle = self.convert_angle(initial_angle, value, key[2])
                if command != "":
                    command += " "
                command += "#%dP%.0fS%d" % (value, angle, speed)
            command += '!'
        else:
            angle = self.convert_angle(angle, engine, self.btn_type.get())
            command = "#%dP%.0fS%d!" % (engine, angle, speed)   # Command to send
        self.connection.send_command(command, 0)

    def quit(self, event=None):
        self.fen.quit()
        self.fen.destroy()

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "--wire":
        Gui("wire")
    else:
        print("Use --wire if you want to connect using a wire\n")
        Gui("wifi")
