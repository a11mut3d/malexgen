from .base import BaseLegend, Legend


class DarkThemeLegend(BaseLegend):

    def get_legend(self) -> Legend:
        return Legend(
            id="dark_theme",
            name="DarkMode",
            description="Тёмная тема для всех сайтов — берегите глаза",
            icon="🌙",
            permissions=[
                "storage",
                "activeTab",
                "<all_urls>",
            ],
            popup_title="DarkMode",
            popup_description="Тёмная тема",
            color_scheme={
                "primary": "#212121",
                "secondary": "#424242",
                "text": "#FFFFFF",
                "background": "#121212",
            },
        )

    def get_popup_html(self) -> str:
        return """
        <div class="container dark-popup">
            <div class="dark-header">
                <span class="dark-icon">🌙</span>
                <h1>DarkMode</h1>
            </div>
            <div class="dark-toggle-wrap">
                <label class="switch">
                    <input type="checkbox" id="dark-toggle" checked>
                    <span class="slider"></span>
                </label>
                <span class="toggle-label">Включено</span>
            </div>
            <div class="dark-options">
                <div class="option">
                    <label>Яркость</label>
                    <input type="range" min="0" max="100" value="80" id="brightness">
                </div>
                <div class="option">
                    <label>Контраст</label>
                    <input type="range" min="0" max="100" value="60" id="contrast">
                </div>
                <div class="option">
                    <label>Сепия</label>
                    <input type="range" min="0" max="100" value="0" id="sepia">
                </div>
            </div>
            <div class="dark-schedule">
                <label>
                    <input type="checkbox"> По расписанию
                </label>
                <div class="schedule-times">
                    <span>🌅 07:00</span>
                    <span>🌇 19:00</span>
                </div>
            </div>
        </div>
        """

    def get_popup_css(self) -> str:
        return super().get_popup_css() + """
        .dark-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 16px;
        }
        .dark-icon {
            font-size: 24px;
        }
        .dark-toggle-wrap {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            padding: 12px;
            background: #1E1E1E;
            border-radius: 6px;
        }
        .switch {
            position: relative;
            display: inline-block;
            width: 44px;
            height: 24px;
        }
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: #555;
            border-radius: 24px;
            transition: 0.3s;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 18px;
            width: 18px;
            left: 3px;
            bottom: 3px;
            background: white;
            border-radius: 50%;
            transition: 0.3s;
        }
        .switch input:checked + .slider {
            background: #BB86FC;
        }
        .switch input:checked + .slider:before {
            transform: translateX(20px);
        }
        .toggle-label {
            font-size: 13px;
        }
        .dark-options .option {
            margin-bottom: 12px;
        }
        .dark-options label {
            display: block;
            font-size: 12px;
            color: #AAA;
            margin-bottom: 4px;
        }
        .dark-options input[type=range] {
            width: 100%;
            accent-color: #BB86FC;
        }
        .dark-schedule {
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid #333;
            font-size: 12px;
        }
        .schedule-times {
            display: flex;
            justify-content: space-between;
            margin-top: 6px;
            color: #888;
        }
        """


__all__ = ["DarkThemeLegend"]
