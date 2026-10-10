from .base import BaseLegend, Legend


class PDFConverterLegend(BaseLegend):

    def get_legend(self) -> Legend:
        return Legend(
            id="pdf_converter",
            name="PDFMaster",
            description="Конвертируйте любые страницы в PDF одним кликом",
            icon="📄",
            permissions=[
                "storage",
                "tabs",
                "activeTab",
                "downloads",
                "<all_urls>",
            ],
            popup_title="PDFMaster",
            popup_description="PDF-конвертер",
            color_scheme={
                "primary": "#E53935",
                "secondary": "#EF5350",
                "text": "#333333",
                "background": "#FFEBEE",
            },
        )

    def get_popup_html(self) -> str:
        return """
        <div class="container pdf-popup">
            <div class="pdf-header">
                <span class="pdf-icon">📄</span>
                <h1>PDFMaster</h1>
            </div>
            <div class="pdf-options">
                <div class="option-group">
                    <label>Формат:</label>
                    <select id="pdf-format">
                        <option>A4</option>
                        <option>Letter</option>
                        <option>Legal</option>
                    </select>
                </div>
                <div class="option-group">
                    <label>Ориентация:</label>
                    <div class="radio-group">
                        <label><input type="radio" name="orient" checked> Портрет</label>
                        <label><input type="radio" name="orient"> Ландшафт</label>
                    </div>
                </div>
                <div class="option-group">
                    <label>Качество:</label>
                    <input type="range" min="50" max="100" value="90" id="pdf-quality">
                </div>
            </div>
            <div class="pdf-checkboxes">
                <label><input type="checkbox" checked> Включить изображения</label>
                <label><input type="checkbox" checked> Включить ссылки</label>
                <label><input type="checkbox"> Только текст</label>
            </div>
            <button class="pdf-convert" id="pdf-convert">
                📥 Скачать PDF
            </button>
            <div class="pdf-footer">
                <span>Последний: 2 минуты назад</span>
            </div>
        </div>
        """

    def get_popup_css(self) -> str:
        return super().get_popup_css() + """
        .pdf-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }
        .pdf-icon {
            font-size: 24px;
        }
        .pdf-options {
            margin-bottom: 12px;
        }
        .option-group {
            margin-bottom: 10px;
        }
        .option-group > label {
            display: block;
            font-size: 11px;
            color: #666;
            margin-bottom: 4px;
        }
        .option-group select {
            width: 100%;
            padding: 6px;
            border: 1px solid #DDD;
            border-radius: 4px;
            font-size: 12px;
        }
        .radio-group {
            display: flex;
            gap: 12px;
            font-size: 12px;
        }
        .option-group input[type=range] {
            width: 100%;
            accent-color: #E53935;
        }
        .pdf-checkboxes {
            font-size: 12px;
            color: #666;
            margin-bottom: 12px;
        }
        .pdf-checkboxes label {
            display: block;
            margin-bottom: 4px;
        }
        .pdf-convert {
            margin-bottom: 8px;
        }
        .pdf-footer {
            text-align: center;
            font-size: 10px;
            color: #999;
        }
        """


__all__ = ["PDFConverterLegend"]
