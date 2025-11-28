import flet as ft
import datetime
import asyncio
import random
import traceback

# --- Data Models & State ---

class MonitorState:
    """Holds all the state data for the application."""
    def __init__(self):
        # User Profile Data
        self.name = ""
        self.height = ""
        self.weight = ""
        self.gender = ""
        self.age = ""
        
        # Activity
        self.activity = ""
        
        # Monitoring Data
        self.heart_rate = 72.0  # Starting BPM value
        self.history = []       # Stores (time, BPM) for the chart
        self.logs = []          # Stores alerts and messages
        self.time_counter = 0   
        self.on_update = None   
        self.heart_scale = 1.0  
        self.min_bpm = 999.0    
        self.max_bpm = 0.0      
        self.is_monitoring = False 
        self.total_time = 0
        self.avg_bpm = 0.0      
        self.session_readings = []
        self.history_sessions = [] 

    def log_event(self, message, type="INFO"):
        """Adds a timestamped event to the logs list."""
        now = datetime.datetime.now().strftime("%H:%M:%S")
        if self.logs and self.logs[0]["message"] == message and self.logs[0]["type"] == type:
            return
        self.logs.insert(0, {"time": now, "message": message, "type": type})
        if len(self.logs) > 100:
            self.logs.pop()

monitor_state = MonitorState()

# --- Async Simulation ---

async def run_simulation():
    """Background task to simulate patient vitals using momentum-based randomness."""
    
    # (Min Base HR, Max Base HR, Momentum, Random Fluctuation Size)
    activity_profiles = {
        "Resting": (60, 80, 0.9, 0.5),      
        "Walking": (90, 110, 0.7, 1.0),
        "Running": (130, 160, 0.4, 2.0),
        "Gym": (110, 140, 0.5, 1.5),
        "Swimming": (100, 130, 0.6, 1.2)
    }
    
    base_hr, target_range, momentum, fluctuation = activity_profiles.get(monitor_state.activity, (70, 100, 0.8, 0.8))

    try:
        while monitor_state.is_monitoring:
            
            # 1. Determine the target HR
            target_hr = random.uniform(base_hr, target_range)
            
            # 2. Add high-frequency noise
            random_step = random.uniform(-fluctuation, fluctuation)
            
            # 3. Apply momentum (Smooth transition towards the target)
            monitor_state.heart_rate += (target_hr - monitor_state.heart_rate) * (1 - momentum) + random_step
            
            # **FIX: Round the heart rate to two decimal places for cleaner display**
            monitor_state.heart_rate = round(monitor_state.heart_rate, 2)
            
            # 4. Enforce boundaries
            if monitor_state.heart_rate < 40:
                monitor_state.heart_rate = random.uniform(40, 45)
                monitor_state.log_event(f"Low HR boundary hit: {int(monitor_state.heart_rate)} bpm", "ALERT")
            elif monitor_state.heart_rate > 190:
                monitor_state.heart_rate = random.uniform(180, 190)
                monitor_state.log_event(f"High HR boundary hit: {int(monitor_state.heart_rate)} bpm", "ALERT")
            
            # 5. Update Session Stats
            monitor_state.min_bpm = min(monitor_state.min_bpm, monitor_state.heart_rate)
            monitor_state.max_bpm = max(monitor_state.max_bpm, monitor_state.heart_rate)
            
            monitor_state.session_readings.append(monitor_state.heart_rate)
            if monitor_state.session_readings:
                monitor_state.avg_bpm = sum(monitor_state.session_readings) / len(monitor_state.session_readings)

            # 6. Update Chart History
            monitor_state.time_counter += 1
            monitor_state.total_time += 1
            # Add the new data point, using the rounded value
            monitor_state.history.append((monitor_state.time_counter, monitor_state.heart_rate))
            if len(monitor_state.history) > 60: 
                monitor_state.history.pop(0)
            
            # 7. Heartbeat Animation
            monitor_state.heart_scale = 1.2 if monitor_state.heart_scale == 1.0 else 1.0

            # 8. Refresh UI
            if monitor_state.on_update:
                monitor_state.on_update()
                
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Simulation Error: {e}")
        traceback.print_exc()

def main(page: ft.Page):
    # --- Page Setup ---
    page.title = "Heart Rate Monitor"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1920
    page.window_height = 1080
    
    # Deep Space Blue/Black Gradient background
    page.bgcolor = "#000000" 
    
    # --- UI References ---
    chart_ref = ft.Ref[ft.LineChart]()
    heart_icon_ref = ft.Ref[ft.Icon]()
    hr_text = ft.Text("72", size=60, weight="bold", color="white")
    min_bpm_text = ft.Text("--", size=28, weight="bold", color="white")
    max_bpm_text = ft.Text("--", size=28, weight="bold", color="white")
    avg_bpm_text = ft.Text("--", size=28, weight="bold", color="white")
    dashboard_log_list = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=5)
    
    # --- Profile Page Fields ---
    name_field = ft.TextField(label="Name", hint_text="Enter your name", border_color="white30", focused_border_color="purpleAccent")
    height_field = ft.TextField(label="Height (cm)", hint_text="170", keyboard_type=ft.KeyboardType.NUMBER, border_color="white30", focused_border_color="purpleAccent")
    weight_field = ft.TextField(label="Weight (kg)", hint_text="70", keyboard_type=ft.KeyboardType.NUMBER, border_color="white30", focused_border_color="purpleAccent")
    gender_dropdown = ft.Dropdown(
        label="Gender",
        options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female"), ft.dropdown.Option("Other")],
        border_color="white30", focused_border_color="purpleAccent"
    )
    age_field = ft.TextField(label="Age", hint_text="25", keyboard_type=ft.KeyboardType.NUMBER, border_color="white30", focused_border_color="purpleAccent")

    # --- UI Update Function ---
    def update_ui():
        """Called every second by the simulation to refresh all display values."""
        # Use int() for the main HR display for a clean whole number
        hr_text.value = f"{int(monitor_state.heart_rate)}" 
        
        if monitor_state.min_bpm < 999:
            min_bpm_text.value = f"{int(monitor_state.min_bpm)}"
        if monitor_state.max_bpm > 0:
            max_bpm_text.value = f"{int(monitor_state.max_bpm)}"
        if monitor_state.session_readings:
            avg_bpm_text.value = f"{int(monitor_state.avg_bpm)}"
        
        # Update the Line Chart data
        if chart_ref.current:
            try:
                points = [ft.LineChartDataPoint(x, y) for x, y in monitor_state.history]
                chart_ref.current.data_series[0].data_points = points
                
                if monitor_state.history:
                    min_x = monitor_state.history[0][0]
                    max_x = monitor_state.history[-1][0]
                    chart_ref.current.min_x = min_x
                    chart_ref.current.max_x = max(min_x + 60, max_x) 
                chart_ref.current.update()
            except Exception:
                pass
        
        # Animate the heart icon scale
        if heart_icon_ref.current:
            try:
                heart_icon_ref.current.scale = monitor_state.heart_scale
                heart_icon_ref.current.update()
            except Exception:
                pass

        # Update the Live Alerts log list
        if page.route == "/monitor":
            try:
                dashboard_log_list.controls.clear()
                for log in monitor_state.logs[:8]:
                    color = "redAccent" if log["type"] == "ALERT" else "orangeAccent" if log["type"] == "WARNING" else "grey"
                    icon = "warning" if log["type"] == "ALERT" else "info" if log["type"] == "WARNING" else "circle"
                    dashboard_log_list.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(icon, color=color, size=14),
                                ft.Text(log["time"], color="grey", font_family="monospace", size=10),
                                ft.Text(log["message"], color="white", size=11, expand=True),
                            ], spacing=6),
                            padding=8,
                            bgcolor="white05",
                            border_radius=8,
                            border=ft.border.all(1, f"{color}30")
                        )
                    )
                dashboard_log_list.update()
            except Exception:
                pass

        try:
            hr_text.update()
            min_bpm_text.update()
            max_bpm_text.update()
            avg_bpm_text.update()
        except Exception:
            pass 

    monitor_state.on_update = update_ui

    # --- Button Handlers ---
    
    def save_profile_and_continue(e):
        monitor_state.name = name_field.value or "User"
        monitor_state.height = height_field.value or "N/A"
        monitor_state.weight = weight_field.value or "N/A"
        monitor_state.gender = gender_dropdown.value or "N/A"
        monitor_state.age = age_field.value or "N/A"
        page.go("/activity")
    
    activity_cards_row = ft.Ref[ft.Row]()
    measure_button = ft.Ref[ft.ElevatedButton]()
    
    def select_activity(activity_name):
        def handler(e):
            monitor_state.activity = activity_name
            if activity_cards_row.current:
                activity_cards_row.current.controls = [
                    build_activity_card("Resting", "spa", "#9C27B0", monitor_state.activity == "Resting"),
                    build_activity_card("Walking", "directions_walk", "#4CAF50", monitor_state.activity == "Walking"),
                    build_activity_card("Running", "directions_run", "#FF9800", monitor_state.activity == "Running"),
                    build_activity_card("Gym", "fitness_center", "#F44336", monitor_state.activity == "Gym"),
                    build_activity_card("Swimming", "pool", "#2196F3", monitor_state.activity == "Swimming"),
                ]
                activity_cards_row.current.update()
            if measure_button.current:
                measure_button.current.disabled = False
                measure_button.current.update()
        return handler
    
    def start_monitoring(e):
        if monitor_state.activity:
            monitor_state.is_monitoring = True
            monitor_state.min_bpm = 999.0
            monitor_state.max_bpm = 0.0
            monitor_state.avg_bpm = 0.0
            monitor_state.total_time = 0
            monitor_state.session_readings = []
            monitor_state.history = []
            monitor_state.time_counter = 0
            monitor_state.logs = []
            page.run_task(run_simulation)
            page.go("/monitor")
    
    def stop_monitoring(e):
        monitor_state.is_monitoring = False
        if monitor_state.session_readings:
            session_data = {
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "activity": monitor_state.activity,
                "duration": f"{monitor_state.total_time // 60}:{monitor_state.total_time % 60:02d}",
                "avg_bpm": round(monitor_state.avg_bpm, 1),
                "max_bpm": int(monitor_state.max_bpm),
                "min_bpm": int(monitor_state.min_bpm)
            }
            monitor_state.history_sessions.append(session_data)
        page.go("/activity")

    # --- UI Component Builders ---

    def build_glass_card(content, height=None, expand=False):
        """Creates a modern, translucent card with a blur effect."""
        return ft.Container(
            content=content,
            bgcolor="white10",
            blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR),
            border=ft.border.all(1, "white10"),
            border_radius=20,
            padding=25,
            height=height,
            expand=expand,
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=20, color="black26", offset=ft.Offset(0, 10),
            )
        )

    def build_activity_card(activity_name, icon, color, is_selected):
        """Creates a selectable card for different activities."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=50, color=color if is_selected else "white70"),
                    ft.Text(activity_name, size=16, weight="bold", color="white" if is_selected else "white70"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            bgcolor=f"{color}30" if is_selected else "white10",
            border=ft.border.all(3 if is_selected else 1, color if is_selected else "white10"),
            border_radius=20,
            padding=30,
            on_click=select_activity(activity_name),
            animate=200,
        )

    # --- Page Definitions ---

    def create_profile_page():
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("👤 User Profile", size=36, weight="bold", color="white"),
                    ft.Text("Please enter your information", size=16, color="white70"),
                    ft.Container(height=20),
                    build_glass_card(
                        content=ft.Column(
                            [
                                name_field,
                                ft.Row([ft.Container(content=height_field, expand=True), ft.Container(content=weight_field, expand=True)], spacing=20),
                                ft.Row([ft.Container(content=gender_dropdown, expand=True), ft.Container(content=age_field, expand=True)], spacing=20),
                                ft.Container(height=20),
                                ft.ElevatedButton(
                                    "Continue →",
                                    on_click=save_profile_and_continue,
                                    style=ft.ButtonStyle(bgcolor="purpleAccent", color="white", padding=20),
                                    width=200, height=50
                                )
                            ],
                            spacing=20
                        ),
                        height=500
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center, end=ft.alignment.bottom_center,
                colors=["#0A1931", "#152238", "#0A1931"], 
            ),
            padding=40, expand=True, alignment=ft.alignment.center
        )

    def create_activity_page():
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([ft.IconButton("arrow_back", icon_color="white", on_click=lambda _: page.go("/profile")), ft.Text("Select Activity", size=32, weight="bold", color="white")]),
                    ft.Container(height=20),
                    ft.Row(
                        ref=activity_cards_row,
                        controls=[
                            build_activity_card("Resting", "spa", "#9C27B0", monitor_state.activity == "Resting"),
                            build_activity_card("Walking", "directions_walk", "#4CAF50", monitor_state.activity == "Walking"),
                            build_activity_card("Running", "directions_run", "#FF9800", monitor_state.activity == "Running"),
                            build_activity_card("Gym", "fitness_center", "#F44336", monitor_state.activity == "Gym"),
                            build_activity_card("Swimming", "pool", "#2196F3", monitor_state.activity == "Swimming"),
                        ],
                        spacing=20, alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(height=40),
                    ft.ElevatedButton(
                        ref=measure_button, text="📊 Measure BPM", on_click=lambda e: start_monitoring(e),
                        style=ft.ButtonStyle(bgcolor="greenAccent700", color="white", padding=25),
                        width=300, height=60, disabled=not monitor_state.activity
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center, end=ft.alignment.bottom_center,
                colors=["#0A1931", "#152238", "#0A1931"], 
            ),
            padding=40, expand=True, alignment=ft.alignment.center
        )

    def create_monitor_page():
        activity_icons = {"Resting": "spa", "Walking": "directions_walk", "Running": "directions_run", "Gym": "fitness_center", "Swimming": "pool"}
        activity_colors = {"Resting": "#9C27B0", "Walking": "#4CAF50", "Running": "#FF9800", "Gym": "#F44336", "Swimming": "#2196F3"}
        
        return ft.Container(
            content=ft.Row(
                [
                    # --- Left Sidebar (Profile and Stats) ---
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row([ft.IconButton("arrow_back", icon_color="white", on_click=stop_monitoring), ft.Text("Monitor", size=24, weight="bold", color="white")]),
                                ft.Container(height=10),
                                build_glass_card(content=ft.Column([
                                    ft.Row([ft.Icon("person", color="purpleAccent", size=24), ft.Text("User Profile", size=18, weight="bold", color="white")]),
                                    ft.Divider(color="white10"),
                                    ft.Text(f"Name: {monitor_state.name}", color="white70", size=14),
                                    ft.Text(f"Age: {monitor_state.age} years", color="white70", size=14),
                                    ft.Text(f"Height: {monitor_state.height} cm", color="white70", size=14),
                                    ft.Text(f"Weight: {monitor_state.weight} kg", color="white70", size=14),
                                    ft.Text(f"Gender: {monitor_state.gender}", color="white70", size=14),
                                ], spacing=8), height=220),
                                ft.Container(height=15),
                                
                                ft.Container( # Activity Card
                                    content=ft.Column([
                                        ft.Row([ft.Icon(activity_icons.get(monitor_state.activity, "circle"), color=activity_colors.get(monitor_state.activity, "white"), size=28),
                                                ft.Text(monitor_state.activity, size=20, weight="bold", color="white")]),
                                        ft.Text("Current Activity", color="white54", size=12),
                                    ], spacing=5),
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.top_left, end=ft.alignment.bottom_right,
                                        colors=[activity_colors.get(monitor_state.activity, "#666666") + "80", activity_colors.get(monitor_state.activity, "#444444")],
                                    ),
                                    padding=20, border_radius=20, height=120,
                                    shadow=ft.BoxShadow(blur_radius=15, color=activity_colors.get(monitor_state.activity, "black"))
                                ),
                                ft.Container(height=15),
                                
                                # Stat Cards (Min, Max, Avg)
                                ft.Container(content=ft.Column([ft.Row([ft.Icon("trending_down", color="cyanAccent", size=20), ft.Text("Min BPM", color="white", size=14, weight="bold")]), ft.Row([min_bpm_text, ft.Text("bpm", color="white70", size=12, offset=ft.Offset(0, 0.15))], vertical_alignment=ft.CrossAxisAlignment.END), ft.Text("Lowest recorded", color="white54", size=10)], spacing=5),
                                    gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#00BCD4", "#0097A7"]), padding=20, border_radius=20, expand=True ),
                                ft.Container(height=15),
                                ft.Container(content=ft.Column([ft.Row([ft.Icon("trending_up", color="pinkAccent", size=20), ft.Text("Max BPM", color="white", size=14, weight="bold")]), ft.Row([max_bpm_text, ft.Text("bpm", color="white70", size=12, offset=ft.Offset(0, 0.15))], vertical_alignment=ft.CrossAxisAlignment.END), ft.Text("Highest recorded", color="white54", size=10)], spacing=5),
                                    gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#E91E63", "#C2185B"]), padding=20, border_radius=20, expand=True),
                                ft.Container(height=15),
                                ft.Container(content=ft.Column([ft.Row([ft.Icon("equalizer", color="yellowAccent", size=20), ft.Text("Avg BPM", color="white", size=14, weight="bold")]), ft.Row([avg_bpm_text, ft.Text("bpm", color="white70", size=12, offset=ft.Offset(0, 0.15))], vertical_alignment=ft.CrossAxisAlignment.END), ft.Text("Average recorded", color="white54", size=10)], spacing=5),
                                    gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#FFC107", "#FF9800"]), padding=20, border_radius=20, expand=True),
                            ],
                            scroll=ft.ScrollMode.AUTO, spacing=0
                        ),
                        width=600, padding=20,
                        gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=["#0A1931", "#152238", "#0A1931"]),
                    ),
                    
                    # --- Right Content (BPM Value, Chart, and Logs) ---
                    ft.Container(
                        content=ft.Column(
                            [
                                # 1. Current BPM Display
                                ft.Container(
                                    content=ft.Column([
                                        ft.Row([ft.Icon("favorite", color="redAccent", size=32, ref=heart_icon_ref, animate_scale=300), ft.Text("Heart Rate", size=24, weight="bold", color="white")]),
                                        ft.Container(height=10),
                                        ft.Row([hr_text, ft.Text("bpm", color="white70", size=24, offset=ft.Offset(0, 0.2))], vertical_alignment=ft.CrossAxisAlignment.END, alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Text("Real-time monitoring", color="white54", size=14),
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                                    gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#FF5252", "#D50000"]),
                                    padding=30, border_radius=25, height=220, 
                                ),
                                ft.Container(height=20),
                                
                                # 2. Chart and Logs Row
                                ft.Row(
                                    [
                                        # Chart Card
                                        build_glass_card(
                                            content=ft.Column([
                                                ft.Row([ft.Icon("show_chart", color="purpleAccent"), ft.Text("Real-time ECG", color="white", size=18, weight="bold")]),
                                                ft.Container(height=10),
                                                ft.LineChart( 
                                                    ref=chart_ref,
                                                    data_series=[
                                                        ft.LineChartData(data_points=[], stroke_width=3, color="purpleAccent", curved=True,)
                                                    ],
                                                    border=ft.border.all(0, "transparent"),
                                                    # Hiding axis labels to clean up the graph area
                                                    left_axis=ft.ChartAxis(labels_size=0, title=ft.Text("")), 
                                                    bottom_axis=ft.ChartAxis(labels_size=0, title=ft.Text("")), 
                                                    min_y=30, max_y=180, 
                                                    expand=True, 
                                                )
                                            ]),
                                            expand=2 
                                        ),
                                        
                                        # Alerts Log Card
                                        build_glass_card(
                                            content=ft.Column([
                                                ft.Row([ft.Icon("notifications_active", color="yellowAccent"), ft.Text("Live Alerts", color="white", size=18, weight="bold")]),
                                                ft.Container(height=10),
                                                ft.Container(content=dashboard_log_list, expand=True)
                                            ]),
                                            expand=1 
                                        ),
                                    ],
                                    spacing=20, expand=True 
                                )
                            ],
                            spacing=0, expand=True 
                        ),
                        expand=True, padding=20,
                        gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=["#0A1931", "#152238", "#0A1931"]),
                    )
                ],
                spacing=0
            ),
            expand=True
        )

    def create_history_page():
        history_list = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)
        
        def build_history_list():
            history_list.controls.clear()
            if not monitor_state.history_sessions:
                history_list.controls.append(ft.Text("No sessions recorded yet", color="white70", size=16))
            else:
                for session in monitor_state.history_sessions:
                    activity_colors = {"Resting": "#9C27B0", "Walking": "#4CAF50", "Running": "#FF9800", "Gym": "#F44336", "Swimming": "#2196F3"}
                    
                    history_list.controls.insert(0,
                        ft.Container(
                            content=ft.Row([
                                ft.Container(width=5, bgcolor=activity_colors.get(session["activity"], "white")),
                                ft.Column([
                                    ft.Text(f"{session['activity']} Session", size=18, weight="bold", color="white"),
                                    ft.Text(f"Date: {session['date']} | Duration: {session['duration']}", size=12, color="white54"),
                                ], expand=True),
                                ft.Column([
                                    ft.Row([ft.Icon("favorite", color="redAccent", size=14), ft.Text(f"Avg: {session['avg_bpm']} BPM", size=14, color="white")]),
                                    ft.Row([ft.Icon("trending_up", color="pinkAccent", size=14), ft.Text(f"Max: {session['max_bpm']} BPM", size=14, color="white")]),
                                    ft.Row([ft.Icon("trending_down", color="cyanAccent", size=14), ft.Text(f"Min: {session['min_bpm']} BPM", size=14, color="white")]),
                                ], horizontal_alignment=ft.CrossAxisAlignment.END)
                            ], spacing=15),
                            padding=15, bgcolor="white10", border_radius=10,
                            shadow=ft.BoxShadow(blur_radius=10, color="black26")
                        )
                    )
            history_list.update()
            
        build_history_list()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([ft.IconButton("arrow_back", icon_color="white", on_click=lambda _: page.go("/activity")), ft.Text("Session History", size=32, weight="bold", color="white")]),
                    ft.Container(height=20),
                    build_glass_card(content=history_list, expand=True)
                ],
                expand=True, padding=40
            ),
            gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=["#0A1931", "#152238", "#0A1931"]),
            expand=True
        )

    # --- Routing Logic ---

    def route_change(route):
        page.views.clear()
        
        page.views.append(ft.View("/profile", [create_profile_page()], padding=0, scroll=ft.ScrollMode.AUTO))
        
        if page.route == "/activity" or page.route == "/monitor" or page.route == "/history":
            page.views.append(ft.View("/activity", [create_activity_page()], padding=0, scroll=ft.ScrollMode.AUTO))

        if page.route == "/monitor":
            page.views.append(ft.View("/monitor", [create_monitor_page()], padding=0))

        if page.route == "/history":
            if "/activity" not in [v.route for v in page.views]:
                 page.views.append(ft.View("/activity", [create_activity_page()], padding=0, scroll=ft.ScrollMode.AUTO))
            if "/monitor" not in [v.route for v in page.views]:
                 page.views.append(ft.View("/monitor", [create_monitor_page()], padding=0))
                 
            page.views.append(ft.View("/history", [create_history_page()], padding=0))
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    
if __name__ == "__main__":
    ft.app(target=main)