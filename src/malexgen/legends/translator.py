from .base import BaseLegend, Legend


class TranslatorLegend(BaseLegend):

    def get_legend(self) -> Legend:
        return Legend(
            id="translator",
            name="TransLite",
            description="Мгновенный перевод текста на любой сайт",
            icon="🌐",
            permissions=[
                "storage",
                "activeTab",
                "contextMenus",
                "<all_urls>",
            ],
            popup_title="TransLite",
            popup_description="Переводчик",
            color_scheme={
                "primary": "#2196F3",
                "secondary": "#64B5F6",
                "text": "#333333",
                "background": "#F5F5F5",
            },
        )

    def get_popup_html(self) -> str:
        return """
        <div class="container translator-popup">
            <div class="translator-header">
                <span class="translator-icon">🌐</span>
                <h1>TransLite</h1>
            </div>
            <div class="translator-controls">
                <select id="from-lang">
                    <option>Авто</option>
                    <option>Русский</option>
                    <option>English</option>
                </select>
                <span class="arrow">→</span>
                <select id="to-lang">
                    <option>English</option>
                    <option>Русский</option>
                    <option>Deutsch</option>
                </select>
            </div>
            <textarea id="translate-input" placeholder="Введите текст..."></textarea>
            <button id="translate-btn">Перевести</button>
            <div class="translator-result" id="translate-result">
                Результат появится здесь...
            </div>
            <div class="translator-footer">
                <label>
                    <input type="checkbox" checked> Переводить при выделении
                </label>
            </div>
        </div>
        """

    def get_popup_css(self) -> str:
        return super().get_popup_css() + """
        .translator-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }
        .translator-icon {
            font-size: 24px;
        }
        .translator-controls {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }
        .translator-controls select {
            flex: 1;
            padding: 6px;
            border: 1px solid #DDD;
            border-radius: 4px;
            font-size: 12px;
        }
        .arrow {
            color: #2196F3;
            font-weight: bold;
        }
        textarea {
            width: 100%;
            box-sizing: border-box;
            padding: 8px;
            border: 1px solid #DDD;
            border-radius: 4px;
            font-size: 13px;
            resize: vertical;
            min-height: 60px;
            margin-bottom: 8px;
        }
        .translator-result {
            margin-top: 8px;
            padding: 8px;
            background: #E3F2FD;
            border-radius: 4px;
            font-size: 13px;
            min-height: 40px;
        }
        .translator-footer {
            margin-top: 12px;
            font-size: 12px;
            color: #666;
        }
        """


__all__ = ["TranslatorLegend"]
