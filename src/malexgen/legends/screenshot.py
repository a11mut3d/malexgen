from .base import BaseLegend, Legend


class ScreenshotLegend(BaseLegend):

    def get_legend(self) -> Legend:
        return Legend(
            id="screenshot",
            name="ScreenCapture",
            description="Делайте скриншоты, редактируйте и делитесь",
            icon="📸",
            permissions=[
                "storage",
                "activeTab",
                "tabs",
                "<all_urls>",
            ],
            popup_title="ScreenCapture",
            popup_description="Скриншоты",
            color_scheme={
                "primary": "#FF5722",
                "secondary": "#FF8A65",
                "text": "#333333",
                "background": "#F5F5F5",
            },
        )

    def get_popup_html(self) -> str:
        return """
        <div class="container screenshot-popup">
            <div class="screenshot-header">
                <span class="screenshot-icon">📸</span>
                <h1>ScreenCapture</h1>
            </div>
            <div class="screenshot-modes">
                <button class="mode-btn active" data-mode="visible">
                    <span>👁️</span>
                    <span>Видимая часть</span>
                </button>
                <button class="mode-btn" data-mode="full">
                    <span>📄</span>
                    <span>Вся страница</span>
                </button>
                <button class="mode-btn" data-mode="selection">
                    <span>✂️</span>
                    <span>Выделение</span>
                </button>
            </div>
            <button class="screenshot-btn" id="take-screenshot">
                📸 Сделать скриншот
            </button>
            <div class="screenshot-options">
                <label>
                    <input type="checkbox" checked> Копировать в буфер
                </label>
                <label>
                    <input type="checkbox"> Открыть редактор
                </label>
                <label>
                    <input type="checkbox"> Сохранить автоматически
                </label>
            </div>
            <div class="screenshot-history">
                <div class="history-title">Последние:</div>
                <div class="history-thumbs">
                    <div class="thumb">📷</div>
                    <div class="thumb">📷</div>
                    <div class="thumb">📷</div>
                </div>
            </div>
        </div>
        """

    def get_popup_css(self) -> str:
        return super().get_popup_css() + """
        .screenshot-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 16px;
        }
        .screenshot-icon {
            font-size: 24px;
        }
        .screenshot-modes {
            display: flex;
            gap: 6px;
            margin-bottom: 12px;
        }
        .mode-btn {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            padding: 8px 4px;
            background: #FFF;
            border: 1px solid #DDD;
            border-radius: 6px;
            font-size: 10px;
            cursor: pointer;
            color: #333;
        }
        .mode-btn.active {
            border-color: #FF5722;
            background: #FBE9E7;
        }
        .mode-btn span:first-child {
            font-size: 16px;
        }
        .screenshot-btn {
            margin-bottom: 12px;
        }
        .screenshot-options {
            font-size: 12px;
            color: #666;
            margin-bottom: 12px;
        }
        .screenshot-options label {
            display: block;
            margin-bottom: 4px;
        }
        .screenshot-history {
            padding-top: 12px;
            border-top: 1px solid #EEE;
        }
        .history-title {
            font-size: 11px;
            color: #999;
            margin-bottom: 6px;
        }
        .history-thumbs {
            display: flex;
            gap: 6px;
        }
        .thumb {
            width: 40px;
            height: 30px;
            background: #EEE;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
        }
        """


__all__ = ["ScreenshotLegend"]
