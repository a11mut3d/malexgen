from .base import BaseLegend, Legend


class NotesLegend(BaseLegend):

    def get_legend(self) -> Legend:
        return Legend(
            id="notes",
            name="QuickNotes",
            description="Быстрые заметки прямо в браузере",
            icon="📝",
            permissions=[
                "storage",
                "activeTab",
                "contextMenus",
                "<all_urls>",
            ],
            popup_title="QuickNotes",
            popup_description="Заметки",
            color_scheme={
                "primary": "#FFC107",
                "secondary": "#FFD54F",
                "text": "#333333",
                "background": "#FFFDE7",
            },
        )

    def get_popup_html(self) -> str:
        return """
        <div class="container notes-popup">
            <div class="notes-header">
                <span class="notes-icon">📝</span>
                <h1>QuickNotes</h1>
            </div>
            <div class="notes-list">
                <div class="note-item">
                    <div class="note-title">Купить молоко</div>
                    <div class="note-preview">Не забыть про хлеб...</div>
                    <div class="note-date">Сегодня, 14:30</div>
                </div>
                <div class="note-item">
                    <div class="note-title">Идея для проекта</div>
                    <div class="note-preview">Сделать генератор расширений...</div>
                    <div class="note-date">Вчера, 22:15</div>
                </div>
                <div class="note-item">
                    <div class="note-title">Пароль от Wi-Fi</div>
                    <div class="note-preview">qwerty12345...</div>
                    <div class="note-date">12 октября</div>
                </div>
            </div>
            <button class="notes-add" id="notes-add">+ Новая заметка</button>
            <div class="notes-footer">
                <span>3 заметки</span>
                <span>·</span>
                <span>Синхронизировано</span>
            </div>
        </div>
        """

    def get_popup_css(self) -> str:
        return super().get_popup_css() + """
        .notes-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }
        .notes-icon {
            font-size: 24px;
        }
        .notes-list {
            margin-bottom: 12px;
            max-height: 240px;
            overflow-y: auto;
        }
        .note-item {
            padding: 10px;
            background: #FFF;
            border-radius: 6px;
            margin-bottom: 8px;
            cursor: pointer;
            border-left: 3px solid #FFC107;
        }
        .note-item:hover {
            background: #FFF9C4;
        }
        .note-title {
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 2px;
        }
        .note-preview {
            font-size: 11px;
            color: #666;
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .note-date {
            font-size: 10px;
            color: #AAA;
        }
        .notes-footer {
            display: flex;
            justify-content: center;
            gap: 6px;
            margin-top: 8px;
            font-size: 11px;
            color: #999;
        }
        """


__all__ = ["NotesLegend"]
