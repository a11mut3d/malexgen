from .base import BaseLegend, Legend


class WeatherLegend(BaseLegend):

    def get_legend(self) -> Legend:
        return Legend(
            id="weather",
            name="WeatherNow",
            description="Точный прогноз погоды в новой вкладке",
            icon="☀️",
            permissions=[
                "storage",
                "geolocation",
                "activeTab",
                "<all_urls>",
            ],
            popup_title="WeatherNow",
            popup_description="Погода",
            color_scheme={
                "primary": "#03A9F4",
                "secondary": "#4FC3F7",
                "text": "#333333",
                "background": "#E1F5FE",
            },
        )

    def get_popup_html(self) -> str:
        return """
        <div class="container weather-popup">
            <div class="weather-header">
                <span class="weather-icon">☀️</span>
                <h1>WeatherNow</h1>
            </div>
            <div class="weather-current">
                <div class="weather-temp">+18°</div>
                <div class="weather-desc">Солнечно</div>
                <div class="weather-location">📍 Москва</div>
            </div>
            <div class="weather-details">
                <div class="detail">
                    <span class="detail-icon">💨</span>
                    <span class="detail-value">3 м/с</span>
                    <span class="detail-label">Ветер</span>
                </div>
                <div class="detail">
                    <span class="detail-icon">💧</span>
                    <span class="detail-value">45%</span>
                    <span class="detail-label">Влажность</span>
                </div>
                <div class="detail">
                    <span class="detail-icon">🌡️</span>
                    <span class="detail-value">+21°</span>
                    <span class="detail-label">Ощущается</span>
                </div>
            </div>
            <div class="weather-forecast">
                <div class="forecast-day">
                    <div class="day-name">Пн</div>
                    <div class="day-icon">☀️</div>
                    <div class="day-temp">+20°</div>
                </div>
                <div class="forecast-day">
                    <div class="day-name">Вт</div>
                    <div class="day-icon">⛅</div>
                    <div class="day-temp">+17°</div>
                </div>
                <div class="forecast-day">
                    <div class="day-name">Ср</div>
                    <div class="day-icon">🌧️</div>
                    <div class="day-temp">+14°</div>
                </div>
                <div class="forecast-day">
                    <div class="day-name">Чт</div>
                    <div class="day-icon">☀️</div>
                    <div class="day-temp">+19°</div>
                </div>
            </div>
            <div class="weather-footer">
                <label>
                    <input type="checkbox" checked> Показывать в новой вкладке
                </label>
            </div>
        </div>
        """

    def get_popup_css(self) -> str:
        return super().get_popup_css() + """
        .weather-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }
        .weather-icon {
            font-size: 24px;
        }
        .weather-current {
            text-align: center;
            padding: 16px;
            background: #FFF;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        .weather-temp {
            font-size: 42px;
            font-weight: 300;
            color: #03A9F4;
        }
        .weather-desc {
            font-size: 14px;
            color: #666;
            margin-bottom: 4px;
        }
        .weather-location {
            font-size: 12px;
            color: #999;
        }
        .weather-details {
            display: flex;
            justify-content: space-around;
            margin-bottom: 12px;
            padding: 10px 0;
            background: #FFF;
            border-radius: 8px;
        }
        .detail {
            text-align: center;
        }
        .detail-icon {
            display: block;
            font-size: 16px;
            margin-bottom: 2px;
        }
        .detail-value {
            display: block;
            font-size: 12px;
            font-weight: 500;
        }
        .detail-label {
            display: block;
            font-size: 10px;
            color: #999;
        }
        .weather-forecast {
            display: flex;
            justify-content: space-around;
            padding: 10px 0;
            background: #FFF;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        .forecast-day {
            text-align: center;
        }
        .day-name {
            font-size: 11px;
            color: #666;
        }
        .day-icon {
            font-size: 18px;
            margin: 4px 0;
        }
        .day-temp {
            font-size: 12px;
            font-weight: 500;
        }
        .weather-footer {
            font-size: 11px;
            color: #666;
        }
        """


__all__ = ["WeatherLegend"]
