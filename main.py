import flet as ft
from datetime import datetime, timedelta

# Constants
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
HOURS_IN_DAY = 24

# Helper to generate grid data
def generate_initial_availability():
    return [[0 for _ in range(HOURS_IN_DAY)] for _ in DAYS_OF_WEEK]

class AvailabilityApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.user_availability = generate_initial_availability()
        self.shared_availability = generate_initial_availability()
        self.is_dragging = False
        self.selected_day = None

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
            ],
            spacing=10,
            expand=True,
        )

    def create_grid(self):
        grid = ft.GridView(
            expand=True,
            child_aspect_ratio=1 / 2,
            runs_count=7,
            max_cross_axis_extent=150,
        )
        for day_index, day in enumerate(DAYS_OF_WEEK):
            for hour in range(HOURS_IN_DAY):
                cell = ft.Container(
                    on_hover=self.on_hover(day_index, hour),
                    on_click=self.on_click(day_index, hour),
                    width=50,
                    height=50,
                    bgcolor=self.get_cell_color(day_index, hour),
                    border=ft.Border.all(1, ft.colors.BLACK),
                )
                grid.controls.append(cell)
        return grid

    def get_cell_color(self, day, hour):
        if self.shared_availability[day][hour] > 0:
            return ft.colors.GREEN_300
        return ft.colors.WHITE if self.user_availability[day][hour] == 0 else ft.colors.BLUE_200

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
        # Aggregate availability (mock example; replace with server logic)
        for day in range(len(DAYS_OF_WEEK)):
            for hour in range(HOURS_IN_DAY):
                if self.user_availability[day][hour] == 1:
                    self.shared_availability[day][hour] += 1
        self.grid.update()

def main(page: ft.Page):
    page.title = "Availability Coordinator"
    page.add(AvailabilityApp())

if __name__ == "__main__":
    ft.app(target=main)


ft.app(target=main, view=None, port=int(os.getenv("PORT", 8502)))
