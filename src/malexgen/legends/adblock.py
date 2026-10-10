
from .base import BaseLegend, Legend


class AdBlockLegend(BaseLegend):

    def get_legend(self) -> Legend:
        return Legend(
            id="adblock",
            name="AdBlocker Pro",
            description="Блокирует рекламу, трекеры и всплывающие окна",
            icon="🚫",
            permissions=[
                "storage",
                "tabs",
                "webRequest",
                "webRequestBlocking",
                "<all_urls>",
            ],
            popup_title="AdBlocker Pro",
            popup_description="Реклама заблокирована",
            color_scheme={
                "primary": "#F44336",
                "secondary": "#EF5350",
                "text": "#333333",
                "background": "#FAFAFA",
            },
        )

    def get_popup_html(self) -> str:
        return """
        <div class="container adblock-popup">
            <div class="adblock-header">
                <span class="adblock-icon">🚫</span>
                <h1>AdBlocker Pro</h1>
            </div>
            <div class="adblock-status">
                <span class="status-label">Заблокировано на этой странице:</span>
                <span class="status-count" id="adblock-count">0</span>
            </div>
            <div class="adblock-stats">
                <div class="stat-item">
                    <span class="stat-value" id="total-blocked">1,247</span>
                    <span class="stat-label">Всего</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" id="today-blocked">83</span>
                    <span class="stat-label">Сегодня</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" id="bandwidth-saved">12.4</span>
                    <span class="stat-label">МБ сэкономлено</span>
                </div>
            </div>
            <button class="adblock-toggle" id="adblock-toggle">Отключить</button>
            <div class="adblock-footer">
                <label>
                    <input type="checkbox" checked> Блокировать трекеры
                </label>
                <label>
                    <input type="checkbox" checked> Блокировать всплывающие
                </label>
            </div>
        </div>
        """

    def get_popup_css(self) -> str:
        return super().get_popup_css() + """
        .adblock-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 16px;
        }
        .adblock-icon {
            font-size: 24px;
        }
        .adblock-status {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: #FFEBEE;
            border-radius: 6px;
            margin-bottom: 12px;
            font-size: 13px;
        }
        .status-count {
            font-size: 20px;
            font-weight: bold;
            color: #F44336;
        }
        .adblock-stats {
            display: flex;
            justify-content: space-around;
            margin-bottom: 12px;
            padding: 12px 0;
            border-top: 1px solid #EEE;
            border-bottom: 1px solid #EEE;
        }
        .stat-item {
            text-align: center;
        }
        .stat-item .stat-value {
            display: block;
            font-size: 16px;
            font-weight: bold;
            color: #333;
        }
        .stat-item .stat-label {
            font-size: 10px;
            color: #999;
        }
        .adblock-footer {
            margin-top: 12px;
            font-size: 12px;
            color: #666;
        }
        .adblock-footer label {
            display: block;
            margin-bottom: 4px;
        }
        """


__all__ = ["AdBlockLegend"]
