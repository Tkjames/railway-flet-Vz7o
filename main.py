import flet as ft
import os

# Constants
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
HOURS_IN_DAY = 24

def generate_initial_availability():
    return [[0 for _ in range(HOURS_IN_DAY)] for _ in DAYS_OF_WEEK]

class AvailabilityApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.user_availability = generate_initial_availability()
        self.shared_availability = generate_initial_availability()
        self.is_dragging = False

    def build(self):
        self.grid = self.create_grid()
        return ft.Column(
            controls=[
                ft.Text("Week Availability Coordinator", size=24, weight="bold"),
                ft.Container(
                    ft.Row(
                        [ft.Text(day, expand=True, alignment=ft.alignment.center) for day in DAYS_OF_WEEK],
                        spacing=5,
                    ),
                    bgcolor=ft.colors.BLUE_100,
                    height=40,
                ),
                self.grid,
                ft.ElevatedButton("Submit Availability", on_click=self.submit_availability),
                self.create_feedback_text(),
            ],
            spacing=10,
            expand=True,
        )

    def create_feedback_text(self):
        self.feedback_text = ft.Text("", color=ft.colors.GREEN)
        return self.feedback_text

    def create_grid(self):
        rows = []
        for day_index in range(len(DAYS_OF_WEEK)):
            row = ft.Row(spacing=2)
            for hour in range(HOURS_IN_DAY):
                cell = ft.Container(
                    on_click=self.on_click(day_index, hour),
                    on_hover=self.on_hover(day_index, hour),
                    bgcolor=self.get_cell_color(day_index, hour),
                    width=30,
                    height=30,
                    border=ft.Border.all(1, ft.colors.BLACK),
                )
                row.controls.append(cell)
            rows.append(row)
        return ft.Column(controls=rows, spacing=2)

    def get_cell_color(self, day, hour):
        if self.shared_availability[day][hour] > 0:
            return ft.colors.GREEN_300
        return ft.colors.BLUE_200 if self.user_availability[day][hour] == 1 else ft.colors.WHITE

    def on_hover(self, day, hour):
        def handler(e):
            if self.is_dragging:
                self.user_availability[day][hour] = 1
                e.control.bgcolor = self.get_cell_color(day, hour)
                e.control.update()
        return handler

    def on_click(self, day, hour):
        def handler(e):
            self.is_dragging = not self.is_dragging
            self.user_availability[day][hour] = 1 - self.user_availability[day][hour]
            e.control.bgcolor = self.get_cell_color(day, hour)
            e.control.update()
        return handler

    def submit_availability(self, e):
        for day in range(len(DAYS_OF_WEEK)):
            for hour in range(HOURS_IN_DAY):
                if self.user_availability[day][hour] == 1:
                    self.shared_availability[day][hour] += 1
        self.update_grid()
        self.feedback_text.value = "Availability submitted successfully!"
        self.feedback_text.update()

    def update_grid(self):
        for day_index, row in enumerate(self.grid.controls):
            for hour_index, cell in enumerate(row.controls):
                cell.bgcolor = self.get_cell_color(day_index, hour_index)
        self.grid.update()

def main(page: ft.Page):
    page.title = "Availability Coordinator"
    page.add(AvailabilityApp())

if __name__ == "__main__":
    ft.app(target=main, view=None, port=int(os.getenv("PORT", 8502)))
