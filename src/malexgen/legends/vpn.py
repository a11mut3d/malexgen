from .base import BaseLegend, Legend


class VPNLegend(BaseLegend):

    def get_legend(self) -> Legend:
        return Legend(
            id="vpn",
            name="SecureVPN",
            description="Быстрый и безопасный VPN для вашего браузера",
            icon="🔒",
            permissions=[
                "storage",
                "tabs",
                "cookies",
                "webRequest",
                "<all_urls>",
            ],
            popup_title="SecureVPN",
            popup_description="Ваше соединение защищено",
            color_scheme={
                "primary": "#4CAF50",
                "secondary": "#81C784",
                "text": "#FFFFFF",
                "background": "#F5F5F5",
            },
        )

    def get_popup_html(self) -> str:
        return """
        <div class="container vpn-popup">
            <div class="vpn-header">
                <span class="vpn-icon">🔒</span>
                <h1>SecureVPN</h1>
            </div>
            <div class="vpn-status">
                <div class="status-indicator connected"></div>
                <span>Защищено</span>
            </div>
            <div class="vpn-location">
                <label>Локация:</label>
                <select id="vpn-location">
                    <option value="nl">🇳🇱 Нидерланды</option>
                    <option value="de">🇩🇪 Германия</option>
                    <option value="us">🇺🇸 США</option>
                    <option value="jp">🇯🇵 Япония</option>
                </select>
            </div>
            <button class="vpn-connect" id="vpn-toggle">Отключить</button>
            <div class="vpn-stats">
                <div class="stat">
                    <span class="stat-label">IP:</span>
                    <span class="stat-value">185.xx.xx.xx</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Скорость:</span>
                    <span class="stat-value">45 Мбит/с</span>
                </div>
            </div>
        </div>
        """

    def get_popup_css(self) -> str:
        return super().get_popup_css() + """
        .vpn-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 16px;
        }
        .vpn-icon {
            font-size: 24px;
        }
        .vpn-status {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px;
            background: #E8F5E9;
            border-radius: 6px;
            margin-bottom: 12px;
        }
        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #4CAF50;
        }
        .status-indicator.connected {
            box-shadow: 0 0 8px #4CAF50;
        }
        .vpn-location {
            margin-bottom: 12px;
        }
        .vpn-location label {
            display: block;
            font-size: 12px;
            color: #666;
            margin-bottom: 4px;
        }
        .vpn-location select {
            width: 100%;
            padding: 8px;
            border: 1px solid #DDD;
            border-radius: 6px;
        }
        .vpn-stats {
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid #EEE;
            font-size: 12px;
            color: #666;
        }
        .stat {
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
        }
        """


__all__ = ["VPNLegend"]
