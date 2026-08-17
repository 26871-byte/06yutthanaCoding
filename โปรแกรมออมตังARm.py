from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Ellipse, RoundedRectangle, Line
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.clock import Clock


# ============================================================
# ข้อมูลเริ่มต้น
# ============================================================

START_INCOME = 12300.0
START_EXPENSE = 7450.0


# ============================================================
# กราฟวงกลม
# ============================================================

class PieChart(Widget):

    income = NumericProperty(12300)
    expense = NumericProperty(7450)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(
            pos=self.draw,
            size=self.draw,
            income=self.draw,
            expense=self.draw
        )

        Clock.schedule_once(
            lambda dt: self.draw(),
            0.1
        )

    def draw(self, *args):

        self.canvas.clear()

        total = self.income + self.expense

        if total <= 0:
            return

        with self.canvas:

            # พื้นหลังวงกลม
            Color(
                0.93,
                0.94,
                0.97,
                1
            )

            Ellipse(
                pos=self.pos,
                size=(self.width, self.width)
            )

            # รายรับ
            income_angle = (
                self.income / total
            ) * 360

            Color(
                0.16,
                0.73,
                0.49,
                1
            )

            Ellipse(
                pos=self.pos,
                size=(self.width, self.width),
                angle_start=0,
                angle_end=income_angle
            )

            # รายจ่าย
            Color(
                0.94,
                0.36,
                0.42,
                1
            )

            Ellipse(
                pos=self.pos,
                size=(self.width, self.width),
                angle_start=income_angle,
                angle_end=360
            )

            # วงกลมตรงกลาง
            center_size = self.width * 0.55

            Color(
                1,
                1,
                1,
                1
            )

            Ellipse(
                pos=(
                    self.x + (self.width - center_size) / 2,
                    self.y + (self.height - center_size) / 2
                ),
                size=(
                    center_size,
                    center_size
                )
            )


# ============================================================
# การ์ดรายการเงิน
# ============================================================

class TransactionRow(BoxLayout):

    def __init__(
        self,
        title,
        category,
        amount,
        transaction_type,
        icon,
        **kwargs
    ):

        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(65),
            spacing=dp(10),
            padding=[
                dp(8),
                dp(5),
                dp(8),
                dp(5)
            ],
            **kwargs
        )

        # Icon
        icon_box = BoxLayout(
            size_hint_x=None,
            width=dp(45)
        )

        icon_label = Label(
            text=icon,
            font_size=dp(22),
            color=(0.25, 0.28, 0.38, 1)
        )

        icon_box.add_widget(icon_label)

        self.add_widget(icon_box)

        # รายละเอียด
        info = BoxLayout(
            orientation="vertical"
        )

        info.add_widget(
            Label(
                text=title,
                color=(0.15, 0.17, 0.24, 1),
                font_size=dp(14),
                halign="left",
                valign="middle"
            )
        )

        info.add_widget(
            Label(
                text=category,
                color=(0.55, 0.58, 0.66, 1),
                font_size=dp(10),
                halign="left",
                valign="middle"
            )
        )

        self.add_widget(info)

        # จำนวนเงิน
        sign = "+" if transaction_type == "income" else "-"
        color = (
            (0.10, 0.70, 0.43, 1)
            if transaction_type == "income"
            else
            (0.92, 0.30, 0.37, 1)
        )

        self.add_widget(
            Label(
                text=f"{sign} ฿{amount:,.2f}",
                color=color,
                font_size=dp(13),
                size_hint_x=None,
                width=dp(100),
                halign="right"
            )
        )


# ============================================================
# Dashboard
# ============================================================

class HomeScreen(Screen):

    def on_enter(self):

        app = App.get_running_app()

        self.refresh()


    def refresh(self):

        app = App.get_running_app()

        balance = (
            app.total_income -
            app.total_expense
        )

        self.ids.balance.text = (
            f"฿ {balance:,.2f}"
        )

        self.ids.income.text = (
            f"฿ {app.total_income:,.2f}"
        )

        self.ids.expense.text = (
            f"฿ {app.total_expense:,.2f}"
        )

        self.ids.pie.income = (
            app.total_income
        )

        self.ids.pie.expense = (
            app.total_expense
        )

        self.refresh_transactions()


    def refresh_transactions(self):

        container = self.ids.transaction_list

        container.clear_widgets()

        app = App.get_running_app()

        for item in app.transactions[:6]:

            row = TransactionRow(
                title=item["title"],
                category=item["category"],
                amount=item["amount"],
                transaction_type=item["type"],
                icon=item["icon"]
            )

            container.add_widget(row)


# ============================================================
# หน้ารายการ
# ============================================================

class TransactionScreen(Screen):

    def on_enter(self):
        self.refresh()

    def refresh(self):

        container = self.ids.all_transactions

        container.clear_widgets()

        app = App.get_running_app()

        for item in app.transactions:

            row = TransactionRow(
                title=item["title"],
                category=item["category"],
                amount=item["amount"],
                transaction_type=item["type"],
                icon=item["icon"]
            )

            container.add_widget(row)


# ============================================================
# หน้าเป้าหมาย
# ============================================================

class GoalScreen(Screen):

    def on_enter(self):
        self.refresh()

    def refresh(self):

        container = self.ids.goal_list

        container.clear_widgets()

        app = App.get_running_app()

        for goal in app.goals:

            total = goal["target"]

            saved = goal["saved"]

            percentage = (
                saved / total
                if total > 0
                else 0
            )

            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(105),
                padding=dp(12),
                spacing=dp(5)
            )

            # พื้นหลัง
            with card.canvas.before:

                Color(
                    1,
                    1,
                    1,
                    1
                )

                card.bg = RoundedRectangle(
                    pos=card.pos,
                    size=card.size,
                    radius=[dp(15)]
                )

            card.bind(
                pos=lambda obj, value:
                    setattr(
                        obj.bg,
                        "pos",
                        value
                    )
            )

            card.bind(
                size=lambda obj, value:
                    setattr(
                        obj.bg,
                        "size",
                        value
                    )
            )

            title = BoxLayout(
                orientation="horizontal"
            )

            title.add_widget(
                Label(
                    text=goal["icon"],
                    font_size=dp(22),
                    size_hint_x=None,
                    width=dp(45)
                )
            )

            title.add_widget(
                Label(
                    text=goal["name"],
                    color=(0.15, 0.17, 0.24, 1),
                    font_size=dp(14),
                    halign="left"
                )
            )

            title.add_widget(
                Label(
                    text=f"{percentage * 100:.0f}%",
                    color=(0.40, 0.38, 0.90, 1),
                    font_size=dp(12),
                    size_hint_x=None,
                    width=dp(45)
                )
            )

            card.add_widget(title)

            progress = ProgressWidget(
                value=percentage
            )

            card.add_widget(progress)

            card.add_widget(
                Label(
                    text=(
                        f"เก็บแล้ว ฿{saved:,.0f}"
                        f" / ฿{total:,.0f}"
                    ),
                    color=(0.55, 0.58, 0.66, 1),
                    font_size=dp(10),
                    halign="left"
                )
            )

            container.add_widget(card)


# ============================================================
# Progress Bar
# ============================================================

class ProgressWidget(Widget):

    value = NumericProperty(0)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.bind(
            pos=self.draw,
            size=self.draw,
            value=self.draw
        )

        Clock.schedule_once(
            lambda dt: self.draw(),
            0.1
        )

    def draw(self, *args):

        self.canvas.clear()

        with self.canvas:

            # พื้น
            Color(
                0.91,
                0.92,
                0.96,
                1
            )

            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(5)]
            )

            # progress
            Color(
                0.40,
                0.39,
                0.90,
                1
            )

            RoundedRectangle(
                pos=self.pos,
                size=(
                    self.width *
                    max(0, min(1, self.value)),
                    self.height
                ),
                radius=[dp(5)]
            )


# ============================================================
# หน้าโปรไฟล์
# ============================================================

class ProfileScreen(Screen):
    pass


# ============================================================
# เพิ่มรายการ Popup
# ============================================================

class AddTransactionPopup(Popup):

    def save(self):

        amount_text = self.ids.amount.text.strip()

        title = self.ids.title.text.strip()

        category = self.ids.category.text

        transaction_type = (
            self.ids.type_spinner.text
        )

        if not amount_text:

            self.ids.error.text = (
                "กรุณากรอกจำนวนเงิน"
            )

            return

        try:

            amount = float(
                amount_text
            )

        except ValueError:

            self.ids.error.text = (
                "จำนวนเงินต้องเป็นตัวเลข"
            )

            return

        if amount <= 0:

            self.ids.error.text = (
                "จำนวนเงินต้องมากกว่า 0"
            )

            return

        if not title:

            title = category

        app = App.get_running_app()

        if transaction_type == "รายรับ":

            app.total_income += amount

            transaction_type_value = "income"

            icon = "💰"

        else:

            app.total_expense += amount

            transaction_type_value = "expense"

            icon = app.category_icons.get(
                category,
                "💸"
            )

        app.transactions.insert(
            0,
            {
                "title": title,
                "category": category,
                "amount": amount,
                "type": transaction_type_value,
                "icon": icon
            }
        )

        self.dismiss()

        app.refresh_all()


# ============================================================
# KV Layout
# ============================================================

KV = r'''

#:import dp kivy.metrics.dp

<RoundButton@Button>:
    background_color: 0,0,0,0
    color: 1,1,1,1
    font_size: dp(14)
    bold: True

<MainLabel@Label>:
    color: .15,.17,.24,1
    font_size: dp(16)

<AddTransactionPopup>:

    title: "เพิ่มรายการ"
    size_hint: .92, None
    height: dp(500)
    auto_dismiss: False

    background_color: 1,1,1,1

    BoxLayout:

        orientation: "vertical"
        padding: dp(20)
        spacing: dp(12)

        Label:
            text: "เพิ่มรายการเงิน"
            font_size: dp(21)
            bold: True
            color: .15,.17,.24,1
            size_hint_y: None
            height: dp(40)

        Spinner:
            id: type_spinner
            text: "รายรับ"
            values: ["รายรับ", "รายจ่าย"]
            size_hint_y: None
            height: dp(45)

        TextInput:
            id: amount
            hint_text: "จำนวนเงิน เช่น 150"
            input_filter: "float"
            multiline: False
            size_hint_y: None
            height: dp(45)

        Spinner:
            id: category
            text: "อาหาร"
            values:
                [
                "อาหาร",
                "เครื่องดื่ม",
                "การเดินทาง",
                "การเรียน",
                "ช้อปปิ้ง",
                "อื่น ๆ"
                ]
            size_hint_y: None
            height: dp(45)

        TextInput:
            id: title
            hint_text: "รายละเอียด เช่น ข้าวกลางวัน"
            multiline: False
            size_hint_y: None
            height: dp(45)

        Label:
            id: error
            text: ""
            color: .9,.2,.25,1
            font_size: dp(11)
            size_hint_y: None
            height: dp(25)

        Widget:

        BoxLayout:
            size_hint_y: None
            height: dp(45)
            spacing: dp(10)

            Button:
                text: "ยกเลิก"
                on_release: root.dismiss()

            Button:
                text: "บันทึก"
                background_color: .40,.39,.90,1
                on_release: root.save()


<ProgressWidget>:
    size_hint_y: None
    height: dp(8)


<HomeScreen>:

    BoxLayout:
        orientation: "vertical"
        spacing: dp(0)

        # Header
        BoxLayout:
            size_hint_y: None
            height: dp(190)
            padding: dp(20)
            orientation: "vertical"

            canvas.before:
                Color:
                    rgba: .40,.39,.90,1

                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [0,0,dp(25),dp(25)]

            BoxLayout:
                size_hint_y: None
                height: dp(40)

                Label:
                    text: "ภาพรวมวันนี้"
                    color: 1,1,1,1
                    font_size: dp(22)
                    bold: True
                    halign: "left"

                Label:
                    text: "👨🏻‍🎓"
                    font_size: dp(24)
                    size_hint_x: None
                    width: dp(50)

            Label:
                text: "จัดการเงินของคุณได้ง่ายขึ้น"
                color: .88,.89,1,1
                font_size: dp(11)
                halign: "left"
                size_hint_y: None
                height: dp(25)

            Label:
                id: header_balance
                text: "฿ 4,850.00"
                color: 1,1,1,1
                font_size: dp(31)
                bold: True
                halign: "left"

        ScrollView:

            do_scroll_x: False

            BoxLayout:

                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(12)
                padding: dp(15)

                # Balance card
                BoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: dp(155)
                    padding: dp(18)
                    spacing: dp(4)

                    canvas.before:
                        Color:
                            rgba: 1,1,1,1

                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(18)]

                    Label:
                        text: "ยอดคงเหลือ"
                        color: .55,.58,.66,1
                        font_size: dp(11)
                        halign: "left"
                        size_hint_y: None
                        height: dp(20)

                    Label:
                        id: balance
                        text: "฿ 4,850.00"
                        color: .15,.17,.24,1
                        font_size: dp(27)
                        bold: True
                        halign: "left"
                        size_hint_y: None
                        height: dp(40)

                    BoxLayout:
                        spacing: dp(8)

                        BoxLayout:
                            orientation: "vertical"
                            padding: dp(10)

                            canvas.before:
                                Color:
                                    rgba: .91,.98,.95,1

                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [dp(12)]

                            Label:
                                text: "รายรับ"
                                color: .55,.58,.66,1
                                font_size: dp(10)
                                halign: "left"

                            Label:
                                id: income
                                text: "฿ 12,300.00"
                                color: .10,.70,.43,1
                                font_size: dp(13)
                                bold: True
                                halign: "left"

                        BoxLayout:
                            orientation: "vertical"
                            padding: dp(10)

                            canvas.before:
                                Color:
                                    rgba: 1,.93,.94,1

                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [dp(12)]

                            Label:
                                text: "รายจ่าย"
                                color: .55,.58,.66,1
                                font_size: dp(10)
                                halign: "left"

                            Label:
                                id: expense
                                text: "฿ 7,450.00"
                                color: .92,.30,.37,1
                                font_size: dp(13)
                                bold: True
                                halign: "left"

                # สรุป
                Label:
                    text: "สรุปเดือนนี้"
                    color: .15,.17,.24,1
                    font_size: dp(17)
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(30)

                BoxLayout:
                    size_hint_y: None
                    height: dp(190)
                    padding: dp(10)

                    canvas.before:
                        Color:
                            rgba: 1,1,1,1

                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(18)]

                    BoxLayout:
                        orientation: "vertical"

                        PieChart:
                            id: pie
                            size_hint_y: None
                            height: dp(125)

                        BoxLayout:
                            size_hint_y: None
                            height: dp(35)

                            Label:
                                text: "● รายรับ"
                                color: .10,.70,.43,1
                                font_size: dp(10)

                            Label:
                                text: "● รายจ่าย"
                                color: .92,.30,.37,1
                                font_size: dp(10)

                # รายการ
                Label:
                    text: "รายการล่าสุด"
                    color: .15,.17,.24,1
                    font_size: dp(17)
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(30)

                BoxLayout:
                    id: transaction_list
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(2)

                # เป้าหมาย
                Label:
                    text: "เป้าหมายของฉัน 🎯"
                    color: .15,.17,.24,1
                    font_size: dp(17)
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(35)

                Label:
                    text: "ดูเป้าหมายการออมได้ที่เมนูด้านล่าง"
                    color: .55,.58,.66,1
                    font_size: dp(11)
                    halign: "left"
                    size_hint_y: None
                    height: dp(35)


<TransactionScreen>:

    BoxLayout:
        orientation: "vertical"

        canvas.before:
            Color:
                rgba: .96,.97,1,1

            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "รายการทั้งหมด"
            size_hint_y: None
            height: dp(70)
            font_size: dp(22)
            bold: True
            color: .15,.17,.24,1

        ScrollView:

            do_scroll_x: False

            BoxLayout:
                id: all_transactions
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(15)
                spacing: dp(5)


<GoalScreen>:

    BoxLayout:
        orientation: "vertical"

        canvas.before:
            Color:
                rgba: .96,.97,1,1

            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "เป้าหมายของฉัน 🎯"
            size_hint_y: None
            height: dp(75)
            font_size: dp(22)
            bold: True
            color: .15,.17,.24,1

        ScrollView:

            do_scroll_x: False

            BoxLayout:
                id: goal_list
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(15)
                spacing: dp(8)


<ProfileScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(25)
        spacing: dp(15)

        canvas.before:
            Color:
                rgba: .96,.97,1,1

            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "👨🏻‍🎓"
            font_size: dp(60)

        Label:
            text: "นักเรียน"
            font_size: dp(22)
            bold: True
            color: .15,.17,.24,1

        Label:
            text: "จัดการเงินให้เป็น เริ่มต้นจากวันนี้"
            font_size: dp(12)
            color: .55,.58,.66,1

        Widget:


<RootWidget>:

    BoxLayout:
        orientation: "vertical"

        ScreenManager:
            id: screens

            HomeScreen:
                name: "home"

            TransactionScreen:
                name: "transactions"

            GoalScreen:
                name: "goals"

            ProfileScreen:
                name: "profile"

        # Bottom navigation
        BoxLayout:
            size_hint_y: None
            height: dp(65)
            spacing: dp(2)

            canvas.before:
                Color:
                    rgba: 1,1,1,1

                Rectangle:
                    pos: self.pos
                    size: self.size

            Button:
                text: "⌂\\nหน้าหลัก"
                background_color: 0,0,0,0
                color: .40,.39,.90,1
                on_release: screens.current = "home"

            Button:
                text: "▤\\nรายการ"
                background_color: 0,0,0,0
                color: .55,.58,.66,1
                on_release: screens.current = "transactions"

            Button:
                text: "🎯\\nเป้าหมาย"
                background_color: 0,0,0,0
                color: .55,.58,.66,1
                on_release: screens.current = "goals"

            Button:
                text: "👤\\nบัญชี"
                background_color: 0,0,0,0
                color: .55,.58,.66,1
                on_release: screens.current = "profile"

            Button:
                text: "+"
                font_size: dp(30)
                bold: True
                background_color: .40,.39,.90,1
                color: 1,1,1,1
                size_hint_x: None
                width: dp(60)
                on_release: app.open_add_popup()


'''


# ============================================================
# Root Widget
# ============================================================

class RootWidget(BoxLayout):

    pass


# ============================================================
# Application
# ============================================================

class FinanceApp(App):

    total_income = START_INCOME

    total_expense = START_EXPENSE

    category_icons = {
        "อาหาร": "🍜",
        "เครื่องดื่ม": "🥤",
        "การเดินทาง": "🚌",
        "การเรียน": "📚",
        "ช้อปปิ้ง": "🛍️",
        "อื่น ๆ": "💰"
    }

    transactions = [
        {
            "title": "ข้าวมันไก่",
            "category": "อาหาร",
            "amount": 45.00,
            "type": "expense",
            "icon": "🍜"
        },
        {
            "title": "รถเมล์",
            "category": "การเดินทาง",
            "amount": 20.00,
            "type": "expense",
            "icon": "🚌"
        },
        {
            "title": "รับค่าขนม",
            "category": "ผู้ปกครอง",
            "amount": 100.00,
            "type": "income",
            "icon": "💰"
        }
    ]

    goals = [
        {
            "name": "iPhone 15",
            "saved": 13750,
            "target": 25000,
            "icon": "📱"
        },
        {
            "name": "เที่ยวญี่ปุ่น",
            "saved": 15000,
            "target": 50000,
            "icon": "🏯"
        },
        {
            "name": "คอร์สเรียนออนไลน์",
            "saved": 4000,
            "target": 5000,
            "icon": "💻"
        }
    ]

    def build(self):

        Builder.load_string(KV)

        root = RootWidget()

        return root

    def open_add_popup(self):

        popup = AddTransactionPopup()

        popup.open()

    def refresh_all(self):

        root = self.root

        if root is None:
            return

        screens = root.ids.screens

        home = screens.get_screen("home")

        home.refresh()

        transaction_screen = (
            screens.get_screen(
                "transactions"
            )
        )

        transaction_screen.refresh()

        goal_screen = (
            screens.get_screen(
                "goals"
            )
        )

        goal_screen.refresh()


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":

    FinanceApp().run()